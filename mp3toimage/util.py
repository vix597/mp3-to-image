"""Shared utility methods and classes."""
from typing import Tuple

import numpy as np


class Point:
    """A class with an x and y attribute to represent a point."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash(f"{self.x},{self.y}")


class Color:
    """A class to represent a color."""

    def __init__(self, r, g, b, a):
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    def as_tuple(self) -> Tuple[int, int, int, int]:
        return (self.red, self.green, self.blue, self.alpha)

    @classmethod
    def transparent(cls):
        return cls(0, 0, 0, 0)

    @classmethod
    def from_tuple(cls, as_tuple: Tuple[int, int, int, int]) -> object:
        return cls(as_tuple[0], as_tuple[1], as_tuple[2], as_tuple[3])

    def __eq__(self, other: object) -> bool:
        return self.red == other.red and\
               self.green == other.green and\
               self.blue == other.blue and\
               self.alpha == other.alpha

    def __str__(self):
        return f"{self.red},{self.green},{self.blue},{self.alpha}"


def generate_pixels(resolution: Point) -> np.ndarray:
    """Generate transparent pixels for an image."""
    pixels = []

    for _row in range(resolution.y):
        cur_row = []
        for _col in range(resolution.x):
            cur_row.append(Color.transparent().as_tuple())
        pixels.append(cur_row)

    return np.array(pixels, dtype=np.uint8)