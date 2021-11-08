# MP3 To Image

An MP3 to image converter. Code breakdown and sample images in [the associated blog post](https://seanlaplante.com/index.php/2021/10/27/creating-an-icon-from-a-song/). Why? ¯\_(ツ)_/¯.

# Installation

_Tested with Python 3.9.7 64-bit on Windows 10. The commands below will be for a Windows setup but it should also work on Linux with slight modification to the environment setup steps._

1. Install Python
1. Create a virtual environment: `python -m venv ./venv`
1. Activate the environment (from PowerShell): `./venv/Scripts/Activate.ps1`
1. Install the dependencies: `pip install -r requirements.txt`
1. Run the app and get help: `python -m mp3toimage -h`
1. To do live playback of the image generation you will need [Processing 4](https://processing.org/)
    1. Extract Processing
    1. Open it
    1. Navigate to and open `mp3toimage_visualizer\mp3toimage_visualizer.pde`
    1. Click the play button
    1. Select a `.pb` file generated by running the `mp3toimage` script with the `--playback` option

## Examples

* Generate a 512x512 favicon in the current directory from the song "Brass Monkey" by the Beastie Boys with default settings:

    ```PowerShell
    python -m mp3toimage -s .\brass_monkey.mp3
    ```

* Generate 7 different resolution images from the song "Brass Monkey" by the Beastie Boys with wrapping collisions, start in the middle, and save the results in the current directory:

    ```PowerShell
    python -m mp3toimage -s .\brass_monkey.mp3 -r 1920x1080 -r 1024x1024 -r 512x512 -r 32x32 -r 48x48 -r 96x96 -r 128x128 --wrap-collision --start-middle
    ```

* Generate a 1920x1080 resolution image from the song "Brass Monkey" by the Beastie Boys and output a playback file that can be used with the mp3toimage_visualizer

    ```PowerShell
    python -m mp3toimage -s .\brass_monkey.mp3 -r 1920x1080 --playback
    ```

* Full help output:

    ```
    usage: Convert an MP3 into an image [-h] -s SONG [--recursive] [-r RESOLUTION] [-b BEAT_COLOR] [-o OFF_BEAT_COLOR] [--alg {basic,basic_tight,fib,fib_tight,garbage}] [--start-middle] [--out-dir OUT_DIR] [--four-directions] [--playback] [--wrap-collisions | --collide-180]

    optional arguments:
      -h, --help            show this help message and exit
      -s SONG, --song SONG  Path to an .mp3 file. Can be called multiple times.
      --recursive           If any of the songs provided are directories, list files recursively.
      -r RESOLUTION, --resolution RESOLUTION
                              One or more resolutions for the images in the form <num>x<num>
      -b BEAT_COLOR, --beat-color BEAT_COLOR
                              Color used for beat pixels
      -o OFF_BEAT_COLOR, --off-beat-color OFF_BEAT_COLOR
                              Color used for off-beat pixels
      --alg {basic,basic_tight,fib,fib_tight,garbage}
                              Which algorithm to use. One of: dict_keys(['basic', 'basic_tight', 'fib', 'fib_tight', 'garbage'])
      --start-middle        Set the start position in the middle of the image instead of the top-left corner.
      --out-dir OUT_DIR     The output directory (default current directory)
      --four-directions     Use 4 directions (90 degree turns) instead of 8.
      --playback            Playback the visualization live with the song after it's generated.
      --wrap-collisions     When the walker collides with the edge of the image, wrap around instead of changing directions.
      --collide-180         When colliding with the edge of the image, flip direction 180 degrees rather than turning to find a new valid direction.
    ```
