# Generic demo product: 6-axis industrial robot arm with motors, strain-wave gearboxes, bearings, cables and a gripper. Real scale (m).
# usage: blender -b --factory-startup --python build_robot.py -- <env: nero|limbo|capannone|laboratorio|officina|logistica> <out.blend>
# Animation: 1-50 the arm moves, 60-100 it explodes joint by joint (motors slide out), 100-120 hold.
import bpy, bmesh, sys, math
env, out = sys.argv[sys.argv.index('--') + 1:][:2]
bpy.ops.wm.read_factory_settings(use_empty=True)
s = bpy.context.scene; s.render.engine = 'CYCLES'; s.render.fps = 24
s.render.resolution_x, s.render.resolution_y = 1920, 1080; s.frame_start, s.frame_end = 1, 120
s.view_settings.view_transform = 'AgX'; s.view_settings.look = 'AgX - Punchy'
PI = math.pi

def mat(name, color, metal=0.0, rough=0.4, coat=0.0, aniso=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough; b.inputs["Coat Weight"].default_value = coat
    b.inputs["Anisotropic"].default_value = aniso
    return m
ORANGE = mat("Verniciato arancio robot", (0.95, 0.36, 0.0), rough=0.3, coat=0.7)
GRAY = mat("Verniciato grigio RAL 7016", (0.03, 0.034, 0.04), rough=0.42, coat=0.3)
ALU = mat("Alluminio anodizzato", (0.55, 0.56, 0.58), metal=1, rough=0.35)
STEEL = mat("Acciaio spazzolato", (0.75, 0.75, 0.76), metal=1, rough=0.25, aniso=0.6)
ZINC = mat("Zincato", (0.6, 0.62, 0.64), metal=1, rough=0.4)
RUBBER = mat("Guaina cavi", (0.015, 0.015, 0.017), rough=0.7)
BLUE = mat("Connettore", (0.02, 0.12, 0.35), rough=0.4)
# internals, seen only in the cutaway
CU = mat("Rame avvolgimenti", (0.80, 0.36, 0.17), metal=1, rough=0.3)
LAM = mat("Lamierini", (0.22, 0.23, 0.25), metal=1, rough=0.35)
BRASS = mat("Bronzo", (0.78, 0.55, 0.25), metal=1, rough=0.3)

def obj(o, name, m, parent):
    o.name = name; o.data.materials.append(m); o.parent = parent
    return o
def autosmooth(o):
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    try: bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
    except Exception: pass
    o.select_set(False)
def bevel(o, w=0.006, seg=3):
    b = o.modifiers.new("Bevel", 'BEVEL'); b.width = w; b.segments = seg; b.limit_method = 'ANGLE'
def cyl(name, m, parent, r, depth, loc=(0, 0, 0), axis='Z', verts=64, bev=0.0):
    rot = {'Z': (0, 0, 0), 'Y': (PI / 2, 0, 0), 'X': (0, PI / 2, 0)}[axis]
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, vertices=verts)
    o = obj(bpy.context.object, name, m, parent); o.rotation_euler = rot; o.location = loc
    autosmooth(o)
    if bev: bevel(o, bev)
    return o
def box(name, m, parent, size, loc=(0, 0, 0), bev=0.01, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = obj(bpy.context.object, name, m, parent); o.scale = size; o.location = loc; o.rotation_euler = rot
    if bev: bevel(o, bev)
    return o
def torus(name, m, parent, R, r, loc=(0, 0, 0), axis='Z'):
    rot = {'Z': (0, 0, 0), 'Y': (PI / 2, 0, 0), 'X': (0, PI / 2, 0)}[axis]
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=64, minor_segments=16)
    o = obj(bpy.context.object, name, m, parent); o.rotation_euler = rot; o.location = loc; return o

