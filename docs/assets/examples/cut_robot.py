# Cutaway of the robot: hollows the housings, cuts a section through J1, J2, J3 and their motors, red caps on the castings.
# usage: blender -b robot.blend --python cut_robot.py -- <frame> <out.jpg> [spp] [res%]
import bpy, sys
a = sys.argv[sys.argv.index('--') + 1:]; frame, out = int(a[0]), a[1]
spp = int(a[2]) if len(a) > 2 else 128; res = int(a[3]) if len(a) > 3 else 80
s = bpy.context.scene; O = bpy.data.objects
CAP = bpy.data.materials.new("Sezione"); CAP.use_nodes = True
b = CAP.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (0.45, 0.02, 0.015, 1); b.inputs["Roughness"].default_value = 0.5

# hollow housings: subtract a smaller copy of themselves (same parent and transform)
HOLLOW = {"rame": (0.55, 1.1), "carter": (0.88, 0.94), "corpo": (0.88, 0.9), "colonna": (0.85, 1.2), "statore": (0.7, 1.1), "rotore": (0.4, 1.1), "flexspline": (0.85, 1.1)}
for o in [o for o in O if o.type == 'MESH']:
    k = next((k for k in HOLLOW if "." + k in o.name and not o.name.endswith("_vuoto")), None)
    if not k: continue
    r, l = HOLLOW[k]; h = o.copy(); h.modifiers.clear(); h.name = o.name + "_vuoto"; s.collection.objects.link(h)
    h.scale = (o.scale[0] * r, o.scale[1] * r, o.scale[2] * l); h.hide_render = True; h.hide_viewport = True
    m = o.modifiers.new("Vuoto", 'BOOLEAN'); m.operation = 'DIFFERENCE'; m.solver = 'EXACT'; m.object = h

# the arm castings overlap their joint housing: empty them there too, so the gearbox is not buried in the casting
for link, joint in (("J2.braccio", "J2.carter"), ("J1.spalla", "J2.carter"), ("J3.avambraccio", "J3.carter")):
    m = O[link].modifiers.new("Vuoto", 'BOOLEAN'); m.operation = 'DIFFERENCE'; m.solver = 'EXACT'; m.object = O[joint + "_vuoto"]

def cutter(name, parent, lo, hi, prefixes, skip=()):
    bpy.ops.mesh.primitive_cube_add(size=1); c = bpy.context.object; c.name = name; c.parent = parent
    c.location = [(x + y) / 2 for x, y in zip(lo, hi)]; c.scale = [y - x for x, y in zip(lo, hi)]
    c.data.materials.append(CAP); c.hide_render = True; c.hide_viewport = True
    for o in [o for o in O if o.type == 'MESH' and o.name.startswith(prefixes) and not o.name.endswith("_vuoto") and o != c]:
        if any(x in o.name for x in skip): continue
        m = o.modifiers.new("Taglio " + name, 'BOOLEAN'); m.operation = 'DIFFERENCE'; m.solver = 'EXACT'; m.object = c
        inside = any(x in o.name for x in (".int.", ".rame", ".rotore", ".albero"))
        m.material_mode = 'INDEX' if inside else 'TRANSFER'  # internals keep their own colour on the cut face
        if not inside and CAP.name not in o.data.materials: o.data.materials.append(CAP)
# the base turns so the J2 section plane faces the camera, the arm reaches towards the lens and out of the top of the frame
CAM = __import__("mathutils").Vector((0.75, -1.75, 0.45))
j1 = O["J1"]; j1.animation_data_clear(); j1.rotation_euler.z = __import__("math").atan2(CAM.y, CAM.x)
cutter("C1", j1, (0, -0.6, -0.25), (0.6, 0, 0.2), ("J1.", "Base.colonna", "Base.anello", "Base.targa"), ("spalla", "J1.motore"))
cutter("C2", O["J2"], (0, -0.7, -0.3), (0.4, 0.3, 0.25), ("J2.", "J1.spalla"), ("cavo", "fascetta"))

p = bpy.context.preferences.addons['cycles'].preferences; p.compute_device_type = 'METAL'; p.get_devices()
for d in p.devices: d.use = True
s.render.engine = 'CYCLES'; s.cycles.device = 'GPU'; s.cycles.samples = spp; s.cycles.use_denoising = True
s.render.resolution_percentage = res; s.frame_set(frame)
# close shot on the shoulder: camera off the orbit rig, aimed between J1 and J2
cam = s.camera; mw = cam.matrix_world.copy(); cam.parent = None; cam.constraints.clear(); cam.animation_data_clear()
bpy.context.view_layer.update(); t = (O["J1"].matrix_world.translation + O["J2"].matrix_world.translation) / 2
aim = bpy.data.objects.new("Mira", None); s.collection.objects.link(aim); aim.location = t
cam.location = t + CAM; cam.data.lens = 40
cam.constraints.new('TRACK_TO').target = aim; cam.data.dof.focus_object = aim; cam.data.dof.aperture_fstop = 5.6
s.render.image_settings.file_format = 'JPEG'; s.render.image_settings.quality = 90; s.render.filepath = out
bpy.ops.render.render(write_still=True)
