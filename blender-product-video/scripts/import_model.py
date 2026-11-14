# Imports a model or 2D drawing into an empty scene at real scale, centred on the floor, and saves a .blend.
# usage: blender -b --factory-startup --python import_model.py -- <file> <out.blend> [unit: m|cm|mm|in]
# Prints the size in metres: check it against a real dimension before going on.
import bpy, sys, os
from mathutils import Vector
src, out, *rest = sys.argv[sys.argv.index('--') + 1:]
scale = {'m': 1, 'cm': 0.01, 'mm': 0.001, 'in': 0.0254}[rest[0] if rest else 'm']
bpy.ops.wm.read_factory_settings(use_empty=True)
ext = os.path.splitext(src)[1].lower()
imp = {'.glb': bpy.ops.import_scene.gltf, '.gltf': bpy.ops.import_scene.gltf, '.fbx': bpy.ops.import_scene.fbx,
       '.obj': bpy.ops.wm.obj_import, '.stl': bpy.ops.wm.stl_import, '.ply': bpy.ops.wm.ply_import,
       '.usd': bpy.ops.wm.usd_import, '.usdz': bpy.ops.wm.usd_import, '.usdc': bpy.ops.wm.usd_import,
       '.abc': bpy.ops.wm.alembic_import, '.svg': bpy.ops.import_curve.svg}.get(ext)
if not imp:
    sys.exit(f"ERR formato {ext} non importabile: esportalo come GLB/OBJ/STL (3D) o SVG (2D) dal CAD")
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
