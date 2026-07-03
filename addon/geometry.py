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


def create_cavity(obj, radius=0.09, depth=2.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=radius, depth=depth)
    cutter = bpy.context.object
    mod = obj.modifiers.new("Cavity", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.solver = 'EXACT'
    mod.object = cutter
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


def prepare_core(radius=0.4):
    obj = create_core(radius)
    apply_scale(obj)
    create_cavity(obj)
    shade_smooth(obj)
    return obj
