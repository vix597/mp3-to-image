# MP3 To Image

An MP3 to image converter

# Installation

_Tested with Python 3.9.7 64-bit on Windows 10. The command will be for a Windows setup but it should also work on Linux with slight modification to the environment setup steps._

1. Install Python
1. Create a virtual environment: `python -m venv ./venv`
1. Activate the environment (from PowerShell): `./venv/Scripts/Activate.ps1`
1. Install the dependencies: `pip install -r requirements.txt`
1. You will also need `pyaudio` (for visualizations). I don't have a build environment on Windows so I found `pipwin` to be helpful:

    ```PowerShell
    pip install pipwin
    pipwin install pyaudio
    ```

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

    UPDATE
    ```
