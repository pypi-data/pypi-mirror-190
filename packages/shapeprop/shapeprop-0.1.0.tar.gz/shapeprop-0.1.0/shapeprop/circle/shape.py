import math
from ..triangle.shape import area as tri_area


def area(radius):
    """Calculates area of circle"""
    return math.pi * (radius ** 2)


def circumference(radius):
    """Calculates the circumference of a circle."""
    return 2 * math.pi * radius


def triangle_area(base, height):
    return tri_area(base, height)
