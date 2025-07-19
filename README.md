# dota2-auto-accept

This is a simple tool which automatically accepts a Dota 2 match and notifies you that one was found via Pushbullet.

Ready checks are also automatically accepted.

Only Windows is currently supported.

## Requirements

* [Python](https://www.python.org/downloads/) 3.8 or later
* [uv](https://docs.astral.sh/uv/getting-started/installation/)
* [tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

## Setup/Installation

**IMPORTANT**: If using the UB-Mannheim installer for tesseract, you will need to manually add the directory containing `tesseract.exe` (likely `C:\Program Files\Tesseract-OCR`) to PATH.

To enable notifications via Pushbullet, create a file `.pushbullet-token` in the project directory containing your access token.

## Usage

**IMPORTANT**: Ensure that the game is on your primary monitor, and takes up the entire screen. Otherwise, the script may not work correctly.

Simply start the game, and run the script via `uv`:

    cd dota2-auto-accept
    uv run python main.py

Dependencies other than those listed in the requirements section will be installed automatically.

### Options

Only one option is currently available, `--notify-ready`. If passed, notifications will be also be sent when a ready check is accepted.