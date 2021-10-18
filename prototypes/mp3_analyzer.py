"""Analyze an mp3 file and pull something meaningful out."""
import os
import sys
import math
import argparse

import librosa
import numpy as np
import matplotlib.pyplot as plt


def main():
    """Entry Point."""
    parser = argparse.ArgumentParser("Analyze an MP3")
    parser.add_argument(
        "-f", "--filename", action="store",
        help="Path to an .mp3 file", required=True)
    args = parser.parse_args()

    # Input validation
    if not os.path.exists(args.filename) or \
       not os.path.isfile(args.filename) or \
       not args.filename.endswith(".mp3"):
        print("An .mp3 file is required.")
        sys.exit(1)

    # Get the song duration
    duration = librosa.get_duration(filename=args.filename)

    # Get the estimated tempo of the song
    time_series, sample_rate = librosa.load(args.filename)
    onset_env = librosa.onset.onset_strength(time_series, sr=sample_rate)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sample_rate)
    bps = tempo / 60.0  # beats per second

    # The image we're generating is going to be 512x512 (or 262,144) pixels.
    # So let's break the duration down so that each pixel represents some
    # amount of song time.
    num_pixels = 512 * 512
    pixel_time = duration / num_pixels
    samples_per_pixel = math.floor(len(time_series) / num_pixels)

    if not samples_per_pixel:
        print(f"Song not long enough. Not enough samples to make the image.")
        sys.exit(1)

    print(f"Each pixel represents {pixel_time} seconds of song")
    print(f"Each pixel represents {samples_per_pixel} samples of song")

    # Now we just need 2 more things
    # 1. a way to get "beat" or "no beat" for a given pixel
    # 2. a way to get the amplitude of the waveform for a given pixel
    beats = 0
    avg_amps = []
    for pixel_idx in range(num_pixels):
        song_time = pixel_idx * pixel_time

        # To figure out if it's a beat, let's just round and
        # see if it's evenly divisible
        song_time = math.floor(song_time)
        if song_time and math.ceil(bps) % song_time == 0:
            beats += 1

        # Now let's figure out the average amplitude of the
        # waveform for this pixel's time
        sample_idx = pixel_idx * samples_per_pixel
        samps = time_series[sample_idx:sample_idx + samples_per_pixel]
        avg_amplitude = np.array(samps ).mean()
        avg_amps.append(avg_amplitude)

    print(f"Found {beats} pixels that land on a beat")

    # Plot the average amplitudes and make sure it still looks
    # somewhat song-like
    xaxis = np.arange(0, num_pixels, 1)
    plt.plot(xaxis, np.array(avg_amps))
    plt.xlabel("Pixel index")
    plt.ylabel("Average Pixel Amplitude")
    plt.title(args.filename)
    plt.show()


if __name__ == "__main__":
    main()