def link(name, parent, r1, r2, L, t, loc=(0, 0, 0)):
    # classic robot link: 2D hull of two circles (bottom r1, top r2 at height L), extruded t along Y
    pts = [(r1 * math.cos(a), r1 * math.sin(a)) for a in [i * 2 * PI / 48 for i in range(48)]]
    pts += [(r2 * math.cos(a), L + r2 * math.sin(a)) for a in [i * 2 * PI / 48 for i in range(48)]]
    pts = sorted(set(pts))
    def half(ps):
        h = []
        for p in ps:
            while len(h) >= 2 and (h[-1][0] - h[-2][0]) * (p[1] - h[-2][1]) - (h[-1][1] - h[-2][1]) * (p[0] - h[-2][0]) <= 0: h.pop()
            h.append(p)
        return h
    hull = half(pts)[:-1] + half(pts[::-1])[:-1]
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    f = bm.faces.new([bm.verts.new((x, -t / 2, z)) for x, z in hull])
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    bmesh.ops.translate(bm, verts=[v for v in ext['geom'] if isinstance(v, bmesh.types.BMVert)], vec=(0, t, 0))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); s.collection.objects.link(o)
    o.data.materials.append(ORANGE); o.parent = parent; o.location = loc
    bevel(o, 0.022, 5); autosmooth(o); return o

def empty(name, parent, loc, rot=(0, 0, 0)):
    e = bpy.data.objects.new(name, None); s.collection.objects.link(e); e.parent = parent; e.location = loc; e.rotation_euler = rot
    e.empty_display_size = 0.1; return e

def bolts(name, parent, R, n, r, depth, loc, axis):
    for k in range(n):
        a = 2 * PI * k / n
        if axis == 'Y': p = (loc[0] + R * math.cos(a), loc[1], loc[2] + R * math.sin(a))
        elif axis == 'X': p = (loc[0], loc[1] + R * math.cos(a), loc[2] + R * math.sin(a))
        else: p = (loc[0] + R * math.cos(a), loc[1] + R * math.sin(a), loc[2])
        cyl(f"{name}.vite{k}", ZINC, parent, r, depth, p, axis, verts=6)

MOTORS = []
def motor(name, parent, loc, axis, r, L, sign=-1):
    # servo motor sticking out of a joint: body with fins, end cap, encoder, connector
    g = empty(name, parent, loc); MOTORS.append((g, axis, sign))
    o = {'Y': (0, sign, 0), 'X': (sign, 0, 0), 'Z': (0, 0, sign)}[axis]
    at = lambda d: (o[0] * d, o[1] * d, o[2] * d)
    cyl(name + ".corpo", GRAY, g, r, L, at(L / 2), axis, bev=0.004)
    for k in range(12):
        a = 2 * PI * k / 12
        if axis == 'Y': p, rr = (r * math.cos(a), L * 0.5 * sign, r * math.sin(a)), (0, -a, 0)
        elif axis == 'X': p, rr = (L * 0.5 * sign, r * math.cos(a), r * math.sin(a)), (a, 0, 0)
        else: p, rr = (r * math.cos(a), r * math.sin(a), L * 0.5 * sign), (0, 0, a)
        f = box(f"{name}.aletta{k}", GRAY, g, {'Y': (0.012, L * 0.8, 0.02), 'X': (L * 0.8, 0.012, 0.02), 'Z': (0.02, 0.012, L * 0.8)}[axis], p, 0.002, rr)
        if axis == 'Y': f.scale = (0.02, L * 0.8, 0.012)
    cyl(name + ".coperchio", ALU, g, r * 0.92, 0.03, at(L + 0.015), axis, bev=0.004)
    cyl(name + ".encoder", GRAY, g, r * 0.6, 0.04, at(L + 0.05), axis, bev=0.004)
    cyl(name + ".rame", CU, g, r * 0.78, L * 0.8, at(L / 2), axis)  # windings, rotor and shaft: visible only when cut
    cyl(name + ".rotore", LAM, g, r * 0.4, L * 0.82, at(L / 2), axis)
    cyl(name + ".albero", STEEL, g, r * 0.14, L * 1.15, at(L / 2), axis)
    cb = box(name + ".connettore", BLUE, g, (0.05, 0.05, 0.035), at(L * 0.65), 0.004)
    cb.location[2] += r + 0.012 if axis != 'Z' else 0
    return g

