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

from PIL import Image

from find_accept import findAccept

logging.basicConfig()
LOG = logging.getLogger()
LOG.setLevel("DEBUG")


def main(*args) -> None:
    raise NotImplementedError()


if __name__ == "__main__":
    sys.exit(main(*sys.argv))
