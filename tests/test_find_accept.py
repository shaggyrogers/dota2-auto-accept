#!/usr/bin/env python3
"""
  test_scoring.py
  ===============

  Description:           Tests for matcher.scoring
  Author:                Michael De Pasquale
  Creation Date:         2025-02-05
  Modification Date:     2025-07-08

"""

from pathlib import Path
import logging

from PIL import Image
import pytest

from find_accept import findAccept

LOG = logging.getLogger(__file__)


@pytest.mark.parametrize("path", Path("./tests/images").glob("testPositive*"))
def test_positive(path: Path) -> None:
    img = Image.open(path)
    result = findAccept(img)
    assert result
    assert 0 < result[0] < img.size[0]
    assert 0 < result[1] < img.size[1]


@pytest.mark.parametrize("path", Path("./tests/images/").glob("testNegative*"))
def test_negative(path: Path) -> None:
    assert findAccept(Image.open(path)) is None
