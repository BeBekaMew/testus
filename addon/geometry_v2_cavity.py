"""Geometry V2 - Central cavity generation."""

import bpy


class CavityBuilder:
    """Creates the central through-hole for the Anchor artifact."""

    def __init__(self, core):
        self.core = core

    def create_cavity(self, radius=0.09, depth=2.0, vertices=64):
        if self.core is None:
            raise RuntimeError("Core object is not set")

        bpy.ops.mesh.primitive_cylinder_add(
            vertices=vertices,
            radius=radius,
            depth=depth,
        )
        cutter = bpy.context.object
        cutter.name = "AnchorCavity"

        modifier = self.core.modifiers.new("Cavity", "BOOLEAN")
        modifier.operation = 'DIFFERENCE'
        modifier.solver = 'EXACT'
        modifier.object = cutter

        bpy.context.view_layer.objects.active = self.core
        bpy.ops.object.modifier_apply(modifier=modifier.name)

        bpy.data.objects.remove(cutter, do_unlink=True)

    def create_ring_placeholder(self, radius=0.12, thickness=0.02):
        """Placeholder for the future reinforcing ring geometry."""
        return {
            "radius": radius,
            "thickness": thickness,
        }
