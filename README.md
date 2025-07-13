# dota2-auto-accept

This is a simple tool which automatically accepts a Dota 2 match and notifies you that one was found via Pushbullet.

Ready checks are also automatically accepted.

Only Windows is currently supported.


## Requirements

* python 3.8+
* uv
* [tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

## Setup/Installation

**IMPORTANT**: If using the UB-Mannheim installer for tesseract, you will need to manually add the directory containing tesseract.exe (likely C:\Program Files\Tesseract-OCR) to PATH.

To enable notifications via Pushbullet, create a file '.pushbullet-token' in the project directory containing your access token.

## Usage

    cd dota2-auto-accept
    uv run python main.py

### Options

Only one option is currently available, `--notify-ready`. If passed, notifications will be also be sent when a ready check is accepted.