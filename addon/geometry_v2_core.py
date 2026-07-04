"""Core module for Geometry V2."""

import bpy


class CoreBuilder:
    def __init__(self, radius=0.4):
        self.radius = radius
        self.core = None

    def create_core(self):
        bpy.ops.mesh.primitive_ico_sphere_add(radius=self.radius, subdivisions=4)
        self.core = bpy.context.object
        self.core.name = "AnchorCore_V2"
        return self.core

    def apply_transforms(self):
        bpy.context.view_layer.objects.active = self.core
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    def shade_smooth(self):
        bpy.context.view_layer.objects.active = self.core
        bpy.ops.object.shade_smooth()
