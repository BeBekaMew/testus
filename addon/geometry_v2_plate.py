"""Geometry V2 - Procedural plate generation."""

import random
import bpy
import bmesh
from mathutils import Vector


class PlateBuilder:
    """Creates a single procedural rock plate for the Anchor artifact."""

    def __init__(self, seed=None):
        self.random = random.Random(seed)

    def create_plate(self, size=0.18, thickness=0.05):
        mesh = bpy.data.meshes.new("AnchorPlate")
        obj = bpy.data.objects.new("AnchorPlate", mesh)
        bpy.context.collection.objects.link(obj)

        bm = bmesh.new()

        bmesh.ops.create_cube(bm, size=size)

        for vert in bm.verts:
            scale = Vector((
                self.random.uniform(0.8, 1.6),
                self.random.uniform(0.15, 0.45),
                self.random.uniform(0.8, 1.5),
            ))
            vert.co.x *= scale.x
            vert.co.y *= thickness * scale.y
            vert.co.z *= scale.z
            vert.co += Vector((
                self.random.uniform(-0.01, 0.01),
                self.random.uniform(-0.004, 0.004),
                self.random.uniform(-0.01, 0.01),
            ))

        bm.normal_update()
        bm.to_mesh(mesh)
        bm.free()

        return obj

    def orient_plate(self, obj, location, rotation):
        obj.location = location
        obj.rotation_euler = rotation
        return obj
