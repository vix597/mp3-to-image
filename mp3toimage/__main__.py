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
    out_file += f"-{resolution.x}x{resolution.y}.png"
    out_path = os.path.join(args.out_dir, out_file)

    # Process the song
    song = SongImage(args.song, resolution)

    # Get an array of transparent pixels
    img_pixels = generate_pixels(resolution)

    # Edit the pixels in place based on the song
    ALGORITHMS[args.alg].generate_image(
        img_pixels, song, args.beat_color,
        args.off_beat_color, overwrite=not args.no_color_overwrite)

    # Create the image from our multi-dimmensional array of pixels
    img = Image.fromarray(img_pixels)
    img.save(out_path)


def main():
    """Entry point."""
    global ALGORITHMS

    # Discover algorithm plugins and set the transparent color
    ALGORITHMS = [importlib.import_module(name) for _finder, name, _ispkg in iter_namespace(mp3toimage.algorithms)]

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
        "--no-color-overwrite", action="store_true",
        help="Don't change the color of a pixel once it's set")
    parser.add_argument(
        "--alg", action="store", type=int, default=0,
        help=f"Which algorithm to use. A number between 0 and {len(ALGORITHMS) - 1}")
    parser.add_argument(
        "--out-dir", action="store", default=".",
        help="The output directory (default current directory)")
    args = parser.parse_args()

    _, song_ext = os.path.splitext(args.song)

    # Input validation
    if not os.path.exists(args.song) or \
       not os.path.isfile(args.song) or \
       not song_ext in (".mp3", ".m4a"):
        print("An .mp3 or .m4a file is required.")
        sys.exit(1)

    if args.alg < 0 or args.alg > (len(ALGORITHMS) - 1):
        print(f"Invalid algorithm index. Must be a value between 0 and {len(ALGORITHMS - 1)}")
        sys.exit(1)

    # Validate colors
    try:
        r, g, b = args.beat_color.split(",")
        args.beat_color = Color(int(r), int(g), int(b), 255)
        r, g, b = args.off_beat_color.split(",")
        args.off_beat_color = Color(int(r), int(g), int(b), 255)
    except ValueError as exc:
        print(f"Invalid color format. Expected <num>,<num>,<num>: {exc}")
        sys.exit(1)

    for res in args.resolution:
        # Validate resolution
        try:
            x, y = res.split("x")
            resolution = Point(int(x), int(y))
        except ValueError as exc:
            print(f"Invalid resolution format. Expected <num>x<num> (e.g. 512x512): {exc}")
            sys.exit(1)

        generate_image(resolution, args)


if __name__ == "__main__":
    main()