def joint_internals(name, parent, axis, R, width):
    # inside every joint: shaft, motor windings, strain-wave gearbox (ring with teeth), crossed-roller bearing
    cyl(name + ".albero", STEEL, parent, R * 0.16, width * 1.05, (0, 0, 0), axis)
    cyl(name + ".statore", CU, parent, R * 0.62, width * 0.32, {'Y': (0, -width * 0.22, 0), 'X': (-width * 0.22, 0, 0), 'Z': (0, 0, -width * 0.22)}[axis], axis)
    cyl(name + ".rotore", LAM, parent, R * 0.42, width * 0.36, {'Y': (0, -width * 0.22, 0), 'X': (-width * 0.22, 0, 0), 'Z': (0, 0, -width * 0.22)}[axis], axis)
    off = {'Y': (0, width * 0.16, 0), 'X': (width * 0.16, 0, 0), 'Z': (0, 0, width * 0.16)}[axis]
    cyl(name + ".flexspline", STEEL, parent, R * 0.6, width * 0.14, off, axis)
    n = 40
    for k in range(n):
        a = 2 * PI * k / n; rr = R * 0.66
        if axis == 'Y': p, rot, sz = (rr * math.cos(a), off[1], rr * math.sin(a)), (0, -a, 0), (0.02 * R / 0.15, width * 0.14, 0.012 * R / 0.15)
        elif axis == 'X': p, rot, sz = (off[0], rr * math.cos(a), rr * math.sin(a)), (a, 0, 0), (width * 0.14, 0.012 * R / 0.15, 0.02 * R / 0.15)
        else: p, rot, sz = (rr * math.cos(a), rr * math.sin(a), off[2]), (0, 0, a), (0.02 * R / 0.15, 0.012 * R / 0.15, width * 0.14)
        box(f"{name}.dente{k}", BRASS, parent, sz, p, 0, rot)
    boff = {'Y': (0, width * 0.36, 0), 'X': (width * 0.36, 0, 0), 'Z': (0, 0, width * 0.36)}[axis]
    torus(name + ".cuscinetto_est", STEEL, parent, R * 0.8, R * 0.05, boff, axis)
    torus(name + ".cuscinetto_int", STEEL, parent, R * 0.58, R * 0.05, boff, axis)
    for k in range(16):
        a = 2 * PI * k / 16; rr = R * 0.69
        bpy.ops.mesh.primitive_uv_sphere_add(radius=R * 0.07, segments=16, ring_count=8)
        sph = obj(bpy.context.object, f"{name}.sfera{k}", STEEL, parent)
        sph.location = {'Y': (rr * math.cos(a), boff[1], rr * math.sin(a)), 'X': (boff[0], rr * math.cos(a), rr * math.sin(a)), 'Z': (rr * math.cos(a), rr * math.sin(a), boff[2])}[axis]

def cable(name, parent, pts, r=0.016):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = r; cu.bevel_resolution = 4
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts): bp.co = p; bp.handle_left_type = bp.handle_right_type = 'AUTO'
    o = bpy.data.objects.new(name, cu); s.collection.objects.link(o); o.parent = parent; o.data.materials.append(RUBBER); return o

ROOT = empty("Robot", None, (0, 0, 0))
# base: floor plate with anchors, fixed column
cyl("Base.piastra", GRAY, ROOT, 0.34, 0.04, (0, 0, 0.02), bev=0.006)
bolts("Base", ROOT, 0.29, 8, 0.018, 0.025, (0, 0, 0.045), 'Z')
cyl("Base.colonna", ORANGE, ROOT, 0.24, 0.14, (0, 0, 0.11), bev=0.012)
cyl("Base.anello", ALU, ROOT, 0.25, 0.02, (0, 0, 0.19), bev=0.004)
box("Base.targa", ALU, ROOT, (0.12, 0.002, 0.05), (0, -0.241, 0.11), 0.001)
cable("Base.cavo", ROOT, [(-0.6, -0.15, 0.015), (-0.4, -0.12, 0.02), (-0.27, -0.06, 0.08)], 0.022)

J1 = empty("J1", ROOT, (0, 0, 0.2))
cyl("J1.carter", ORANGE, J1, 0.23, 0.26, (0, 0, 0.13), bev=0.02)
box("J1.spalla", ORANGE, J1, (0.36, 0.34, 0.2), (0.08, 0, 0.3), 0.06)
joint_internals("J1.int", empty("J1.centro", J1, (0, 0, 0.13)), 'Z', 0.2, 0.24)
motor("J1.motore", J1, (-0.17, 0, 0.18), 'X', 0.075, 0.2)

