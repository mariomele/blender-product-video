# Generic demo product: electric motor + centrifugal pump on a base plate. Real scale (m).
# usage: blender -b --factory-startup --python build_pump.py -- <env: nero|limbo|capannone> <out.blend>
import bpy, sys, math
from mathutils import Vector
env, out = sys.argv[sys.argv.index('--') + 1:][:2]
bpy.ops.wm.read_factory_settings(use_empty=True)
s = bpy.context.scene; s.render.engine = 'CYCLES'; s.render.fps = 24
s.render.resolution_x, s.render.resolution_y = 1920, 1080; s.frame_start, s.frame_end = 1, 120
s.view_settings.view_transform = 'AgX'; s.view_settings.look = 'AgX - Punchy'  # keeps brand-like yellows saturated

def mat(name, color, metal=0.0, rough=0.4, coat=0.0, aniso=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough; b.inputs["Coat Weight"].default_value = coat
    b.inputs["Anisotropic"].default_value = aniso
    return m
YELLOW = mat("Verniciato giallo RAL 1003", (0.95, 0.42, 0.0), rough=0.32, coat=0.6)
GRAY = mat("Verniciato grigio RAL 7016", (0.035, 0.04, 0.045), rough=0.45, coat=0.3)
STEEL = mat("Inox spazzolato", (0.75, 0.75, 0.75), metal=1, rough=0.28, aniso=0.6)
ZINC = mat("Zincato", (0.6, 0.62, 0.64), metal=1, rough=0.4)
RUBBER = mat("Gomma", (0.02, 0.02, 0.02), rough=0.85)

parts = {}
def add(kind, name, m, loc, rot=(0, 0, 0), **kw):
    getattr(bpy.ops.mesh, f"primitive_{kind}_add")(location=loc, rotation=rot, **kw)
    o = bpy.context.object; o.name = name; o.data.materials.append(m)
    bpy.ops.object.shade_auto_smooth() if hasattr(bpy.ops.object, "shade_auto_smooth") else None
    parts.setdefault(name.split('.')[0], []).append(o); return o
def bevel(o, w=0.004):
    b = o.modifiers.new("Bevel", 'BEVEL'); b.width = w; b.segments = 3; b.limit_method = 'ANGLE'

X = (0, math.pi / 2, 0)
# base plate
base = add("cube", "Base", GRAY, (0, 0, 0.02), size=1); base.scale = (0.95, 0.36, 0.04); bevel(base, 0.006)
for x in (-0.4, 0.4):
    for y in (-0.14, 0.14):
        add("cylinder", "Bullone", ZINC, (x, y, 0.045), radius=0.012, depth=0.015, vertices=6)
# motor (x < 0): body with cooling fins, end caps, terminal box, feet
add("cylinder", "Motore", GRAY, (-0.22, 0, 0.2), X, radius=0.12, depth=0.36, vertices=64)
for i in range(14):
    a = i * 2 * math.pi / 14
    f = add("cube", "Motore.aletta", GRAY, (-0.22, 0.125 * math.cos(a), 0.2 + 0.125 * math.sin(a)), (a, 0, 0), size=1)
    f.scale = (0.33, 0.012, 0.03)
add("cylinder", "Motore.coperchio", GRAY, (-0.42, 0, 0.2), X, radius=0.115, depth=0.05, vertices=64)
fan = add("cylinder", "Motore.ventola", STEEL, (-0.455, 0, 0.2), X, radius=0.1, depth=0.02, vertices=48)
box = add("cube", "Motore.morsettiera", GRAY, (-0.2, 0, 0.345), size=1); box.scale = (0.12, 0.1, 0.06); bevel(box)
for x in (-0.33, -0.1):
    foot = add("cube", "Motore.piede", GRAY, (x, 0, 0.07), size=1); foot.scale = (0.05, 0.26, 0.06); bevel(foot)
# coupling + shaft
add("cylinder", "Giunto", STEEL, (0.0, 0, 0.2), X, radius=0.05, depth=0.06, vertices=48)
add("cylinder", "Giunto.gomma", RUBBER, (0.04, 0, 0.2), X, radius=0.045, depth=0.02, vertices=48)
# pump (x > 0): volute, suction and discharge flanges, support
vol = add("cylinder", "Pompa", YELLOW, (0.26, 0, 0.22), X, radius=0.15, depth=0.12, vertices=96); bevel(vol, 0.01)
add("cylinder", "Pompa.coperchio", YELLOW, (0.335, 0, 0.22), X, radius=0.12, depth=0.04, vertices=96)
add("cylinder", "Pompa.aspirazione", YELLOW, (0.41, 0, 0.22), X, radius=0.055, depth=0.12, vertices=48)
add("cylinder", "Pompa.flangia_asp", STEEL, (0.475, 0, 0.22), X, radius=0.085, depth=0.02, vertices=48)
add("cylinder", "Pompa.mandata", YELLOW, (0.26, 0, 0.4), radius=0.045, depth=0.12, vertices=48)
add("cylinder", "Pompa.flangia_mand", STEEL, (0.26, 0, 0.465), radius=0.075, depth=0.02, vertices=48)
for k in range(8):
    a = k * math.pi / 4
    add("cylinder", "Pompa.vite", ZINC, (0.487, 0.068 * math.cos(a), 0.22 + 0.068 * math.sin(a)), X, radius=0.007, depth=0.012, vertices=6)
sup = add("cube", "Pompa.supporto", GRAY, (0.26, 0, 0.065), size=1); sup.scale = (0.12, 0.2, 0.05); bevel(sup)
plate = add("cube", "Pompa.targa", STEEL, (0.26, -0.151, 0.2), size=1); plate.scale = (0.07, 0.002, 0.04)

# exploded view: motor group slides back, pump group forward (frames 60-100)
def group(prefixes):
    e = bpy.data.objects.new("G_" + prefixes[0], None); s.collection.objects.link(e)
    for p in prefixes:
        for o in parts.get(p, []): o.parent = e
    return e
gm, gp = group(["Motore"]), group(["Pompa"])
for e, dx in ((gm, -0.18), (gp, 0.16)):
    e.keyframe_insert("location", frame=60); e.location.x += dx; e.location.z += 0.06; e.keyframe_insert("location", frame=100)

# camera: slow orbit + push-in
piv = bpy.data.objects.new("Pivot", None); s.collection.objects.link(piv); piv.location = (0, 0, 0.2)
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam")); s.collection.objects.link(cam); s.camera = cam
cam.parent = piv; cam.data.lens = 50; cam.data.dof.use_dof = True; cam.data.dof.focus_object = piv; cam.data.dof.aperture_fstop = 5.6
cam.constraints.new('TRACK_TO').target = piv
cam.location = (0.9, -2.0, 0.55); cam.keyframe_insert("location", frame=1)
cam.location = (0.6, -1.5, 0.45); cam.keyframe_insert("location", frame=120)
piv.rotation_euler = (0, 0, math.radians(-25)); piv.keyframe_insert("rotation_euler", frame=1)
piv.rotation_euler = (0, 0, math.radians(35)); piv.keyframe_insert("rotation_euler", frame=120)

# environments
w = bpy.data.worlds.new("W"); s.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]
def light(name, loc, energy, size, color=(1, 1, 1)):
    l = bpy.data.lights.new(name, 'AREA'); l.energy = energy; l.size = size; l.color = color
    o = bpy.data.objects.new(name, l); o.location = loc; s.collection.objects.link(o)
    o.constraints.new('TRACK_TO').target = piv
