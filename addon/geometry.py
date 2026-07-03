import bpy
import random
from mathutils import Vector

# NOTE: Temporary scaffold extending the current prototype.
# Core helpers remain unchanged from previous revision.

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
    m=obj.modifiers.new('Cavity','BOOLEAN')
    m.operation='DIFFERENCE';m.solver='EXACT';m.object=cutter
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.data.objects.remove(cutter,do_unlink=True)

def build_major_plates(count=8,radius=0.42):
    plates=[];random.seed(1)
    for i in range(count):
        bpy.ops.mesh.primitive_cube_add(size=random.uniform(0.15,0.28))
        p=bpy.context.object
        p.location=Vector((random.uniform(-radius,radius),random.uniform(-radius,radius),random.uniform(-radius,radius)))
        p.scale=(random.uniform(.5,1.6),random.uniform(.4,1.4),random.uniform(.5,1.8))
        plates.append(p)
    return plates

def build_secondary_shards(count=24,radius=0.55):
    shards=[]
    for _ in range(count):
        bpy.ops.mesh.primitive_cone_add(vertices=5,radius1=random.uniform(0.015,0.04),depth=random.uniform(0.05,0.12))
        s=bpy.context.object
        s.location=Vector((random.uniform(-radius,radius),random.uniform(-radius,radius),random.uniform(-radius,radius)))
        s.rotation_euler=(random.random()*3.14,random.random()*3.14,random.random()*3.14)
        shards.append(s)
    return shards

def boolean_union(core,objs):
    bpy.context.view_layer.objects.active=core
    for o in objs:
        m=core.modifiers.new(f'U_{o.name}','BOOLEAN')
        m.operation='UNION';m.solver='EXACT';m.object=o
        bpy.ops.object.modifier_apply(modifier=m.name)
        bpy.data.objects.remove(o,do_unlink=True)

def voxel_remesh(obj,size=0.03):
    r=obj.modifiers.new('Remesh','REMESH');r.mode='VOXEL';r.voxel_size=size
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.modifier_apply(modifier=r.name)
    b=obj.modifiers.new('Bevel','BEVEL');b.width=0.003;b.segments=2
    bpy.ops.object.modifier_apply(modifier=b.name)

def prepare_core(radius=0.4):
    core=create_core(radius)
    apply_scale(core)
    create_cavity(core)
    objs=build_major_plates()+build_secondary_shards()
    boolean_union(core,objs)
    voxel_remesh(core)
    shade_smooth(core)
    return core