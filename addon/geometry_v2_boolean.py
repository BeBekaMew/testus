"""Geometry V2 - Boolean stage."""

class BooleanBuilder:
    """Scaffold for boolean operations."""

    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)
        return obj

    def union(self, target, source):
        return target

    def union_all(self, target):
        return target
