"""Geometry V2 - Remesh and mesh cleanup."""

import bpy


class RemeshBuilder:
    """Applies remesh and basic cleanup modifiers."""

    def apply_voxel_remesh(self, obj, voxel_size=0.03):
        modifier = obj.modifiers.new("VoxelRemesh", "REMESH")
        modifier.mode = 'VOXEL'
        modifier.voxel_size = voxel_size
        return modifier

    def apply_bevel(self, obj, width=0.003, segments=2):
        modifier = obj.modifiers.new("Bevel", "BEVEL")
        modifier.width = width
        modifier.segments = segments
        return modifier

    def finalize(self, obj):
        return obj