def limbo(color, rough):
    # floor that curves up into the backdrop: no horizon line
    bpy.ops.mesh.primitive_plane_add(size=1); o = bpy.context.object; me = o.data
    import bmesh; bm = bmesh.new(); prev = None; R = 1.2; rows = []
    pts = [(y, 0.0) for y in (-4.0, -2.0, 0.0, 1.0)] + [(1.0 + R * math.sin(t), R - R * math.cos(t)) for t in [i * math.pi / 2 / 12 for i in range(1, 13)]] + [(1.0 + R, 4.0)]
    for y, z in pts:
        rows.append((bm.verts.new((-6, y, z)), bm.verts.new((6, y, z))))
    for (a, b), (c, d) in zip(rows, rows[1:]): bm.faces.new((a, b, d, c))
    bm.to_mesh(me); bm.free(); o.data.materials.append(mat("Limbo", color, rough=rough))
    for p in o.data.polygons: p.use_smooth = True
if env == "nero":
    bg.inputs[1].default_value = 0.0; limbo((0.003, 0.003, 0.0035), 0.22)
    light("Key", (1.4, -1.5, 1.2), 160, 0.9); light("Rim", (-1.0, 0.9, 0.9), 180, 0.5); light("Fill", (-1.6, -1.4, 0.6), 30, 1.5); light("Top", (0, -0.2, 1.6), 60, 0.8)
