"""Main module for mp3toimage."""
import os
import sys
import pkgutil
import argparse
import importlib
from typing import List

from PIL import Image

import mp3toimage.algorithms
from mp3toimage.song import NotEnoughSong, SongImage
from mp3toimage.util import generate_pixels, Point, Color

VALID_SONG_EXTS = (".mp3", ".m4a", ".ogg", ".flac")
ALGORITHMS = None


def get_songs_from_dir(song_dir: str, recursive: bool = False) -> List[str]:
    """Get valid song files from a directory."""
    ret = []
    if recursive:
        for root, _dirs, files in os.walk(song_dir):
            for file in files:
                fpath = os.path.join(root, file)
                _, ext = os.path.splitext(file)
                if ext in VALID_SONG_EXTS:
                    ret.append(fpath)
    else:
        for file in os.listdir(song_dir):
            fpath = os.path.join(song_dir, file)
            _, ext = os.path.splitext(file)
            if ext in VALID_SONG_EXTS:
                ret.append(fpath)

    return ret


def validate_color(color: str) -> Color:
    """Validate the color string. Raises ValueError if invalid."""
    r, g, b = color.split(",")
    return Color(int(r), int(g), int(b), 255)


def iter_namespace(ns_pkg):
    """Iterate a namespace."""
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def generate_image(resolution: Point, song_path: str, args: argparse.Namespace):
    """Generate an image from a song."""
    pb_file = None
    out_file, _ = os.path.splitext(os.path.basename(song_path))
    out_file += f"-{resolution.x}x{resolution.y}"
    if args.wrap_collisions:
        out_file += "-wrap"
    if args.collide_180:
        out_file += "-collide180"
    if args.start_middle:
        out_file += "-middle"
    if args.four_directions:
        out_file += "-4dir"
    if args.playback:
        pb_file = os.path.join(args.out_dir, out_file + ".pb")
    out_file += f"-{args.alg}.png"
    out_path = os.path.join(args.out_dir, out_file)

    pb_list = [] if args.playback else None

    # Process the song
    song = SongImage(song_path, resolution)

    # Get an array of transparent pixels
    img_pixels = generate_pixels(resolution)

    # Edit the pixels in place based on the song
    ALGORITHMS[args.alg].generate_image(img_pixels, song, args, pb_list=pb_list)

    # Create the image from our multi-dimmensional array of pixels
    img = Image.fromarray(img_pixels)
    img.save(out_path)

    if pb_file and pb_list:
        with open(pb_file, "w") as fh:
            fh.write(os.path.abspath(song_path) + "\n")
            fh.write(f"{resolution.x},{resolution.y}\n")
            for item in pb_list:
                fh.write(str(item) + "\n")


def main():
    """Entry point."""
    global ALGORITHMS

    # Discover algorithm plugins and set the transparent color
    ALGORITHMS = {
        name.split(".")[-1]: importlib.import_module(name) for _finder, name, _ispkg in iter_namespace(mp3toimage.algorithms)
    }

    parser = argparse.ArgumentParser("Convert an MP3 into an image")
    parser.add_argument(
        "-s", "--song", action="append",
        help="Path to an .mp3 file. Can be called multiple times.", required=True)
    parser.add_argument(
        "--recursive", action="store_true",
        help="If any of the songs provided are directories, list files recursively.")
    parser.add_argument(
        "-r", "--resolution", action="append",
        help="One or more resolutions for the images in the form <num>x<num>")
    parser.add_argument(
        "-b", "--beat-color", action="store", default="255,221,74",
        help="Color used for beat pixels")
    parser.add_argument(
        "-o", "--off-beat-color", action="store", default="60,105,151",
        help="Color used for off-beat pixels")
    parser.add_argument(
        "--alg", action="store", default="basic", choices=ALGORITHMS.keys(),
        help=f"Which algorithm to use. One of: {ALGORITHMS.keys()}")
    parser.add_argument(
        "--start-middle", action="store_true",
        help="Set the start position in the middle of the image instead "
             "of the top-left corner.")
    parser.add_argument(
        "--out-dir", action="store", default=".",
        help="The output directory (default current directory)")
    parser.add_argument(
        "--four-directions", action="store_true",
        help="Use 4 directions (90 degree turns) instead of 8.")
    parser.add_argument(
        "--playback", action="store_true",
        help="Playback the visualization live with the song after it's generated.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--wrap-collisions", action="store_true",
        help="When the walker collides with the edge of the image, wrap "
             "around instead of changing directions.")
    group.add_argument(
        "--collide-180", action="store_true",
        help="When colliding with the edge of the image, flip direction "
             "180 degrees rather than turning to find a new valid direction.")

    args = parser.parse_args()
    if not args.resolution:
        args.resolution = ["512x512"]
    else:
        args.resolution = list(set(args.resolution))  # Remove duplicate resolutions

    # Validate the colors
    try:
        args.beat_color = validate_color(args.beat_color)
        args.off_beat_color = validate_color(args.off_beat_color)
    except ValueError as exc:
        print(f"Invalid color format. Expected <num>,<num>,<num>: {exc}")
        sys.exit(1)

    song_paths = []
    # Expand any song directories
    for song_path in args.song:
        if not os.path.exists(song_path):
            print(f"Warning: {song_path} - File not found.")
            continue
        if os.path.isdir(song_path):
            song_paths.extend(get_songs_from_dir(song_path, recursive=args.recursive))
        else:
            _, ext = os.path.splitext(song_path)
            if ext in VALID_SONG_EXTS:
                song_paths.append(song_path)
            else:
                print(f"Skipping: {song_path} - Unsupported file type.")

    if len(song_paths) == 0:
        print("No valid song files provided.")
        sys.exit(1)

    print(f"Discovered {len(song_paths)} song(s) to process. Press cnrl+c to cancel")

    try:
        for song_path in song_paths:
            print(f"Processing: {song_path}...", flush=True)
            for res in args.resolution:
                # Validate the resolution
                try:
                    x, y = res.split("x")
                    resolution = Point(int(x), int(y))
                except ValueError as exc:
                    print(f"Invalid resolution format. Expected <num>x<num> (e.g. 512x512): {exc}")
                    sys.exit(1)

                # Generate the image
                print(f"\t{res}...", end="", flush=True)
                try:
                    generate_image(resolution, song_path, args)
                    print("Done.", flush=True)
                except NotEnoughSong as exc:
                    print(f"Failed. {exc}", flush=True)
            print("Done.", flush=True)

    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()