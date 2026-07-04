"""Geometry V2 - Secondary shard generation."""

import random
import bpy
from mathutils import Vector


class ShardBuilder:
    """Creates secondary stone shards around the core."""

    def __init__(self, seed=None):
        self.random = random.Random(seed)

    def create_shard(self, size=0.03):
        bpy.ops.mesh.primitive_ico_sphere_add(radius=size, subdivisions=1)
        obj = bpy.context.object
        obj.name = "AnchorShard"
        return obj

    def place_shard(self, obj, radius=0.5):
        obj.location = Vector((
            self.random.uniform(-radius, radius),
            self.random.uniform(-radius, radius),
            self.random.uniform(-radius, radius),
        ))
        return obj