J2 = empty("J2", J1, (0.14, 0, 0.42))
cyl("J2.carter", ORANGE, J2, 0.19, 0.42, (0, 0, 0), 'Y', 96, 0.02)
cyl("J2.tappo", ALU, J2, 0.15, 0.02, (0, -0.215, 0), 'Y', 96, 0.004)
bolts("J2", J2, 0.125, 10, 0.011, 0.015, (0, -0.228, 0), 'Y')
joint_internals("J2.int", J2, 'Y', 0.17, 0.4)
motor("J2.motore", J2, (0, -0.225, 0), 'Y', 0.085, 0.24)
link("J2.braccio", J2, 0.17, 0.13, 0.78, 0.22, (0, 0.06, 0))
cable("J2.cavo", J2, [(-0.1, 0.2, 0.1), (-0.19, 0.19, 0.4), (-0.14, 0.18, 0.72)])
for z in (0.25, 0.55):
    box(f"J2.fascetta{int(z * 100)}", GRAY, J2, (0.05, 0.03, 0.03), (-0.17 + 0.03 * z, 0.185, z), 0.004)

J3 = empty("J3", J2, (0, 0, 0.78))
cyl("J3.carter", ORANGE, J3, 0.15, 0.36, (0, 0, 0), 'Y', 96, 0.018)
cyl("J3.tappo", ALU, J3, 0.11, 0.02, (0, -0.185, 0), 'Y', 96, 0.004)
bolts("J3", J3, 0.09, 8, 0.009, 0.014, (0, -0.196, 0), 'Y')
joint_internals("J3.int", J3, 'Y', 0.13, 0.32)
motor("J3.motore", J3, (0, -0.19, 0), 'Y', 0.07, 0.2)
box("J3.avambraccio", ORANGE, J3, (0.42, 0.24, 0.2), (0.02, 0.04, 0.09), 0.07)
motor("J4.motore", J3, (-0.19, 0.04, 0.09), 'X', 0.06, 0.18)

J4 = empty("J4", J3, (0.23, 0.04, 0.09))
cyl("J4.tubo", ORANGE, J4, 0.085, 0.46, (0.23, 0, 0), 'X', 64, 0.012)
cyl("J4.flangia", ALU, J4, 0.095, 0.03, (0.015, 0, 0), 'X', 64, 0.004)
joint_internals("J4.int", J4, 'X', 0.08, 0.16)
cable("J4.cavo", J3, [(-0.12, 0.17, 0.17), (0.1, 0.17, 0.2), (0.4, 0.12, 0.17)], 0.012)

J5 = empty("J5", J4, (0.52, 0, 0))
box("J5.forcella", ORANGE, J5, (0.12, 0.2, 0.15), (-0.03, 0, 0), 0.05)
cyl("J5.carter", ORANGE, J5, 0.075, 0.2, (0.02, 0, 0), 'Y', 64, 0.012)
cyl("J5.tappo", ALU, J5, 0.055, 0.015, (0.02, -0.105, 0), 'Y', 64, 0.003)
motor("J5.motore", J5, (0.02, 0.105, 0), 'Y', 0.045, 0.1, 1)

J6 = empty("J6", J5, (0.1, 0, 0))
cyl("J6.polso", ORANGE, J6, 0.06, 0.08, (0.04, 0, 0), 'X', 64, 0.01)
cyl("J6.flangia", STEEL, J6, 0.058, 0.02, (0.09, 0, 0), 'X', 64, 0.003)
bolts("J6", J6, 0.044, 6, 0.006, 0.01, (0.1, 0, 0), 'X')
# two-finger gripper
G = empty("Pinza", J6, (0.1, 0, 0))
box("Pinza.corpo", GRAY, G, (0.08, 0.17, 0.08), (0.04, 0, 0), 0.012)
for sgn in (-1, 1):
    box(f"Pinza.slitta{sgn}", ALU, G, (0.02, 0.05, 0.06), (0.09, sgn * 0.045, 0), 0.004)
    box(f"Pinza.dito{sgn}", STEEL, G, (0.11, 0.022, 0.05), (0.16, sgn * 0.045, 0), 0.006)
    box(f"Pinza.gommino{sgn}", RUBBER, G, (0.05, 0.006, 0.04), (0.19, sgn * 0.032, 0), 0.002)

