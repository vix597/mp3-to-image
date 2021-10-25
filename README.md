# MP3 To Image

An MP3 to image converter

# Installation

_Tested with Python 3.9.7 64-bit on Windows 10. The command will be for a Windows setup but it should also work on Linux with slight modification to the environment setup steps._

1. Install Python
1. Create a virtual environment: `python -m venv ./venv`
1. Activate the environment (from PowerShell): `./venv/Scripts/Activate.ps1`
1. Install the dependencies: `pip install -r requirements.txt`
1. Run the app and get help: `python -m mp3toimage -h`

## Examples

* Generate a 512x512 favicon in the current directory from the song "Brass Monkey" by the Beastie Boys:

    ```PowerShell
    python -m mp3toimage -s .\brass_monkey.mp3
    ```

* Generate 7 different resolution images from the song "Brass Monkey" by the Beastie Boys with the "wrap" algorithm and save the results in the current directory:

    ```PowerShell
    python -m mp3toimage -s .\brass_monkey.mp3 -r 1920x1080 -r 1024x1024 -r 512x512 -r 32x32 -r 48x48 -r 96x96 -r 128x128 --alg wrap
    ```

* Full help output:

    ```PowerShell
    python -m mp3toimage -h
    usage: Convert an MP3 into an image [-h] -s SONG [-r RESOLUTION] [-b BEAT_COLOR] [-o OFF_BEAT_COLOR] [--alg {basic,fib,garbage,middle,wrap}] [--out-dir OUT_DIR]

    optional arguments:
      -h, --help            show this help message and exit
      -s SONG, --song SONG  Path to an .mp3 file
      -r RESOLUTION, --resolution RESOLUTION
                              One or more resolutions for the images in the form <num>x<num>
      -b BEAT_COLOR, --beat-color BEAT_COLOR
                              Color used for beat pixels
      -o OFF_BEAT_COLOR, --off-beat-color OFF_BEAT_COLOR
                              Color used for off-beat pixels
      --alg {basic,fib,garbage,middle,wrap}
                              Which algorithm to use. One of: dict_keys(['basic', 'fib', 'garbage', 'middle', 'wrap'])
      --out-dir OUT_DIR     The output directory (default current directory)
    ```
