import os
import sys
import math
import random
import argparse
import numpy as np
from PIL import Image
from typing import Tuple

import librosa
import numpy as np

# The recommended minimum size from WordPress
ICON_SIZE = (512, 512)


class NotEnoughSong(Exception):
    """There's just not enough song."""


class SongImage:
    """An object to hold all the song info."""

    def __init__(self, filename: str, resolution: Tuple[int, int]):
        self.filename = filename
        self.resolution = resolution
        #: Total song length in seconds
        self.duration = librosa.get_duration(filename=self.filename)
        #: The time series data (amplitudes of the waveform) and the sample rate
        self.time_series, self.sample_rate = librosa.load(self.filename)
        #: An onset envelop is used to measure BPM
        onset_env = librosa.onset.onset_strength(self.time_series, sr=self.sample_rate)
        #: Measure the tempo (BPM)
        self.tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=self.sample_rate)
        #: Convert to beats per second
        self.bps = self.tempo / 60.0
        #: Get the total number of pixels for the image
        self.num_pixels = self.resolution[0] * self.resolution[1]
        #: Get the amount of time each pixel will represent in seconds
        self.pixel_time = self.duration / self.num_pixels
        #: Get the number of whole samples each pixel represents
        self.samples_per_pixel = math.floor(len(self.time_series) / self.num_pixels)

        if not self.samples_per_pixel:
            raise NotEnoughSong(
                "Not enough song data to make an image "
                f"with resolution {self.resolution[0]}x{self.resolution[1]}")

    def get_info_at_pixel(self, pixel_idx: int) -> Tuple[bool, float]:
        """Get song info for the pixel at the provided pixel index."""
        beat = False
        song_time = pixel_idx * self.pixel_time

        # To figure out if it's a beat, let's just round and
        # see if it's evenly divisible
        song_time = math.floor(song_time)
        if song_time and math.ceil(self.bps) % song_time == 0:
            beat = True

        # Now let's figure out the average amplitude of the
        # waveform for this pixel's time
        sample_idx = pixel_idx * self.samples_per_pixel
        samps = self.time_series[sample_idx:sample_idx + self.samples_per_pixel]
        avg_amplitude = np.array(samps ).mean()
        return (beat, avg_amplitude)


def generate_pixels(resolution: Tuple[int, int], song: SongImage) -> np.ndarray:
    """Generate pixels of an image with the provided resolution."""
    pixels = []

    pixel_idx = 0
    for _row in range(resolution[1]):
        cur_row = []
        for _col in range(resolution[0]):
            # This is where we pick our color information for the pixel
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

            cur_row.append((r, g, b, a))
            pixel_idx += 1

        pixels.append(cur_row)

    return np.array(pixels, dtype=np.uint8)


def main():
    """Entry point."""
    parser = argparse.ArgumentParser("Convert an MP3 into an image")
    parser.add_argument(
        "-s", "--song", action="store",
        help="Path to an .mp3 file", required=True)
    parser.add_argument(
        "-o", "--output", action="store", required=True,
        help="Full path to the output PNG file.")
    args = parser.parse_args()

    # Input validation
    if not os.path.exists(args.song) or \
       not os.path.isfile(args.song) or \
       not args.song.endswith(".mp3"):
        print("An .mp3 file is required.")
        sys.exit(1)

    # For now, just make a solid color square, one pixel at a time,
    # for each resolution of our image.
    img_pixels = generate_pixels(ICON_SIZE, SongImage(args.song, ICON_SIZE))

    # Create the image from our multi-dimmensional array of pixels
    img = Image.fromarray(img_pixels)
    out_file = args.output
    if not out_file.endswith(".png"):
        out_file += ".png"
    img.save(out_file)


if __name__ == "__main__":
    main()