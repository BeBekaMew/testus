import bpy
import random
from mathutils import Vector

# Existing helper functions omitted for brevity in this update...
# (Preserve previous functions: create_core, apply_scale, shade_smooth, create_cavity)


def build_major_plates(obj, count=8, radius=0.42):
    random.seed(1)
    plates=[]
    for i in range(count):
        bpy.ops.mesh.primitive_cube_add(size=random.uniform(0.15,0.28))
        plate=bpy.context.object
        plate.name=f"Plate_{i:02d}"
        plate.location=Vector((random.uniform(-radius,radius),random.uniform(-radius,radius),random.uniform(-radius,radius)))
        plate.rotation_euler=(random.random()*3.14,random.random()*3.14,random.random()*3.14)

        disp=plate.modifiers.new("Displace","DISPLACE")
        tex=bpy.data.textures.new(f"PlateNoise_{i}",type='CLOUDS')
        disp.texture=tex
        disp.strength=0.08

        bevel=plate.modifiers.new("Bevel","BEVEL")
        bevel.width=0.01
        bevel.segments=2

        plates.append(plate)
    return plates