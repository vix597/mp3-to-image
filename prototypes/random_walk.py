"""Generate an image by randomly walking."""
import random

import numpy as np
from PIL import Image

WIDTH = 64
HEIGHT = 64
INITIAL_COLOR = (0, 0, 0, 0)  # Transparent
NEW_COLOR = (255, 0, 0, 255)  # Red

class Point:
    """A class with an x and y attribute to represent a point."""
    def __init__(self, x, y):
        self.x = x
        self.y = y


def generate_pixels() -> np.ndarray:
    """Generate pixels of an image with the provided resolution."""
    pixels = []

    for _row in range(HEIGHT):
        cur_row = []
        for _col in range(WIDTH):
            cur_row.append(INITIAL_COLOR)
        pixels.append(cur_row)

    return np.array(pixels, dtype=np.uint8)


def walk_pixels(pixels: np.ndarray):
    """Walk the image"""
    pos = Point(0, 0)
    direction = Point(1, 0)  # Start left-to-right

    for idx in range(WIDTH * HEIGHT):
        if idx % 50 == 0:
            # Choose a random direction
            direction = random.choice([
                Point(1, 0),   # Left-to-right
                Point(0, 1),   # Top-to-bottom
                Point(-1, 0),  # Right-to-left
                Point(0, -1),  # Bottom-to-top
                Point(1, 1),   # Left-to-right diaganal
                Point(-1, -1)  # Right-to-left diaganal
            ])

        # Set the pixel at the current position to red
        pixels[pos.y][pos.x] = NEW_COLOR

        # Compute the next position (the spot we will go
        # if we continue in this direction).
        check_pos = Point(pos.x, pos.y)
        check_pos.x += direction.x
        check_pos.y += direction.y

        # Make sure we're not outside the bounds
        # of the image and if we are, flip directions
        if check_pos.x >= WIDTH or check_pos.x < 0:
            direction.x *= -1
        if check_pos.y >= HEIGHT or check_pos.y < 0:
            direction.y *= -1

        # Do the real update to the position now that
        # we know it will be valid.
        pos.x += direction.x
        pos.y += direction.y


def main():
    """Entry point."""
    num_pixels = WIDTH * HEIGHT

    # Generate the pixels like before
    pixels = generate_pixels()

    # Walk the generated 2D array of pixels
    # changing certain ones to red based on
    # the random walker (edits the pixels
    # variable in place).
    walk_pixels(pixels)

    # Create the image
    img = Image.fromarray(pixels)
    img.save('favicon.png')


if __name__ == "__main__":
    main()