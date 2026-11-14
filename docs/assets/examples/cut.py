# Cutaway still of the demo pump: hollow bodies, add internals, quarter-cut with red section caps. -- frame out.jpg
import bpy, sys, math
a = sys.argv[sys.argv.index('--') + 1:]
s = bpy.context.scene; s.frame_set(int(a[0]))
O = bpy.data.objects

def mat(name, rgb, metal=0.0, rough=0.4):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    return m

def cyl(name, r, x0, x1, y=0, z=0.2, m=None, axis='X', hide=False):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=r, depth=x1 - x0)
    o = bpy.context.object; o.name = name
    if axis == 'X': o.rotation_euler = (0, math.pi / 2, 0); o.location = ((x0 + x1) / 2, y, z)
    else: o.location = (y, 0, (x0 + x1) / 2)  # vertical: y arg is x position
    if m: o.data.materials.append(m)
    o.hide_render = hide
    return o

def boolean(target, cutter, transfer=True):
    md = target.modifiers.new('cut_' + cutter.name, 'BOOLEAN'); md.operation = 'DIFFERENCE'; md.solver = 'EXACT'
    md.object = cutter
    if transfer: md.material_mode = 'TRANSFER'

CAP = mat('Sezione', (0.45, 0.02, 0.015), 0, 0.5)
STEEL = mat('Acciaio albero', (0.75, 0.75, 0.76), 1, 0.25)
CU = mat('Rame avvolgimenti', (0.80, 0.36, 0.17), 1, 0.3)
ROT = mat('Lamierini rotore', (0.25, 0.26, 0.28), 1, 0.35)
BRASS = mat('Bronzo girante', (0.78, 0.55, 0.25), 1, 0.3)

# hollow the shells (inner wall keeps the body's own paint)
for tgt, r, x0, x1, z in [('Motore', 0.105, -0.39, -0.05, 0.2), ('Pompa', 0.13, 0.215, 0.305, 0.22),
                          ('Pompa.coperchio', 0.1, 0.32, 0.35, 0.22), ('Pompa.aspirazione', 0.042, 0.33, 0.5, 0.22)]:
    t = O[tgt]; boolean(t, cyl('hollow_' + tgt, r, x0, x1, z=z, m=t.data.materials[0], hide=True))
t = O['Pompa.mandata']; boolean(t, cyl('hollow_mand', 0.032, 0.25, 0.49, y=0.26, m=t.data.materials[0], axis='Z', hide=True))

# internals
cyl('Albero', 0.018, -0.44, 0.31, m=STEEL)
cyl('Rotore', 0.062, -0.34, -0.10, m=ROT)
st = cyl('Statore', 0.099, -0.33, -0.11, m=CU); boolean(st, cyl('stat_in', 0.072, -0.34, -0.10, m=CU, hide=True))
cyl('Girante.disco', 0.105, 0.232, 0.244, m=BRASS)
for i in range(7):
    bpy.ops.mesh.primitive_cube_add(size=1); b = bpy.context.object; b.name = f'Girante.pala{i}'
    b.scale = (0.03, 0.006, 0.075); ang = i * 2 * math.pi / 7
    b.location = (0.26, 0.06 * math.sin(ang), 0.2 + 0.06 * math.cos(ang))
    b.rotation_euler = (-ang + math.radians(25), 0, 0); b.data.materials.append(BRASS)

# quarter cut toward the camera: y < 0 and above the shaft axis
bpy.ops.mesh.primitive_cube_add(size=1); c = bpy.context.object; c.name = 'Cutter'
c.scale = (1.2, 0.5, 0.6); c.location = (0, -0.25, 0.2 + 0.3); c.data.materials.append(CAP); c.hide_render = True
skip = ('Base', 'Bullone', 'Plane', 'Motore.piede', 'Pompa.supporto', 'Pompa.vite', 'Pompa.targa', 'Albero', 'Rotore', 'Girante')
for o in list(s.objects):
    if o.type == 'MESH' and not o.hide_render and not o.name.startswith(skip): boolean(o, c)

s.render.resolution_percentage = 80; s.cycles.samples = 128; s.cycles.use_denoising = True; s.cycles.device = 'GPU'
s.render.image_settings.file_format = 'JPEG'; s.render.image_settings.quality = 90; s.render.filepath = a[1]
bpy.ops.render.render(write_still=True)
