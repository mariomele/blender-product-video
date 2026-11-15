# Builds an animated stress object from fea_surface.py's .npz: the part bends (exaggerated) while the
# von Mises colours rise from its metal, blue low to red at the limit.
# usage: blender -b --factory-startup --python fea_to_blend.py -- <surface.npz> <out.blend> <limit_MPa> [deform_scale=auto] [start=1] [end=72]
# limit_MPa: the red end, usually the material's yield, so red means "it yields here".
import bpy, sys, os, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
src, out, limit = a[0], a[1], float(a[2])
d = np.load(src)
pts, disp = d['points'] * 0.001, d['displacement'] * 0.001  # mm → m
size = np.ptp(pts, axis=0).max()
scale = float(a[3]) if len(a) > 3 and a[3] != 'auto' else 0.08 * size / max(np.linalg.norm(disp, axis=1).max(), 1e-12)
start, end = (int(a[4]), int(a[5])) if len(a) > 5 else (1, 72)
bpy.ops.wm.read_factory_settings(use_empty=True)
me = bpy.data.meshes.new('FEA')
me.from_pydata(pts.tolist(), [], d['faces'].tolist())
me.attributes.new('stress', 'FLOAT', 'POINT').data.foreach_set('value', np.clip(d['von_mises'] / limit, 0, 1).astype(np.float32))
ob = bpy.data.objects.new('FEA', me); bpy.context.scene.collection.objects.link(ob)
ob.shape_key_add(name='Basis'); k = ob.shape_key_add(name='Carico')
k.data.foreach_set('co', (pts + disp * scale).astype(np.float32).ravel())
mat = bpy.data.materials.new('FEA'); mat.use_nodes = True; nt = mat.node_tree
bsdf = nt.nodes['Principled BSDF']
attr = nt.nodes.new('ShaderNodeAttribute'); attr.attribute_name = 'stress'
ramp = nt.nodes.new('ShaderNodeValToRGB'); cr = ramp.color_ramp
cr.elements[0].color, cr.elements[1].color = (0.02, 0.1, 0.8, 1), (0.9, 0.03, 0.01, 1)
for pos, c in ((0.25, (0.0, 0.6, 0.8)), (0.5, (0.1, 0.8, 0.1)), (0.75, (1.0, 0.85, 0.0))):
    cr.elements.new(pos).color = (*c, 1)  # new() keeps the stops sorted; setting .position does not
mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.inputs['A'].default_value = (0.6, 0.6, 0.62, 1)
nt.links.new(attr.outputs['Fac'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], mix.inputs['B'])
nt.links.new(mix.outputs['Result'], bsdf.inputs['Base Color'])
nt.links.new(mix.outputs['Result'], bsdf.inputs['Emission Color']); bsdf.inputs['Emission Strength'].default_value = 0.0
bsdf.inputs['Roughness'].default_value = 0.35
ob.data.materials.append(mat)
for v, f in ((0, start), (1, end)):  # the load comes on: bend and colour together
    k.value = v; k.keyframe_insert('value', frame=f)
    mix.inputs['Factor'].default_value = v; mix.inputs['Factor'].keyframe_insert('default_value', frame=f)
    bsdf.inputs['Metallic'].default_value = 1 - v; bsdf.inputs['Metallic'].keyframe_insert('default_value', frame=f)
me.shade_smooth(); me.set_sharp_from_angle(angle=0.6)  # tetra surfaces: smooth curves, keep the CAD edges sharp
lo = pts.min(0); hi = pts.max(0)
ob.location = (-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2])
bpy.context.scene.frame_start, bpy.context.scene.frame_end = start, end
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(out))
print(f"FEA deformazione x{scale:.0f}, rosso = {limit:g} MPa, frame {start}-{end}")
