import numpy as np
from PIL import Image
from typing import Tuple

# Let's make a red square
SQUARE_COLOR = (255, 0, 0, 255)

# The recommended minimum size from WordPress
ICON_SIZE = (512, 512)


def get_song_info_for_pixel(pixel_idx: int) -> Tuple[bool, float]:
    """Get song info for the pixel at the provided pixel index."""


def generate_pixels(resolution: Tuple[int, int]) -> np.ndarray:
    """Generate pixels of an image with the provided resolution."""
    pixels = []

    # Eventually we'll extend this to generate an image one pixel at a time
    # based on an input song.
    for _row in range(resolution[1]):
        cur_row = []
        for _col in range(resolution[0]):
            cur_row.append(SQUARE_COLOR)
        pixels.append(cur_row)

    return np.array(pixels, dtype=np.uint8)


def main():
    """Entry point."""
    parser = argparse.ArgumentParser("Convert an MP3 into an image")
    parser.add_argument(
        "-s", "--song", action="store",
        help="Path to an .mp3 file", required=True)
    args = parser.parse_args()

    # For now, just make a solid color square, one pixel at a time,
    # for each resolution of our image.
    img_pixels = generate_pixels(ICON_SIZE)

    # Create the image from our multi-dimmensional array of pixels
    img = Image.fromarray(img_pixels)
    img.save('favicon.png', sizes=ICON_SIZE)


if __name__ == "__main__":
    main()