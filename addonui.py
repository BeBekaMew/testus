import bpy


class ANCHOR_PT_main(bpy.types.Panel):
    """Главная панель генератора"""

    bl_label = "Anchor Generator"
    bl_idname = "ANCHOR_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Anchor"

    def draw(self, context):

        layout = self.layout
        scene = context.scene

        layout.label(text="S.T.A.L.K.E.R. Artifact")

        box = layout.box()

        box.prop(scene, "anchor_seed")
        box.prop(scene, "anchor_scale")

        box.separator()

        box.prop(scene, "anchor_plate_count")
        box.prop(scene, "anchor_shard_count")

        box.separator()

        box.prop(scene, "anchor_damage")

        layout.separator()

        layout.operator(
            "anchor.generate",
            icon='MESH_ICOSPHERE'
        )


# ----------------------------------------------------------
# Регистрация свойств
# ----------------------------------------------------------

def register():

    bpy.types.Scene.anchor_seed = bpy.props.IntProperty(
        name="Seed",
        default=1,
        min=1,
        max=999999
    )

    bpy.types.Scene.anchor_scale = bpy.props.FloatProperty(
        name="Scale",
        default=1.0,
        min=0.1,
        max=5.0
    )

    bpy.types.Scene.anchor_plate_count = bpy.props.IntProperty(
        name="Plates",
        default=10,
        min=4,
        max=32
    )

    bpy.types.Scene.anchor_shard_count = bpy.props.IntProperty(
        name="Shards",
        default=80,
        min=10,
        max=500
    )

    bpy.types.Scene.anchor_damage = bpy.props.FloatProperty(
        name="Damage",
        default=0.45,
        min=0.0,
        max=1.0
    )

    bpy.utils.register_class(
        ANCHOR_PT_main
    )


def unregister():

    bpy.utils.unregister_class(
        ANCHOR_PT_main
    )

    del bpy.types.Scene.anchor_seed
    del bpy.types.Scene.anchor_scale
    del bpy.types.Scene.anchor_plate_count
    del bpy.types.Scene.anchor_shard_count
    del bpy.types.Scene.anchor_damage