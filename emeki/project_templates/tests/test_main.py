"""This files contains the tests for `main.py`."""
from unittest import TestCase

from PROJECT_NAME.main import main


def test_main():
    assert main() == 0


class TestMain(TestCase):
    def test_main(self):
        assert main() == 0
