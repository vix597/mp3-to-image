"""Algorithms for generating the images."""
import argparse

from mp3toimage.util import Point, Color

DIRECTIONS_45 = (
    Point(1, 0), Point(1, 1), Point(0, 1),
    Point(-1, 1), Point(-1, 0), Point(-1, -1),
    Point(0, -1), Point(1, -1)
)
DIRECTIONS_90 = (
    Point(1, 0), Point(0, 1),
    Point(-1, 0), Point(0, -1)
)


class PlaybackItem:
    """When doing live visualization, this represents a pixel."""

    def __init__(self, position: Point, color: Color, timestamp: float, duration: float):
        self.position = Point(position.x, position.y)
        self.color = color
        self.timestamp = timestamp
        self.duration = duration
        self.max_timestamp = self.timestamp + duration

    def __str__(self):
        return f"{self.position.x},{self.position.y},{self.color},{self.timestamp},{self.duration}"

    def __eq__(self, o: object) -> bool:
        return self.position.x == o.position.x and\
               self.position.y == o.position.y

    def __hash__(self) -> int:
        return hash(self.position)


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


def update_position(
    pos: Point, direction: Point, resolution: Point,
    args: argparse.Namespace, turn_amnt: int,
    directions: tuple, direction_idx: int) -> Point:
    """Update the pos or direction based on the input pos and direction."""

    if args.wrap_collisions or args.collide_180:
        check_pos = Point(pos.x, pos.y)
        check_pos.x += direction.x
        check_pos.y += direction.y

    if args.wrap_collisions:
        # Wrap if we're outside the bounds
        if check_pos.x >= resolution.x:
            pos.x = 0
        elif check_pos.x < 0:
            pos.x = resolution.x - 1

        if check_pos.y >= resolution.y:
            pos.y = 0
        elif check_pos.y < 0:
            pos.y = resolution.y - 1
        return pos, direction

    if args.collide_180:
        if check_pos.x >= resolution.x or check_pos.x < 0:
            direction.x *= -1
        if check_pos.y >= resolution.y or check_pos.y < 0:
            direction.y *= -1
        return pos, direction

    # If that direction won't work, keep going until we get one that will
    while not test_direction(pos, direction, resolution):
        direction_idx += turn_amnt
        direction_idx = direction_idx % len(directions)
        direction = directions[direction_idx]

    return pos, direction