# pose and animation (joint angles in degrees)
J = {"J1": (J1, 2), "J2": (J2, 1), "J3": (J3, 1), "J4": (J4, 0), "J5": (J5, 1), "J6": (J6, 0)}
def pose(frame, **deg):
    for k, (e, ax) in J.items():
        e.rotation_euler[ax] = math.radians(deg.get(k, 0)); e.keyframe_insert("rotation_euler", index=ax, frame=frame)
pose(1, J1=-35, J2=-8, J3=12, J4=0, J5=40, J6=0)
pose(50, J1=30, J2=12, J3=-6, J4=25, J5=55, J6=90)
pose(120, J1=30, J2=12, J3=-6, J4=25, J5=55, J6=90)
# exploded: every link moves away from its parent along the chain, motors slide out of their joints
for e, d in ((J1, (0, 0, 0.16)), (J2, (0, 0, 0.18)), (J3, (0, 0, 0.2)), (J4, (0.16, 0, 0)), (J5, (0.14, 0, 0)), (J6, (0.1, 0, 0)), (G, (0.08, 0, 0))):
    e.keyframe_insert("location", frame=60)
    e.location = [a + b for a, b in zip(e.location, d)]; e.keyframe_insert("location", frame=100)
for g, axis, sign in MOTORS:
    g.keyframe_insert("location", frame=60)
    i = "XYZ".index(axis); g.location[i] += 0.16 * sign; g.keyframe_insert("location", frame=100)
for a in bpy.data.actions:
    for fc in getattr(a, "fcurves", []):
        for kp in fc.keyframe_points: kp.interpolation = 'BEZIER'; kp.easing = 'EASE_IN_OUT'

# camera: slow orbit + push-in around the robot
piv = bpy.data.objects.new("Pivot", None); s.collection.objects.link(piv); piv.location = (0.35, 0, 0.85)
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam")); s.collection.objects.link(cam); s.camera = cam
cam.parent = piv; cam.data.lens = 40; cam.data.dof.use_dof = True; cam.data.dof.focus_object = piv; cam.data.dof.aperture_fstop = 8
cam.constraints.new('TRACK_TO').target = piv
cam.location = (1.9, -4.7, 0.6); cam.keyframe_insert("location", frame=1)
cam.location = (1.6, -4.2, 0.5); cam.keyframe_insert("location", frame=55)
cam.location = (2.3, -5.9, 0.9); cam.keyframe_insert("location", frame=100)  # pull back while it explodes
piv.keyframe_insert("location", frame=55); piv.location.z = 1.1; piv.keyframe_insert("location", frame=100)
piv.rotation_euler = (0, 0, math.radians(-20)); piv.keyframe_insert("rotation_euler", frame=1)
piv.rotation_euler = (0, 0, math.radians(20)); piv.keyframe_insert("rotation_euler", frame=120)

# environments (scaled for a ~1.8 m tall machine)
w = bpy.data.worlds.new("W"); s.world = w; w.use_nodes = True; bg = w.node_tree.nodes["Background"]
def light(name, loc, energy, size, color=(1, 1, 1)):
    l = bpy.data.lights.new(name, 'AREA'); l.energy = energy; l.size = size; l.color = color
    o = bpy.data.objects.new(name, l); o.location = loc; s.collection.objects.link(o)
    o.constraints.new('TRACK_TO').target = piv
def limbo(color, rough):
    # floor that curves up into the backdrop: no horizon line
    bpy.ops.mesh.primitive_plane_add(size=1); o = bpy.context.object; me = o.data
    bm = bmesh.new(); rows = []; R = 2.0
    pts = [(y, 0.0) for y in (-8.0, -4.0, 0.0, 1.8)] + [(1.8 + R * math.sin(t), R - R * math.cos(t)) for t in [i * PI / 2 / 14 for i in range(1, 15)]] + [(1.8 + R, 7.0)]
    for y, z in pts: rows.append((bm.verts.new((-10, y, z)), bm.verts.new((10, y, z))))
    for (a, b), (c, d) in zip(rows, rows[1:]): bm.faces.new((a, b, d, c))
    bm.to_mesh(me); bm.free(); o.data.materials.append(mat("Limbo", color, rough=rough))
    for p in o.data.polygons: p.use_smooth = True
