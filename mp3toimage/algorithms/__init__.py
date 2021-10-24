"""Algorithms for generating the images."""
from mp3toimage.util import Point

DIRECTIONS = (
    Point(1, 0), Point(1, 1), Point(0, 1),
    Point(-1, 1), Point(-1, 0), Point(-1, -1),
    Point(0, -1), Point(1, -1)
)


def test_direction(pos: Point, direction: Point, resolution: Point) -> bool:
    """Check if we can move in that direction."""
    # Compute the next position (the spot we will go
    # if we continue in this direction).
    check_pos = Point(pos.x, pos.y)
    check_pos.x += direction.x
    check_pos.y += direction.y

    # Make sure we're not outside the bounds
    # of the image and if we are, flip directions
    if check_pos.x >= resolution.x or check_pos.x < 0:
        return False
    if check_pos.y >= resolution.y or check_pos.y < 0:
        return False
    return True
