bl_info = {
    "name": "Anchor Generator 3.0",
    "author": "OpenAI & BeBekaMew",
    "version": (0,1,0),
    "blender": (4,2,0),
    "location": "View3D > Sidebar > Anchor",
    "category": "Object",
    "description": "Procedural Anchor artifact generator"
}

import bpy

from . import ui, operators

modules = (ui, operators)


def register():
    for m in modules:
        m.register()


def unregister():
    for m in reversed(modules):
        m.unregister()


if __name__ == "__main__":
    register()
