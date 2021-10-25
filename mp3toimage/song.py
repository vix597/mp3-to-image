"""Classes/helpers for parsing song files"""
import math
import warnings
from typing import Tuple

import librosa
import numpy as np

from mp3toimage.util import Point


class NotEnoughSong(Exception):
    """There's just not enough song."""


class SongImage:
    """An object to hold all the song info."""

    #: Cache the song analysis to speed up processing when generating
    #: images from the same song with multiple resolutions.
    _song_cache = {}

    def __init__(self, filename: str, resolution: Point):
        #: The song file path
        self.filename = filename
        #: The image resolution
        self.resolution = resolution
        #: Load the song fresh or from the cache
        self._load_song()
        #: Convert to beats per second
        self.bps = self.tempo / 60.0
        #: Get the total number of pixels for the image
        self.num_pixels = self.resolution.x * self.resolution.y
        #: Get the amount of time each pixel will represent in seconds
        self.pixel_time = self.duration / self.num_pixels
        #: Get the number of whole samples each pixel represents
        self.samples_per_pixel = math.floor(len(self.time_series) / self.num_pixels)
        #: Overall average amplitude
        self.overall_avg_amplitude = np.absolute(self.time_series).mean()

        if not self.samples_per_pixel:
            raise NotEnoughSong(
                "Not enough song data to make an image "
                f"with resolution {self.resolution.x}x{self.resolution.y}")

    def _load_song(self) -> None:
        """Load a song (use the cache if it's already loaded)."""
        if self.filename in self._song_cache:
            self.duration = self._song_cache[self.filename]["duration"]
            self.time_series = self._song_cache[self.filename]["time_series"]
            self.sample_rate = self._song_cache[self.filename]["sample_rate"]
            self.tempo = self._song_cache[self.filename]["tempo"]
            return

        #: Total song length in seconds
        self.duration = librosa.get_duration(filename=self.filename)

        # Suppress the user warning for loading with audioread
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            #: The time series data (amplitudes of the waveform) and the sample rate
            self.time_series, self.sample_rate = librosa.load(self.filename)

        #: An onset envelop is used to measure BPM
        onset_env = librosa.onset.onset_strength(self.time_series, sr=self.sample_rate)
        #: Measure the tempo (BPM)
        self.tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=self.sample_rate)

        # Update the cache
        self._song_cache[self.filename] = {
            "duration": self.duration,
            "time_series": self.time_series,
            "sample_rate": self.sample_rate,
            "tempo": self.tempo
        }

    def get_info_at_pixel(self, pixel_idx: int) -> Tuple[bool, float]:
        """Get song info for the pixel at the provided pixel index."""
        beat = False
        song_time = pixel_idx * self.pixel_time

        # To figure out if it's a beat, let's just round and
        # see if it's evenly divisible
        floor_song_time = math.floor(song_time)
        if floor_song_time and math.ceil(self.bps) % floor_song_time == 0:
            beat = True

        # Now let's figure out the average amplitude of the
        # waveform for this pixel's time
        sample_idx = pixel_idx * self.samples_per_pixel
        samps = self.time_series[sample_idx:sample_idx + self.samples_per_pixel]
        avg_amplitude = np.array(samps).mean()
        return (beat, avg_amplitude, song_time)
