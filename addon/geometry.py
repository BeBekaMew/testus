import bpy
import random
from mathutils import Vector

# Core helpers retained

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
    m.operation='DIFFERENCE'; m.solver='EXACT'; m.object=cutter
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.data.objects.remove(cutter,do_unlink=True)

def build_major_plates(count=8,radius=0.42):
    plates=[]; random.seed(1)
    for i in range(count):
        bpy.ops.mesh.primitive_cube_add(size=random.uniform(0.15,0.28))
        p=bpy.context.object
        p.location=Vector((random.uniform(-radius,radius),random.uniform(-radius,radius),random.uniform(-radius,radius)))
        p.scale=(random.uniform(0.5,1.6),random.uniform(0.4,1.4),random.uniform(0.5,1.8))
        d=p.modifiers.new('Displace','DISPLACE')
        t=bpy.data.textures.new(f'Noise_{i}','CLOUDS')
        d.texture=t; d.strength=0.08
        plates.append(p)
    return plates

def boolean_union(core,plates):
    bpy.context.view_layer.objects.active=core
    for p in plates:
        m=core.modifiers.new(f'U_{p.name}','BOOLEAN')
        m.operation='UNION'; m.object=p; m.solver='EXACT'
        bpy.ops.object.modifier_apply(modifier=m.name)
        bpy.data.objects.remove(p,do_unlink=True)

def voxel_remesh(obj,size=0.03):
    r=obj.modifiers.new('Remesh','REMESH')
    r.mode='VOXEL'; r.voxel_size=size
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.modifier_apply(modifier=r.name)

def prepare_core(radius=0.4):
    core=create_core(radius)
    apply_scale(core)
    create_cavity(core)
    plates=build_major_plates()
    boolean_union(core,plates)
    voxel_remesh(core)
    shade_smooth(core)
    return core