if env == "nero":
    bg.inputs[1].default_value = 0.0; limbo((0.003, 0.003, 0.0035), 0.22)
    light("Key", (2.6, -2.8, 2.6), 650, 1.8); light("Rim", (-2.0, 1.8, 2.2), 800, 1.0); light("Fill", (-3.0, -2.6, 1.2), 120, 3.0); light("Top", (0.3, -0.3, 3.4), 260, 1.6)
elif env == "limbo":
    bg.inputs[0].default_value = (1, 1, 1, 1); bg.inputs[1].default_value = 0.2; limbo((0.6, 0.72, 0.72), 0.6)
    light("Key", (3.0, -3.0, 3.8), 520, 5); light("Fill", (-3.8, -2.6, 2.4), 200, 6); light("Top", (0, 0, 4.8), 240, 6)
elif env == "laboratorio":  # clean lab: white tiled floor, white walls with light strips, benches
    bg.inputs[0].default_value = (0.9, 0.95, 1, 1); bg.inputs[1].default_value = 0.3
    bpy.ops.mesh.primitive_plane_add(size=30); fl = bpy.context.object; fm = mat("Pavimento resina", (0.8, 0.82, 0.84), rough=0.25); fl.data.materials.append(fm)
    n = fm.node_tree.nodes; ck = n.new("ShaderNodeTexChecker"); ck.inputs["Scale"].default_value = 30
    ck.inputs["Color1"].default_value = (0.78, 0.8, 0.82, 1); ck.inputs["Color2"].default_value = (0.7, 0.72, 0.75, 1)
    fm.node_tree.links.new(ck.outputs["Color"], n["Principled BSDF"].inputs["Base Color"])
    wm = mat("Pannelli bianchi", (0.85, 0.87, 0.9), rough=0.5)
    for loc, rot in (((0, 3.2, 3), (PI / 2, 0, 0)), ((-3.6, 0, 3), (PI / 2, 0, PI / 2))):
        bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot); w_ = bpy.context.object; w_.scale = (12, 6, 1); w_.data.materials.append(wm)
    led = bpy.data.materials.new("Strisce LED"); led.use_nodes = True; lb = led.node_tree.nodes["Principled BSDF"]
    lb.inputs["Emission Color"].default_value = (0.85, 0.93, 1, 1); lb.inputs["Emission Strength"].default_value = 12
    for z in (1.2, 2.4):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0.6, 3.17, z)); s_ = bpy.context.object; s_.scale = (6, 0.02, 0.06); s_.data.materials.append(led)
    for x in (-2.2, 2.8):  # benches
        box(f"Banco{x}", mat("Banco", (0.9, 0.9, 0.92), rough=0.4), None, (1.6, 0.7, 0.9), (x, 2.6, 0.45), 0.01)
        box(f"Piano{x}", mat("Piano nero", (0.03, 0.03, 0.035), rough=0.3), None, (1.65, 0.75, 0.04), (x, 2.6, 0.92), 0.005)
    light("Key", (2.6, -2.6, 3.4), 500, 3, (0.95, 0.98, 1)); light("Fill", (-3.0, -2.4, 2.0), 220, 4); light("Top", (0, 0, 4.2), 300, 4)
