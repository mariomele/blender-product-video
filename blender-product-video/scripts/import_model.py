# Imports a model or 2D drawing into an empty scene at real scale, centred on the floor, and saves a .blend.
# usage: blender -b --factory-startup --python import_model.py -- <file> <out.blend> [unit: m|cm|mm|in]
# .step/.stp/.3mf go through text-to-cad (cad ... export to GLB, unit m); .pdf (vector) through pdftocairo; .dwg (2D only) through LibreDWG's dwg2SVG, unit mm by default.
# Prints the size in metres: check it against a real dimension before going on.
import bpy, sys, os, re, subprocess
from mathutils import Vector
src, out, *rest = sys.argv[sys.argv.index('--') + 1:]
ext0 = os.path.splitext(src)[1].lower()
if ext0 in ('.step', '.stp', '.3mf'):  # exact CAD: text-to-cad meshes it into a metre-scaled GLB, parts and names kept
    glb = os.path.splitext(os.path.abspath(out))[0] + '.glb'
    try:
        r = subprocess.run(['cad', 'threemf' if ext0 == '.3mf' else 'step', 'export', src, glb, '--tolerance', '0.05'], capture_output=True, text=True)
    except FileNotFoundError:
        sys.exit("ERR per STEP e 3MF serve text-to-cad (comando cad), oppure chiedi un export GLB dal CAD")
    if r.returncode: sys.exit("ERR cad export: " + (r.stderr or r.stdout)[-400:])
    src, rest = glb, ['m']
elif ext0 == '.pdf':  # vector PDF page 1 -> SVG; PDF points are 1/72 in
    svg = os.path.splitext(os.path.abspath(out))[0] + '.svg'
    try:
        subprocess.run(['pdftocairo', '-svg', '-f', '1', '-l', '1', src, svg], check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        sys.exit("ERR per i PDF serve poppler (brew install poppler), oppure chiedi un SVG")
    src = svg
unit = rest[0] if rest else ('mm' if src.lower().endswith('.dwg') else 'm')
scale = {'m': 1, 'cm': 0.01, 'mm': 0.001, 'in': 0.0254}[unit]
if ext0 == '.pdf': scale *= 72 / 25.4  # Blender reads pdftocairo's pt-sized SVG this much too small; 1:1 on paper -> real size
if src.lower().endswith('.dwg'):
    try:
        svg = subprocess.run(['dwg2SVG', src], capture_output=True, text=True).stdout
    except FileNotFoundError:
        sys.exit("ERR serve LibreDWG per i DWG: brew install libredwg")
    vb = re.search(r'viewBox="\S+ \S+ (\S+) (\S+)"', svg)
    w, h = (float(vb.group(1)), float(vb.group(2))) if vb else (0, 0)
    if not (0 < w < 1e9 and 0 < h < 1e9) or '<path' not in svg and '<circle' not in svg:
        sys.exit("ERR DWG senza geometria 2D leggibile (3D, vuoto o versione non supportata): chiedi un export DXF/SVG/PDF o STEP")
    # dwg2SVG writes width="100%": give the SVG real units so Blender's importer scales it, then don't scale again
    mm = scale * 1000  # always mm: Blender's SVG importer mis-scales cm
    svg = svg.replace('width="100%" height="100%"', f'width="{w * mm}mm" height="{h * mm}mm"', 1)
    src = os.path.splitext(os.path.abspath(out))[0] + '.svg'
    open(src, 'w').write(svg)
    scale = 1
bpy.ops.wm.read_factory_settings(use_empty=True)
ext = os.path.splitext(src)[1].lower()
imp = {'.glb': bpy.ops.import_scene.gltf, '.gltf': bpy.ops.import_scene.gltf, '.fbx': bpy.ops.import_scene.fbx,
       '.obj': bpy.ops.wm.obj_import, '.stl': bpy.ops.wm.stl_import, '.ply': bpy.ops.wm.ply_import,
       '.usd': bpy.ops.wm.usd_import, '.usdz': bpy.ops.wm.usd_import, '.usdc': bpy.ops.wm.usd_import,
       '.abc': bpy.ops.wm.alembic_import, '.svg': bpy.ops.import_curve.svg,
       '.blend': lambda filepath: bpy.ops.wm.open_mainfile(filepath=filepath)}.get(ext)
if not imp:
    sys.exit(f"ERR formato {ext} non importabile: esportalo come STEP o GLB (3D) o SVG/PDF (2D) dal CAD")
imp(filepath=os.path.abspath(src))
root = bpy.data.objects.new("PRODUCT", None)
bpy.context.scene.collection.objects.link(root)
for o in bpy.context.scene.objects:
    if o is not root and o.parent is None:
        o.parent = root
root.scale = (scale,) * 3
bpy.context.view_layer.update()
pts = [o.matrix_world @ Vector(c) for o in bpy.context.scene.objects if o.type in {'MESH', 'CURVE'} for c in o.bound_box]
if not pts:
    sys.exit("ERR nessuna geometria importata")
lo = Vector(min(p[i] for p in pts) for i in range(3)); hi = Vector(max(p[i] for p in pts) for i in range(3))
root.location = Vector((-(lo.x + hi.x) / 2, -(lo.y + hi.y) / 2, -lo.z))
size = hi - lo
print(f"SIZE_M {size.x:.3f} x {size.y:.3f} x {size.z:.3f}  objects={len(bpy.context.scene.objects) - 1}")
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(out))
