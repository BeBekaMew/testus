import bpy
import random
from mathutils import Vector


def create_core(radius=0.4, subdivisions=3):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=radius, subdivisions=subdivisions)
    obj=bpy.context.object
    obj.name='AnchorCore'
    return obj


def apply_scale(obj):
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)


def shade_smooth(obj):
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.shade_smooth()


def create_cavity(obj,radius=0.09,depth=2.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=radius,depth=depth)
    cutter=bpy.context.object
    mod=obj.modifiers.new('Cavity','BOOLEAN')
    mod.operation='DIFFERENCE'
    mod.solver='EXACT'
    mod.object=cutter
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter,do_unlink=True)


def build_major_plates(count=8,radius=0.42):
    plates=[]
    random.seed(1)
    for i in range(count):
        bpy.ops.mesh.primitive_cube_add(size=random.uniform(0.15,0.28))
        p=bpy.context.object
        p.location=Vector((random.uniform(-radius,radius),random.uniform(-radius,radius),random.uniform(-radius,radius)))
        p.rotation_euler=(random.random()*3.14,random.random()*3.14,random.random()*3.14)
        plates.append(p)
    return plates


def boolean_union(core,objects):
    for obj in objects:
        m=core.modifiers.new(f'Union_{obj.name}','BOOLEAN')
        m.operation='UNION'
        m.solver='EXACT'
        m.object=obj


def prepare_core(radius=0.4):
    core=create_core(radius)
    apply_scale(core)
    create_cavity(core)
    plates=build_major_plates()
    boolean_union(core,plates)
    shade_smooth(core)
    return core