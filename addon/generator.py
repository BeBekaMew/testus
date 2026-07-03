import bpy
import bmesh
from mathutils import Vector


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def create_core(radius=0.4):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=radius)
    obj = bpy.context.object
    obj.name = 'AnchorCore'
    return obj


def generate(context):
    clear_scene()
    obj = create_core()
    return obj
