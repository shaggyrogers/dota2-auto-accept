#!/usr/bin/env python3
"""
  find_accept.py
  ==============

  Description:           Logic for detecting and locating the accept and ready buttons.
  Author:                Michael De Pasquale
  Creation Date:         2025-07-08
  Modification Date:     2025-07-09

"""

import logging
import math
from typing import Union

from PIL import Image, ImageChops, ImageFilter
import pytesseract


LOG = logging.getLogger(__file__)
# LOG.setLevel("DEBUG")

# Crop regions for 1920x1080 with and without Dota Plus
REGION_DOTA_PLUS = (577 / 1920, 235 / 1080, 1343 / 1920, 746 / 1080)
REGION_NORMAL = (577 / 1920, 363 / 1080, 1344 / 1920, 618 / 1080)


def findAcceptOrReady(img: Image) -> Union[tuple[str, float, float], None]:
    """Find an accept/ready button in img. Returns a tuple with the button text and center coordinates
    if found, None otherwise.
    """
    if not (result := _findAcceptRegion(img, REGION_DOTA_PLUS)):
        result = _findAcceptRegion(img, REGION_NORMAL)

    return result


def _findAcceptRegion(img: Image, region: tuple) -> Union[tuple[str, float, float], None]:
    """Look for an accept/ready button in the given region, given as 4-tuple with each element
    between 0 and 1.
    Returns the text and coordinates of the center of the button if found, None if otherwise.
    """
    img = img.convert("RGB")
    originalImg = img.copy()
    width, height = img.size

    # Scale region to image size, crop image
    region = (
        region[0] * width,
        region[1] * height,
        region[2] * width,
        region[3] * height,
    )
    img = img.crop(region)

    def _makeGreenColorFilter(
        r: float, g: float, b: float
    ) -> tuple[float, float, float]:
        if r > 80 / 255 or g < 50 / 255 or b > 94 / 255:
            return (0, 0, 0)

        if g < r * 1.1 or g < b * 1.1 or b < r:
            return (0, 0, 0)

        return r, g, b

    greenFilter = ImageFilter.Color3DLUT.generate(24, _makeGreenColorFilter)

    # Apply filters that only accept button should survive
    img = img.filter(greenFilter)
    img = img.filter(ImageFilter.MinFilter(5))
    img = img.filter(greenFilter)

    # Get bounding box, check image is not empty and proportions are OK
    bbox = img.getbbox()

    if bbox is None:
        LOG.debug(f"Candidate has empty bounding box")

        return None

    ratio = (bbox[2] - bbox[0]) / (bbox[3] - bbox[1])

    if not math.isclose(ratio, 322 / 64, rel_tol=0.15):
        LOG.debug(f"Candidate has bad ratio (got {ratio:.3f}, expected {322/64:.3f})")

        return None

    # Check unfiltered accept button is valid
    btnText = _getButtonText(
        originalImg.crop(
            (
                region[0] + bbox[0],
                region[1] + bbox[1],
                region[0] + bbox[2],
                region[1] + bbox[3],
            )
        )
    )


    if btnText not in ("accept", "ready"):
        LOG.debug(f"Unrecognised button text: '{btnText}'")

        return None

    return (
        btnText,
        region[0] + bbox[0] + (bbox[2] - bbox[0]) / 2,
        region[1] + bbox[1] + (bbox[3] - bbox[1]) / 2,
    )


def _getButtonText(candidate: Image) -> str:
    """ Run OCR on the image, returning lowercase text. """

    def _makeWhiteColorFilter(
        r: float, g: float, b: float
    ) -> tuple[float, float, float]:
        if r < 230 / 255 or g < 230 / 255 or b < 230 / 255:
            return (0, 0, 0)

        return (1, 1, 1)

    # Remove anything that can't be the "Accept" text
    whiteFilter = ImageFilter.Color3DLUT.generate(24, _makeWhiteColorFilter)

    # Run OCR
    text = pytesseract.image_to_string(candidate.filter(whiteFilter))

    return text.strip().lower()
