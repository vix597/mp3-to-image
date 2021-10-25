"""Main module for mp3toimage."""
import os
import sys
import pkgutil
import argparse
import importlib

from PIL import Image

import mp3toimage.algorithms
from mp3toimage.song import SongImage
from mp3toimage.util import generate_pixels, Point, Color

ALGORITHMS = None


def iter_namespace(ns_pkg):
    """Iterate a namespace."""
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def generate_image(resolution: Point, args: argparse.Namespace):
    """Generate an image from a song."""
    out_file, _ = os.path.splitext(os.path.basename(args.song))
    out_file += f"-{resolution.x}x{resolution.y}-alg-{args.alg}.png"
    out_path = os.path.join(args.out_dir, out_file)

    # Process the song
    song = SongImage(args.song, resolution)

    # Get an array of transparent pixels
    img_pixels = generate_pixels(resolution)

    # Edit the pixels in place based on the song
    ALGORITHMS[args.alg].generate_image(img_pixels, song, args)

    # Create the image from our multi-dimmensional array of pixels
    img = Image.fromarray(img_pixels)
    img.save(out_path)


def main():
    """Entry point."""
    global ALGORITHMS

    # Discover algorithm plugins and set the transparent color
    ALGORITHMS = {
        name.split(".")[-1]: importlib.import_module(name) for _finder, name, _ispkg in iter_namespace(mp3toimage.algorithms)
    }

    parser = argparse.ArgumentParser("Convert an MP3 into an image")
    parser.add_argument(
        "-s", "--song", action="store",
        help="Path to an .mp3 file", required=True)
    parser.add_argument(
        "-r", "--resolution", action="append", default=["512x512"],
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
    args.resolution = list(set(args.resolution))

    _, song_ext = os.path.splitext(args.song)

    # Validate the song file
    if not os.path.exists(args.song) or \
       not os.path.isfile(args.song) or \
       not song_ext in (".mp3", ".m4a"):
        print("An .mp3 or .m4a file is required.")
        sys.exit(1)

    # Validate the colors
    try:
        r, g, b = args.beat_color.split(",")
        args.beat_color = Color(int(r), int(g), int(b), 255)
        r, g, b = args.off_beat_color.split(",")
        args.off_beat_color = Color(int(r), int(g), int(b), 255)
    except ValueError as exc:
        print(f"Invalid color format. Expected <num>,<num>,<num>: {exc}")
        sys.exit(1)

    for res in args.resolution:
        # Validate the resolution
        try:
            x, y = res.split("x")
            resolution = Point(int(x), int(y))
        except ValueError as exc:
            print(f"Invalid resolution format. Expected <num>x<num> (e.g. 512x512): {exc}")
            sys.exit(1)

        # Generate the image
        generate_image(resolution, args)


if __name__ == "__main__":
    main()