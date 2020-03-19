import os
from unittest import TestCase

import pytest

from emeki.project_setup import DATA_DIR
from emeki.testing import AssertPrints
from emeki.util import str2bool, create_dir, zip_dir, unzip_to, empty_dir
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

    def test_create_dir(self):
        dir_name = "Test_dir"
        try:
            create_dir(dir_name)
            assert os.path.isdir(dir_name)
        finally:
            os.removedirs(dir_name)

    def test_zipping(self):
        try:
            out_name = os.path.join(TEST_DATA_DIR, "test.zip")
            zip_dir(DATA_DIR, out_name)
            unzip_dir = os.path.join(TEST_DATA_DIR, "test2")
            unzip_to(out_name, unzip_dir)
        finally:
            empty_dir(TEST_DATA_DIR)


class TestTesting(TestCase):
    def test_test_print(self):
        with AssertPrints("Hi"):
            print("Hi")

    pass
