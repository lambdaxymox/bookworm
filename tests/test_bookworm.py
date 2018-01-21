import sys
import pytest

from bookworm import main


def test_bookworm_main():
    assert main is not None