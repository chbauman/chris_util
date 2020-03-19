import os
import shutil
from pathlib import Path
from unittest import TestCase, mock

from emeki.project_setup import (
    setup_project,
    setup_project_zipped,
    zip_template,
    setup_project_UI,
)
from emeki.testing import InputMock
from emeki.util import create_dir

TEST_DATA_DIR = os.path.join(Path(__file__).parent, "test_data")


class TestProject(TestCase):
    def test_project_creation(self):

        target_dir = os.path.join(TEST_DATA_DIR, "project_test_data")
        create_dir(target_dir)

        try:
            setup_project(target_dir, "test-project", "emeki")
        finally:
            shutil.rmtree(target_dir)

    def test_project_creation_zip(self):
        target_dir = os.path.join(TEST_DATA_DIR, "project_test_data_zip")
        create_dir(target_dir)

        try:
            zip_template()
            setup_project_zipped(target_dir, "test-project", "emeki")
        finally:
            shutil.rmtree(target_dir)

    def test_user_project(self):
        target_dir = os.path.join(TEST_DATA_DIR, "project_test_data")
        create_dir(target_dir)

        with mock.patch("builtins.input", return_value="invalid_path"):
            assert not setup_project_UI()

        with InputMock(["   ", "  ", target_dir]):
            assert not setup_project_UI()

    def test_user_project_success(self):
        target_dir = os.path.join(TEST_DATA_DIR, "project_test_data")
        create_dir(target_dir)
        with open(os.path.join(target_dir, "hoi.txt"), "w") as f:
            f.write("hoi")
        with InputMock(["   ", "project-name", target_dir, "blah"]):
            assert not setup_project_UI()
        with InputMock(["   ", "project-name", target_dir, "n"]):
            assert not setup_project_UI()
        with InputMock(["   ", "project-name", target_dir, "y"]):
            assert setup_project_UI()

    pass
