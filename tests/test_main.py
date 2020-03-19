import sys
from unittest import TestCase

from emeki.main import emeki_main


class TestMain(TestCase):
    def test_main(self):

        sys.argv = [""]
        emeki_main()

    pass
