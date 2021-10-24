"""A basic algorithm."""
import numpy as np

from mp3toimage.song import SongImage
from mp3toimage.util import Point, Color
from mp3toimage.algorithms import test_direction, DIRECTIONS


def generate_image(
    pixels: np.ndarray, song: SongImage, beat_color: Color,
    off_beat_color: Color, overwrite: bool = True) -> None:
    """Walk the image."""
    pos = Point(0, 0)
    direction_idx = 0
    direction = DIRECTIONS[direction_idx]

    for idx in range(song.num_pixels):
        beat, amp = song.get_info_at_pixel(idx)
        pixel = Color.from_tuple(pixels[pos.x][pos.y])

        # Set the color
        if not beat and (pixel == Color.transparent() or overwrite):
            pixels[pos.x][pos.y] = off_beat_color.as_tuple()
        elif overwrite or (pixel == Color.transparent() or pixel == off_beat_color):
            pixels[pos.x][pos.y] = beat_color.as_tuple()

        # Try to choose a direction
        if amp > 0:
            direction_idx += 1
        else:
            direction_idx -= 1
        direction_idx = direction_idx % len(DIRECTIONS)

        # Update the current direction
        direction = DIRECTIONS[direction_idx]

        # If that direction won't work, keep going until we get one that will
        while not test_direction(pos, direction, song.resolution):
            if amp > 0:
                direction_idx += 1
            else:
                direction_idx -= 1
            direction_idx = direction_idx % len(DIRECTIONS)
            direction = DIRECTIONS[direction_idx]

        # Do the real update to the position now that
        # we know it will be valid.
        pos.x += direction.x
        pos.y += direction.y