elif env == "officina":  # production hall: resin floor with walkway lines, yellow overhead crane, bay lights, machine bodies
    bg.inputs[0].default_value = (0.4, 0.42, 0.45, 1); bg.inputs[1].default_value = 0.02
    bpy.ops.mesh.primitive_plane_add(size=40); fl = bpy.context.object; fl.data.materials.append(mat("Resina verde", (0.05, 0.09, 0.08), rough=0.3))
    yel = mat("Giallo sicurezza", (0.9, 0.6, 0.0), rough=0.5)
    for y in (-1.6, 1.5):  # walkway lines
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, y, 0.002)); l_ = bpy.context.object; l_.scale = (40, 0.1, 1); l_.data.materials.append(yel)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 6, 5), rotation=(PI / 2, 0, 0)); wall = bpy.context.object
    wall.scale = (40, 10, 1); wall.data.materials.append(mat("Pannelli", (0.12, 0.13, 0.14), rough=0.7))
    crane = mat("Carroponte", (0.85, 0.55, 0.02), metal=0.3, rough=0.45)
    for x in (-4.5, 4.5):  # crane rails on columns, bridge across
        box(f"Colonna{x}", mat("Acciaio grigio", (0.25, 0.26, 0.28), metal=0.6, rough=0.5), None, (0.4, 0.4, 2.8), (x, 4.4, 1.4), 0.01)
        box(f"Via{x}", crane, None, (0.3, 4, 0.35), (x, 3.4, 2.75), 0.01)
    box("Ponte", crane, None, (9.4, 0.45, 0.45), (0, 3.4, 2.45), 0.01); box("Carrello", crane, None, (0.7, 0.7, 0.4), (-1.8, 3.4, 2.1), 0.02)
    cyl("Fune", mat("Fune", (0.05, 0.05, 0.05), metal=0.8, rough=0.4), None, 0.015, 0.6, (-1.8, 3.4, 1.6))
    torus("Gancio", yel, None, 0.08, 0.02, (-1.8, 3.4, 1.25), axis='Y')
    for x in (-3.2, 3.4):  # machine bodies in the back
        box(f"Macchina{x}", mat("Grigio macchina", (0.2, 0.24, 0.28), metal=0.2, rough=0.4), None, (1.8, 1.2, 1.6), (x, 4.2, 0.8), 0.03)
        box(f"Quadro{x}", mat("Quadro", (0.05, 0.06, 0.07), rough=0.3), None, (0.6, 0.05, 0.4), (x, 3.58, 1.2), 0.005)
    bay = bpy.data.materials.new("Lampada"); bay.use_nodes = True; bb = bay.node_tree.nodes["Principled BSDF"]
    bb.inputs["Emission Color"].default_value = (1, 0.88, 0.7, 1); bb.inputs["Emission Strength"].default_value = 25
    for x in (-2.6, 2.9):  # high-bay lamps
        cyl(f"Campana{x}", mat("Campana", (0.15, 0.15, 0.16), metal=0.7, rough=0.4), None, 0.35, 0.3, (x, 2.6, 2.15), bev=0.01)
        cyl(f"Luce{x}", bay, None, 0.3, 0.02, (x, 2.6, 1.99))
        light(f"Bay{x}", (x, 2.4, 1.9), 250, 0.6, (1, 0.85, 0.65))
    light("Key", (3.0, -3.0, 3.0), 450, 2.0, (1, 0.9, 0.78)); light("Rim", (-2.2, 2.6, 2.6), 900, 1.2, (0.7, 0.82, 1))
elif env == "logistica":  # modern high-bay hall: glossy epoxy floor, sandwich walls, pallet racking, skylights
    bg.inputs[0].default_value = (0.75, 0.85, 1, 1); bg.inputs[1].default_value = 0.25
    bpy.ops.mesh.primitive_plane_add(size=40); fl = bpy.context.object; fl.data.materials.append(mat("Epossidico", (0.42, 0.44, 0.46), rough=0.18))
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 7, 5), rotation=(PI / 2, 0, 0)); wall = bpy.context.object
    wall.scale = (40, 10, 1); wall.data.materials.append(mat("Sandwich bianco", (0.78, 0.8, 0.82), rough=0.6))
    up = mat("Montanti blu", (0.02, 0.12, 0.4), metal=0.4, rough=0.45); beam = mat("Correnti arancio", (0.9, 0.35, 0.03), metal=0.3, rough=0.45)
    for y0 in (3.4, 5.6):  # two rows of racking, three levels
        for x in (-6, -3.6, -1.2, 1.2, 3.6, 6):
            box(f"Mont{x}_{y0}", up, None, (0.1, 1.0, 6), (x, y0, 3), 0.005)
        for z in (0.15, 2.0, 3.9):
            for dy in (-0.45, 0.45):
                box(f"Corr{z}_{dy}_{y0}", beam, None, (12, 0.08, 0.14), (0, y0 + dy, z), 0.005)
        for x in (-4.8, -2.4, 0, 2.4, 4.8):  # loads on the levels
            for z, c in ((0.35, (0.35, 0.24, 0.13)), (2.2, (0.7, 0.7, 0.68)), (4.1, (0.35, 0.24, 0.13))):
                box(f"Carico{x}_{z}_{y0}", mat("Carico", c, rough=0.85), None, (1.9, 0.9, 1.3), (x, y0, z + 0.65), 0.01)
    sky = bpy.data.materials.new("Lucernario"); sky.use_nodes = True; sb = sky.node_tree.nodes["Principled BSDF"]
    sb.inputs["Emission Color"].default_value = (0.85, 0.92, 1, 1); sb.inputs["Emission Strength"].default_value = 8
    for y in (0.5, 3.0, 5.5):  # skylight strips in the roof
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, y, 8), rotation=(PI, 0, 0)); k_ = bpy.context.object; k_.scale = (30, 0.9, 1); k_.data.materials.append(sky)
    light("Sky", (0.5, 1.5, 7.5), 2400, 6, (0.88, 0.94, 1)); light("Key", (3.0, -3.0, 3.0), 550, 2.6, (1, 0.95, 0.88)); light("Rim", (-2.2, 2.6, 2.6), 600, 1.4)
