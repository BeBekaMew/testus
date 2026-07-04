"""
Geometry V2
Procedural stone plate generator.

This module is responsible only for creation of a single stone plate.
Further deformation is performed by geometry_v2_deform.py
"""

from __future__ import annotations

import math
import random

import bpy
import bmesh

from mathutils import Vector
from mathutils import Matrix
from mathutils import Euler


class PlateBuilder:

    def __init__(self, seed=None):

        self.random = random.Random(seed)

    # ----------------------------------------------------
    # PUBLIC
    # ----------------------------------------------------

    def create_plate(
            self,
            width=0.18,
            height=0.045,
            depth=0.20):

        mesh = bpy.data.meshes.new("AnchorPlate")
        obj = bpy.data.objects.new("AnchorPlate", mesh)

        bpy.context.collection.objects.link(obj)

        bm = bmesh.new()

        self._create_base_block(
            bm,
            width,
            height,
            depth
        )

        self._shape_profile(
            bm,
            width,
            height,
            depth
        )

        self._prepare_faces(bm)
        self._finalize_mesh(bm)
                
        bm.normal_update()

        bm.to_mesh(mesh)
        bm.free()

        mesh.update()

        return obj

    # ----------------------------------------------------
    # BASE SHAPE
    # ----------------------------------------------------

    def _create_base_block(
            self,
            bm,
            width,
            height,
            depth):

        bmesh.ops.create_cube(
            bm,
            size=1.0
        )

        for v in bm.verts:

            v.co.x *= width
            v.co.y *= height
            v.co.z *= depth

    # ----------------------------------------------------
    # PRIMARY SHAPING
    # ----------------------------------------------------

    def _shape_profile(
            self,
            bm,
            width,
            height,
            depth):

        for v in bm.verts:

            taper = self.random.uniform(
                0.82,
                1.28
            )

            v.co.x *= taper

            taper = self.random.uniform(
                0.90,
                1.35
            )

            v.co.z *= taper

            v.co.y *= self.random.uniform(
                0.65,
                1.35
            )

            v.co += Vector((
                self.random.uniform(-0.006, 0.006),
                self.random.uniform(-0.003, 0.003),
                self.random.uniform(-0.006, 0.006)
            ))

        self._bend_plate(bm)
        self._pinch_center(bm)
# ----------------------------------------------------
    # CURVATURE
    # ----------------------------------------------------

    def _bend_plate(
            self,
            bm):

        amount = self.random.uniform(
            0.02,
            0.05
        )

        for v in bm.verts:

            d = abs(v.co.x)

            factor = 1.0 - min(
                d / 0.22,
                1.0
            )

            v.co.y += factor * amount

    # ----------------------------------------------------
    # PINCH
    # ----------------------------------------------------

    def _pinch_center(
            self,
            bm):

        strength = self.random.uniform(
            0.90,
            0.97
        )

        for v in bm.verts:

            if abs(v.co.x) < 0.06:

                v.co.x *= strength

                v.co.z *= strength

    # ----------------------------------------------------
    # BACK SIDE
    # ----------------------------------------------------

    def _flatten_back(
            self,
            bm):

        minimum = 1000.0

        for v in bm.verts:

            if v.co.y < minimum:
                minimum = v.co.y

        for v in bm.verts:

            if abs(v.co.y - minimum) < 0.0001:

                v.co.y = minimum

    # ----------------------------------------------------
    # EDGE VARIATION
    # ----------------------------------------------------

    def _random_edge_shift(
            self,
            bm):

        for edge in bm.edges:

            if self.random.random() > 0.45:
                continue

            shift = Vector((
                self.random.uniform(-0.004, 0.004),
                self.random.uniform(-0.001, 0.001),
                self.random.uniform(-0.004, 0.004)
            ))

            edge.verts[0].co += shift
            edge.verts[1].co += shift * 0.35

    # ----------------------------------------------------
    # FACE PREPARATION
    # ----------------------------------------------------

    def _prepare_faces(
            self,
            bm):

        bmesh.ops.recalc_face_normals(
            bm,
            faces=bm.faces
        )

        for face in bm.faces:

            face.smooth = False

        self._flatten_back(bm)
        self._random_edge_shift(bm)

 # ----------------------------------------------------
    # SECONDARY EXTRUSION
    # ----------------------------------------------------

    def _extrude_random_faces(
            self,
            bm):

        candidates = []

        for face in bm.faces:

            if abs(face.normal.y) > 0.90:
                continue

            candidates.append(face)

        self.random.shuffle(candidates)

        count = min(
            len(candidates),
            self.random.randint(2, 5)
        )

        for face in candidates[:count]:

            result = bmesh.ops.extrude_face_region(
                bm,
                geom=[face]
            )

            verts = [
                g for g in result["geom"]
                if isinstance(g, bmesh.types.BMVert)
            ]

            normal = face.normal.normalized()

            distance = self.random.uniform(
                0.010,
                0.030
            )

            for vert in verts:

                vert.co += normal * distance

                vert.co += Vector((
                    self.random.uniform(-0.002, 0.002),
                    self.random.uniform(-0.001, 0.001),
                    self.random.uniform(-0.002, 0.002)
                ))

    # ----------------------------------------------------
    # SURFACE NOISE
    # ----------------------------------------------------

    def _surface_noise(
            self,
            bm):

        for vert in bm.verts:

            strength = 0.003

            vert.co.x += self.random.uniform(
                -strength,
                strength
            )

            vert.co.y += self.random.uniform(
                -strength * 0.5,
                strength * 0.5
            )

            vert.co.z += self.random.uniform(
                -strength,
                strength
            )

    # ----------------------------------------------------
    # EDGE SHARPENING
    # ----------------------------------------------------

    def _crease_edges(
            self,
            bm):

        for edge in bm.edges:

            angle = edge.calc_face_angle(None)

            if angle is None:
                continue

            if angle > math.radians(35):

                edge.smooth = False

    # ----------------------------------------------------
    # FINAL MESH PASS
    # ----------------------------------------------------

    def _finalize_mesh(
            self,
            bm):

        self._extrude_random_faces(bm)

        self._surface_noise(bm)

        self._crease_edges(bm)

        bmesh.ops.recalc_face_normals(
            bm,
            faces=bm.faces
        )

        bm.normal_update()
