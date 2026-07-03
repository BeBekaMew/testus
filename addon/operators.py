import bpy


class ANCHOR_OT_generate(bpy.types.Operator):
    bl_idname = "anchor.generate"
    bl_label = "Generate Anchor"
    bl_description = "Generate procedural Anchor artifact"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            from . import generator
            generator.generate(context)
            self.report({'INFO'}, 'Anchor generated')
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}


classes = (
    ANCHOR_OT_generate,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
