"""Visualize a song."""
import tkinter
from typing import List

from mp3toimage.util import Point
from mp3toimage.algorithms import PlaybackItem

#: Time per pixel in milliseconds
PIXEL_TIME = 16


def draw(canvas: tkinter.Canvas, img:tkinter.PhotoImage, pb_list: List[PlaybackItem]):
    """Draw to the screen."""
    if not pb_list:
        return

    item = pb_list.pop(0)
    img.put("#ffffff", (item.position.x, item.position.y))
    canvas.after(PIXEL_TIME, draw, canvas, img, pb_list)


def visualize_song(filename: str, resolution: Point, pb_list: List[PlaybackItem], pixel_time: float) -> None:
    """Create a window, play the song, and visualize drawing the image."""
    global PIXEL_TIME

    window = tkinter.Tk()
    canvas = tkinter.Canvas(window, width=resolution.x, height=resolution.y, bg="#000000")
    canvas.pack()
    img = tkinter.PhotoImage(width=resolution.x, height=resolution.y)
    _ = canvas.create_image((resolution.x/2, resolution.y/2), image=img, state="normal")

    PIXEL_TIME = pixel_time / 1000

    canvas.after(1000, draw, canvas, img, pb_list)
    window.mainloop()
