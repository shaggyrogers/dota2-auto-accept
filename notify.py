#!/usr/bin/env python3
"""
  notify.py
  =========

  Description:           Notification functionality
  Author:                Michael De Pasquale
  Creation Date:         2025-07-09
  Modification Date:     2025-07-09

"""


import logging
from pathlib import Path

import requests

LOG = logging.getLogger(__file__)
LOG.setLevel("DEBUG")

PUSHBULLET_TOKEN_PATH = Path("./.pushbullet-token")
PUSHBULLET_TOKEN = None


# Load pushbullet access token, if it exists
if PUSHBULLET_TOKEN_PATH.exists():
    with open(PUSHBULLET_TOKEN_PATH, "r") as file:
        PUSHBULLET_TOKEN = file.readline().strip()

    LOG.debug(f"Notifications enabled, token={PUSHBULLET_TOKEN}")

else:
    LOG.warning("Notifications disabled - .pushbullet-token is missing. See README.")


def sendNotification(title: str, body: str) -> None:
    """Send a push notification via pushbullet, with given title and body.
    Aborts immediately if no token was found.
    """
    if not PUSHBULLET_TOKEN:
        return

    requests.post(
        f"https://api.pushbullet.com/v2/pushes",
        json={
            "type": "note",
            "title": title,
            "body": body,
        },
        headers={
            "Access-Token": PUSHBULLET_TOKEN,
            "Content-Type": "application/json",
        },
    )
