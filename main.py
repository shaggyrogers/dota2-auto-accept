#!/usr/bin/env python3
"""
  auto-accept.py
  ==============

  Description:           TODO
  Author:                Michael De Pasquale
  Creation Date:         2025-07-08
  Modification Date:     2025-07-09

"""

import logging
from pathlib import Path
import sys
import time

from PIL import Image
import pyautogui
import pygetwindow

from find_accept import findAcceptOrReady
from notify import sendNotification

logging.basicConfig()
LOG = logging.getLogger()
LOG.setLevel("DEBUG")

# Delay between checks
POLLING_RATE = 5

# FIXME: Add check here to ensure tesseract is in PATH.
# If not, the script will fail suddenly when the Accept button appears...


def poll() -> None:
    if not (window := pygetwindow.getWindowsWithTitle("Dota 2")):
        LOG.warning("Failed to find game window!")

        return

    window = window[0]

    # Focus window to ensure it's not behind anything
    # This fails sometimes (apparently with ERROR_SUCCESS)
    try:
        window.activate()

    except pygetwindow.PyGetWindowException as ex:
        # Probably better to explicitly check code is 0
        LOG.warning(f"Failed to activate game window, continuing: {repr(ex)}")

    # FIXME: pyautogui.screenshot() only includes the primary monitor? playing the game on another monitor will likely
    # result in silent failure. As a hacky guard against this, just check the top left of the window is at (0, 0)
    assert window.topleft.x == 0 and window.topleft.y == 0
    screenshot = pyautogui.screenshot()

    if not (btnInfo := findAcceptOrReady(screenshot)):
        LOG.debug("No button found, skipping...")

        return

    # Button found, click and send appropriate notification if accept
    assert btnInfo[0] in ("accept", "ready"), f"Unexpected button text: {btnInfo[0]}"
    LOG.info(f"Found {btnInfo[0]} button @ {btnInfo[1:]}!")
    pyautogui.click(btnInfo[1], btnInfo[2])

    if btnInfo[0] == "accept":
        sendNotification("Dota 2", "A game has been accepted!")


def main(*args) -> None:
    LOG.info(f"Started. Please ensure the game window is visible. Polling every {POLLING_RATE}s.")

    while True:
        time.sleep(POLLING_RATE)

        try:
            poll()

        except Exception as ex:
            LOG.exception("Unhandled exception!")
            sendNotification("Dota 2", f"An error occurred: {repr(ex)}")

            return 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv))