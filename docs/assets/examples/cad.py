# CAD-viewport look of the demo pump: -- frame out.png
import bpy, sys
a = sys.argv[sys.argv.index('--') + 1:]
s = bpy.context.scene
s.render.engine = 'BLENDER_WORKBENCH'; s.render.resolution_percentage = 80
sh = s.display.shading
sh.light = 'STUDIO'; sh.color_type = 'SINGLE'; sh.single_color = (0.78, 0.80, 0.83)
sh.show_cavity = True; sh.cavity_type = 'BOTH'; sh.show_object_outline = True; sh.object_outline_color = (0.1, 0.12, 0.15)
sh.background_type = 'VIEWPORT'; sh.background_color = (0.93, 0.94, 0.95)
s.render.film_transparent = False
for o in s.objects:  # hide the backdrop: keep only the product
    if o.type == 'MESH' and o.name.startswith('Plane'): o.hide_render = True
s.view_settings.view_transform = 'Standard'
s.frame_set(int(a[0])); s.render.image_settings.file_format = 'PNG'; s.render.filepath = a[1]
bpy.ops.render.render(write_still=True)
