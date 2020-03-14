import pytest
from unittest import TestCase

from emeki.util import str2bool


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
            
    def test_fail(self):
        assert False, "Expected failure"

    pass
