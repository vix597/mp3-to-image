"""Analyze an mp3 file and pull something meaningful out."""
import os
import sys
import math
import argparse

import librosa


def main():
    """Entry Point."""
    parser = argparse.ArgumentParser("Analyze an MP3")
    parser.add_argument("-f", "--filename", action="store", help="Path to an .mp3 file", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.filename) or not os.path.isfile(args.filename) or not args.filename.endswith(".mp3"):
        print("An .mp3 file is required.")
        sys.exit(1)

    # Get the song duration
    duration = librosa.get_duration(filename=args.filename)

    # Get the estimated tempo of the song
    y, sr = librosa.load(args.filename, duration=duration)
    onset_env = librosa.onset.onset_strength(y, sr=sr)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
    bps = tempo / 60.0  # beats per second
    estimated_num_beats = duration * bps
    print(f"Estimated BPM: {tempo}")
    print(f"Estimated BPS: {bps}")
    print(f"Should be about {estimated_num_beats} beats in the song.")

    # The image we're generating is going to be 512x512 (or 262,144) pixels.
    # So let's break the duration down so that each pixel represents some
    # amount of song time.
    num_pixels = 512 * 512
    pixel_time = duration / num_pixels
    print(f"Each pixel represents {pixel_time} seconds of song")

    # Now we just need 2 more things
    # 1. a way to get "beat" or "no beat" for a given pixel
    # 2. a way to get the amplitude of the waveform for a given pixel
    beats = 0
    for pixel_idx in range(num_pixels):
        song_time = pixel_idx * pixel_time

        # To figure out if it's a beat, let's just round and see if it's evenly divisible
        song_time = math.floor(song_time)
        if song_time and math.ceil(bps) % song_time == 0:
            beats += 1

    print(f"Found {beats} pixels that land on a beat")


if __name__ == "__main__":
    main()