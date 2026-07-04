"""Geometry V2 - Ring generation."""

import bpy
import bmesh


class RingBuilder:
    """Creates a procedural ring around the Anchor cavity."""

    def __init__(self, core):
        self.core = core

    def create_ring(self,
                    major_radius=0.18,
                    minor_radius=0.035,
                    major_segments=48,
                    minor_segments=16):

        bpy.ops.mesh.primitive_torus_add(
            major_radius=major_radius,
            minor_radius=minor_radius,
            major_segments=major_segments,
            minor_segments=minor_segments,
        )

        ring = bpy.context.object
        ring.name = "AnchorRing"

        bm = bmesh.new()
        bm.from_mesh(ring.data)

        for vert in bm.verts:
            vert.co += vert.normal * 0.003

        bm.normal_update()
        bm.to_mesh(ring.data)
        bm.free()

        return ring

    def align_to_core(self):
        if self.core is not None:
            self.core.rotation_euler = (0.0, 0.0, 0.0)
