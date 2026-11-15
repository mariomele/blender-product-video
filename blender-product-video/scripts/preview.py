# Renders frames a..b every `step` frames at low quality, with frame/time stamped on each image. Resumable.
# usage: blender -b file.blend --python gpu_setup.py --python preview.py -- a b step outdir [res%=25] [spp=8] [env JPG_Q=50]
import bpy, sys, os
args = sys.argv[sys.argv.index('--') + 1:]
a, b, step = map(int, args[:3]); out = args[3]
res = int(args[4]) if len(args) > 4 else 25
spp = int(args[5]) if len(args) > 5 else 8
s = bpy.context.scene; r = s.render
fps = round(r.fps / r.fps_base)
frames = list(range(a, b + 1, step))
if step >= fps and frames[-1] != b: frames.append(b)  # storyboard: always show how the scene ends
print("FPS", fps); print("COUNT", len(frames))
r.resolution_percentage = res
s.cycles.device = "GPU"; s.cycles.samples = spp; s.cycles.use_denoising = True
r.use_stamp = True; r.use_stamp_note = False
for k in ("date", "render_time", "camera", "lens", "scene", "filename", "memory", "hostname", "marker", "sequencer_strip", "time"):
    setattr(r, "use_stamp_" + k, False)
r.use_stamp_frame = True; r.stamp_font_size = max(10, r.resolution_y * res // 100 // 40)  # ~1/40 of the image height
r.image_settings.file_format = 'JPEG'; r.image_settings.quality = int(os.environ.get('JPG_Q', 50))
os.makedirs(out, exist_ok=True)
for f in frames:
    path = os.path.join(out, f"f{f:05d}.jpg")
    if os.path.exists(path): continue
    s.frame_set(f); r.filepath = path
    bpy.ops.render.render(write_still=True)
