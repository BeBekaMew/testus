import bpy

class ANCHOR_PT_main(bpy.types.Panel):
    bl_label='Anchor Generator'
    bl_idname='ANCHOR_PT_main'
    bl_space_type='VIEW_3D'
    bl_region_type='UI'
    bl_category='Anchor'

    def draw(self, context):
        layout=self.layout
        layout.label(text='Anchor Generator v3')
        layout.operator('anchor.generate', icon='MESH_ICOSPHERE')

classes=(ANCHOR_PT_main,)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
