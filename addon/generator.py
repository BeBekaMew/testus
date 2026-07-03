import bpy
from . import geometry


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def generate(context):
    """Main entry point for Anchor generation."""
    clear_scene()

    # Stage 1: create the core.
    core = geometry.prepare_core(radius=0.4)

    # TODO: next commits
    # geometry.create_cavity(core)
    # geometry.build_major_plates(core)
    # geometry.build_minor_plates(core)
    # geometry.build_shards(core)
    # geometry.boolean_union(...)

    return core
