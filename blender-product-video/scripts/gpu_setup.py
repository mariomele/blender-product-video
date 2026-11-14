import bpy, subprocess
p = bpy.context.preferences.addons['cycles'].preferences
p.compute_device_type = 'METAL'
p.get_devices()
for d in p.devices:
    d.use = d.type == 'METAL'
    print("DEV", d.type, d.name, d.use)
chip = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], capture_output=True, text=True).stdout
# M1/M2 have no hardware ray tracing: MetalRT there is slower. M3+ has it: let Blender decide (AUTO).
rt = "metalrt" if hasattr(p, "metalrt") else "metal_rt"  # renamed across Blender versions
if hasattr(p, rt): setattr(p, rt, 'OFF' if ('M1' in chip or 'M2' in chip) else 'AUTO')
print("CHIP", chip.strip(), "METALRT", getattr(p, rt, "n/a"))