else:  # capannone: concrete floor, back wall, high windows, columns, pallets
    bg.inputs[0].default_value = (0.55, 0.65, 0.8, 1); bg.inputs[1].default_value = 0.12
    bpy.ops.mesh.primitive_plane_add(size=40); fl = bpy.context.object
    cm = mat("Cemento", (0.32, 0.31, 0.3), rough=0.75); fl.data.materials.append(cm)
    n = cm.node_tree.nodes; noise = n.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 3
    ramp = n.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].color = (0.08, 0.075, 0.07, 1); ramp.color_ramp.elements[1].color = (0.16, 0.15, 0.14, 1)
    cm.node_tree.links.new(noise.outputs["Fac"], ramp.inputs["Fac"]); cm.node_tree.links.new(ramp.outputs["Color"], n["Principled BSDF"].inputs["Base Color"])
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 4.2, 5), rotation=(PI / 2, 0, 0)); wall = bpy.context.object
    wall.scale = (40, 10, 1); wall.data.materials.append(mat("Parete", (0.18, 0.2, 0.22), rough=0.8))
    for x in (-5, 0, 5):
        bpy.ops.mesh.primitive_plane_add(size=1, location=(x, 4.15, 3.8), rotation=(PI / 2, 0, 0)); win = bpy.context.object; win.scale = (3.4, 2, 1)
        em = bpy.data.materials.new("Finestra"); em.use_nodes = True; em.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 6
        em.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (0.8, 0.9, 1, 1); win.data.materials.append(em)
    steel = mat("Acciaio strutture", (0.05, 0.12, 0.2), metal=0.6, rough=0.5)
    for x in (-3.8, 0.0, 3.8):  # I-beam columns
        for sx, sy in ((0.5, 0.04), (0.04, 0.5)):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 3.6, 5)); c = bpy.context.object; c.scale = (sx, sy, 10); c.data.materials.append(steel)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 1.3, 0.002)); st = bpy.context.object; st.scale = (40, 0.16, 1)
    st.data.materials.append(mat("Striscia sicurezza", (0.9, 0.6, 0.0), rough=0.5))
    for x in (-2.4, 2.6):  # pallets with boxes
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 2.5, 0.07)); p_ = bpy.context.object; p_.scale = (1.2, 1.0, 0.14); p_.data.materials.append(mat("Pallet", (0.3, 0.2, 0.1), rough=0.9))
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 2.5, 0.45)); b_ = bpy.context.object; b_.scale = (1.0, 0.8, 0.62); b_.data.materials.append(mat("Cartone", (0.35, 0.24, 0.13), rough=0.9))
    light("Sun", (4.5, 3.6, 5.0), 1000, 4.0, (0.85, 0.92, 1)); light("Key", (3.0, -3.0, 3.0), 650, 2.6, (1, 0.9, 0.78)); light("Rim", (-2.2, 2.6, 2.6), 800, 1.4)
bpy.ops.wm.save_as_mainfile(filepath=out)
print("BUILT", env, len(bpy.data.objects))
