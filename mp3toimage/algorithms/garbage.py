"""A bad algorithm that does a bad job."""
import random

import numpy as np

from mp3toimage.song import SongImage
from mp3toimage.util import Color


def generate_image(pixels: np.ndarray, song: SongImage, beat_color: Color, off_beat_color: Color) -> None:
    """Generate pixels of an image with the provided resolution."""

    pixel_idx = 0
    for col in range(song.resolution.x):
        for row in range(song.resolution.y):
            beat, amp = song.get_info_at_pixel(pixel_idx)
            r = g = b = a = 0
            if beat and amp > 0:
                a = 255
            elif amp > 0:
                a = 125

            amp = abs(int(amp))

            # Randomly pick a primary color
            choice = random.choice([0, 1, 2])
            if choice == 0:
                r = amp
            elif choice == 1:
                g = amp
            else:
                b = amp

            pixels[col][row] = (r, g, b, a)
            pixel_idx += 1
