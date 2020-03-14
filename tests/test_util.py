from unittest import TestCase

from emeki.util import str2bool


class TestUtil(TestCase):

    def test_str_to_bool(self):

        test_in = "true"
        self.assertTrue(str2bool(test_in), f"Test with input: {test_in} failed!")

    pass
