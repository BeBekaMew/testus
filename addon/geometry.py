import bpy
import bmesh
from math import radians
from mathutils import Vector


def create_core(radius=0.4, subdivisions=3):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=radius, subdivisions=subdivisions)
    obj = bpy.context.object
    obj.name = "AnchorCore"
    return obj


def apply_scale(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)


def shade_smooth(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()


def prepare_core(radius=0.4):
    obj = create_core(radius)
    apply_scale(obj)
    shade_smooth(obj)
    return obj
