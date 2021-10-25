"""An algorithm using the Fibonacci sequence to choose direction that takes tighter turns than fib."""
import argparse
import numpy as np
from typing import Iterator, List

from mp3toimage.song import SongImage
from mp3toimage.util import Point, Color
from mp3toimage.algorithms import DIRECTIONS_45, DIRECTIONS_90, PlaybackItem, update_position


def fib() -> Iterator[int]:
    """Fibonacci sequence."""
    a, b = 0, 1
    while 1:
        yield a
        a, b = b, a + b


def generate_image(pixels: np.ndarray, song: SongImage, args: argparse.Namespace, pb_list: List[PlaybackItem] = None) -> None:
    """Walk the image."""
    seq = fib()
    pos = Point(0, 0)
    if args.start_middle:
        pos = Point(int(song.resolution.x / 2), int(song.resolution.y / 2))

    directions = DIRECTIONS_45
    if args.four_directions:
        directions = DIRECTIONS_90

    direction_idx = 0
    direction = directions[direction_idx]

    for idx in range(song.num_pixels):
        beat, amp, timestamp = song.get_info_at_pixel(idx)
        pixel = Color.from_tuple(pixels[pos.y][pos.x])

        # Set the color
        if not beat and pixel == Color.transparent():
            pixels[pos.y][pos.x] = args.off_beat_color.as_tuple()
        elif pixel == Color.transparent() or pixel == args.off_beat_color:
            pixels[pos.y][pos.x] = args.beat_color.as_tuple()

        if pb_list is not None:
            pb_list.append(PlaybackItem(pos, Color.from_tuple(pixels[pos.y][pos.x]), timestamp, song.pixel_time))

        # Try to choose a direction
        if amp > 0:
            turn_amnt = next(seq)
        else:
            turn_amnt = (next(seq) * -1)

        direction_idx += turn_amnt
        direction_idx = direction_idx % len(directions)

        # Update the current direction
        direction = directions[direction_idx]
        pos, direction = update_position(pos, direction, song.resolution, args, turn_amnt, directions, direction_idx)

        # Do the real update to the position now that
        # we know it will be valid.
        pos.x += direction.x
        pos.y += direction.y
