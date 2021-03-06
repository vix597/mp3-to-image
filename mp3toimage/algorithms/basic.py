"""A basic algorithm."""
import argparse
import numpy as np
from typing import List

from mp3toimage.song import SongImage
from mp3toimage.util import Point, Color
from mp3toimage.algorithms import DIRECTIONS_45, DIRECTIONS_90, update_position, PlaybackItem


def generate_image(pixels: np.ndarray, song: SongImage, args: argparse.Namespace, pb_list: List[PlaybackItem] = None) -> None:
    """Walk the image."""
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
        pixel_changed = False
        if not beat and pixel == Color.transparent():
            pixels[pos.y][pos.x] = args.off_beat_color.as_tuple()
            pixel_changed = True
        elif pixel == Color.transparent() or pixel == args.off_beat_color:
            pixels[pos.y][pos.x] = args.beat_color.as_tuple()
            pixel_changed = True

        if pixel_changed and pb_list is not None:
            pb_list.append(PlaybackItem(pos, Color.from_tuple(pixels[pos.y][pos.x]), timestamp, song.pixel_time))

        # Try to choose a direction
        if amp > 0:
            turn_amnt = 1
        else:
            turn_amnt = -1

        direction_idx += turn_amnt

        # Turn more if it's above average
        if amp > song.overall_avg_amplitude:
            direction_idx += 2
        elif amp < (song.overall_avg_amplitude * -1):
            direction_idx -= 2

        direction_idx = direction_idx % len(directions)

        # Update the current direction
        direction = directions[direction_idx]
        pos, direction = update_position(pos, direction, song.resolution, args, turn_amnt, directions, direction_idx)

        # Do the real update to the position now that
        # we know it will be valid.
        pos.x += direction.x
        pos.y += direction.y
