import os
import shutil
from pathlib import Path

import pytest
from unittest import TestCase

from emeki.project_setup import DATA_DIR
from emeki.testing import AssertPrints
from emeki.util import str2bool, emeki_main, create_dir, zip_dir, unzip_to
from tests.project_test import TEST_DATA_DIR


@pytest.mark.parametrize("str_in, output", [("t", True), ("0", False), (True, True)])
def test_str_to_bool(str_in, output):
    assert str2bool(str_in) == output, "failed"


class TestUtil(TestCase):
    def test_str_to_bool(self):
        test_in = "true"
        self.assertTrue(str2bool(test_in), f"Test with input: {test_in} failed!")

    def test_str_to_bool_ex(self):
        with self.assertRaises(ValueError):
            str2bool(2)

    def test_emeki(self):
        emeki_main()

    def test_create_dir(self):
        dir_name = "Test_dir"
        try:
            create_dir(dir_name)
            assert os.path.isdir(dir_name)
        finally:
            os.removedirs(dir_name)

    def test_zipping(self):
        try:
            out_name = os.path.join(TEST_DATA_DIR, "test")
            zip_dir(DATA_DIR, out_name)
            unzip_dir = os.path.join(TEST_DATA_DIR, "test2")
            unzip_to(out_name + ".zip", unzip_dir)
        finally:
            shutil.rmtree(TEST_DATA_DIR)


class TestTesting(TestCase):
    def test_test_print(self):
        with AssertPrints("Hi"):
            print("Hi")

    pass
