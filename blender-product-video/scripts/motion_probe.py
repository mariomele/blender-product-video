# Measures how the moving parts of a scene really move, to check them against funzionamento.md.
# usage: blender -b scena.blend --python motion_probe.py -- <out.json> [step=1] [first last]
# For every object (not cameras) whose transform changes: position (m) and rotation (deg, unwrapped) relative to its
# parent, constraints and drivers included, per sampled frame. Prints one PROBE line per object: travel, mean rpm, range.
import bpy, sys, json, math
a = sys.argv[sys.argv.index('--') + 1:]; out = a[0]; step = int(a[1]) if len(a) > 1 else 1
s = bpy.context.scene; fps = s.render.fps / s.render.fps_base
first, last = (int(a[2]), int(a[3])) if len(a) > 3 else (s.frame_start, s.frame_end)
frames = list(range(first, last + 1, step)); obs = [o for o in s.objects if o.type != 'CAMERA']
tr = {o.name: {"loc": [], "rot_deg": []} for o in obs}; prev = {}
for f in frames:
    s.frame_set(f)
    for o in obs:
        m = o.parent.matrix_world.inverted() @ o.matrix_world if o.parent else o.matrix_world
        e = m.to_euler('XYZ', prev[o.name]) if o.name in prev else m.to_euler('XYZ'); prev[o.name] = e  # compat euler = no 360° jumps
        tr[o.name]["loc"].append([round(v, 5) for v in m.translation]); tr[o.name]["rot_deg"].append([round(math.degrees(v), 3) for v in e])
def moves(rows, tol): return any(abs(x - y) > tol for r in rows for x, y in zip(r, rows[0]))
moving = {k: v for k, v in tr.items() if moves(v["loc"], 1e-4) or moves(v["rot_deg"], 0.05)}  # 0.1 mm, 0.05°: float noise is below
secs = (frames[-1] - frames[0]) / fps or 1
for k, v in moving.items():
    R = list(zip(*v["rot_deg"])); L = list(zip(*v["loc"]))
    print(f"PROBE {k} rot_tot_deg={tuple(round(r[-1] - r[0], 1) for r in R)} rpm={tuple(round((r[-1] - r[0]) / secs / 6, 2) for r in R)}"
          f" rot_range_deg={tuple(round(max(r) - min(r), 1) for r in R)} loc_range_m={tuple(round(max(l) - min(l), 4) for l in L)}")
json.dump({"fps": fps, "frames": frames, "objects": moving}, open(out, "w"))
print(f"PROBE_OK {len(moving)} moving objects, {len(frames)} frames -> {out}")
