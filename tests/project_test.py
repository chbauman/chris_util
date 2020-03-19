import os
import shutil
from pathlib import Path
from unittest import TestCase

from emeki.project_setup import setup_project
from emeki.util import create_dir

TEST_DATA_DIR = os.path.join(Path(__file__).parent, "test_data")


class TestTesting(TestCase):
    def test_project_creation(self):

        target_dir = os.path.join(TEST_DATA_DIR, "project_test_data")
        create_dir(target_dir)

        try:
            setup_project(target_dir, "test-project", "emeki")
        finally:
            shutil.rmtree(target_dir)

    pass
