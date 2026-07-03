"""
Geometry V2

Experimental procedural geometry generator for the Anchor artifact.
This module is developed independently from geometry.py so the current
addon remains functional while the new generator evolves.
"""

import bpy
import bmesh
from mathutils import Vector


class GeometryBuilder:
    def __init__(self, radius=0.4):
        self.radius = radius
        self.core = None

    def create_core(self):
        bpy.ops.mesh.primitive_ico_sphere_add(
            radius=self.radius,
            subdivisions=4,
        )
        self.core = bpy.context.object
        self.core.name = "AnchorCore_V2"
        return self.core

    def create_cavity(self, radius=0.09, depth=2.0):
        if self.core is None:
            raise RuntimeError("Core has not been created")

        bpy.ops.mesh.primitive_cylinder_add(
            vertices=64,
            radius=radius,
            depth=depth,
        )
        cutter = bpy.context.object

        mod = self.core.modifiers.new("Cavity", "BOOLEAN")
        mod.operation = 'DIFFERENCE'
        mod.solver = 'EXACT'
        mod.object = cutter

        bpy.context.view_layer.objects.active = self.core
        bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.data.objects.remove(cutter, do_unlink=True)


def prepare_core(radius=0.4):
    builder = GeometryBuilder(radius)
    builder.create_core()
    builder.create_cavity()
    return builder.core
