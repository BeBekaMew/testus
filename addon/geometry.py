import bpy
import bmesh
import random
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
    mod.operation='DIFFERENCE'
    mod.solver='EXACT'
    mod.object=cutter
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


def build_major_plates(obj, count=8, radius=0.42):
    random.seed(1)
    plates=[]
    for i in range(count):
        bpy.ops.mesh.primitive_cube_add(size=random.uniform(0.15,0.28))
        plate=bpy.context.object
        plate.name=f"Plate_{i:02d}"
        plate.location=Vector((random.uniform(-radius,radius),random.uniform(-radius,radius),random.uniform(-radius,radius)))
        plate.rotation_euler=(random.random()*3.14,random.random()*3.14,random.random()*3.14)
        plates.append(plate)
    return plates


def prepare_core(radius=0.4):
    obj=create_core(radius)
    apply_scale(obj)
    create_cavity(obj)
    build_major_plates(obj)
    shade_smooth(obj)
    return obj