elif env == "limbo":
    bg.inputs[0].default_value = (1, 1, 1, 1); bg.inputs[1].default_value = 0.2; limbo((0.6, 0.72, 0.72), 0.6)
    light("Key", (1.6, -1.6, 2.0), 130, 2.5); light("Fill", (-2, -1.4, 1.2), 50, 3); light("Top", (0, 0, 2.5), 60, 3)
else:  # capannone: concrete floor, back wall, high windows, warm practicals
    bg.inputs[0].default_value = (0.55, 0.65, 0.8, 1); bg.inputs[1].default_value = 0.25
    bpy.ops.mesh.primitive_plane_add(size=20); fl = bpy.context.object
    cm = mat("Cemento", (0.32, 0.31, 0.3), rough=0.75); fl.data.materials.append(cm)
    n = cm.node_tree.nodes; noise = n.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 6
    ramp = n.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].color = (0.08, 0.075, 0.07, 1); ramp.color_ramp.elements[1].color = (0.16, 0.15, 0.14, 1)
    cm.node_tree.links.new(noise.outputs["Fac"], ramp.inputs["Fac"]); cm.node_tree.links.new(ramp.outputs["Color"], n["Principled BSDF"].inputs["Base Color"])
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 2.4, 3), rotation=(math.pi / 2, 0, 0)); wall = bpy.context.object
    wall.scale = (20, 6, 1); wall.data.materials.append(mat("Parete", (0.18, 0.2, 0.22), rough=0.8))
    for x in (-3, 0, 3):
        bpy.ops.mesh.primitive_plane_add(size=1, location=(x, 2.35, 2.2), rotation=(math.pi / 2, 0, 0)); win = bpy.context.object; win.scale = (2, 1.2, 1)
        em = bpy.data.materials.new("Finestra"); em.use_nodes = True; em.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 6
        em.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (0.8, 0.9, 1, 1); win.data.materials.append(em)
    steel = mat("Acciaio strutture", (0.05, 0.12, 0.2), metal=0.6, rough=0.5)
    for x in (-2.2, 0.0, 2.2):  # I-beam columns
        for sx, sy, ox in ((0.3, 0.02, 0), (0.02, 0.25, 0)):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 2.0, 3)); c = bpy.context.object; c.scale = (sx, sy if sy > 0.1 else 0.3, 6) if False else (sx, sy + (0.28 if sx > 0.1 else 0), 6)
            c.data.materials.append(steel)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0.75, 0.002)); st = bpy.context.object; st.scale = (20, 0.1, 1)
    st.data.materials.append(mat("Striscia sicurezza", (0.9, 0.6, 0.0), rough=0.5))
    for x in (-1.4, 1.5):  # pallets with boxes
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 1.45, 0.07)); p_ = bpy.context.object; p_.scale = (1.0, 0.8, 0.14); p_.data.materials.append(mat("Pallet", (0.3, 0.2, 0.1), rough=0.9))
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 1.45, 0.4)); b_ = bpy.context.object; b_.scale = (0.8, 0.6, 0.5); b_.data.materials.append(mat("Cartone", (0.35, 0.24, 0.13), rough=0.9))
    light("Sun", (2.5, 2.0, 3.0), 250, 2.5, (0.85, 0.92, 1)); light("Key", (1.6, -1.6, 1.6), 160, 1.5, (1, 0.9, 0.78)); light("Rim", (-1.2, 1.4, 1.4), 200, 0.8)
    s.world.node_tree.nodes["Background"].inputs[1].default_value = 0.12
bpy.ops.wm.save_as_mainfile(filepath=out)
print("BUILT", env, len(bpy.data.objects))
