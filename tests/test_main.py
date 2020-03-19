import shutil
import sys
from unittest import TestCase, mock

from emeki import main
from emeki.main import emeki_main
from emeki.testing import InputMock
from emeki.util import empty_dir, create_dir
from tests.project_test import TEST_DATA_DIR


class TestMain(TestCase):
    def test_main_abort(self):
        sys.argv = [""]
        emeki_main()

    def test_main(self):
        sys.argv = ["", "--init_pro"]
        create_dir(TEST_DATA_DIR)
        empty_dir(TEST_DATA_DIR)
        with InputMock(["Ich", "my-awesome-project", TEST_DATA_DIR]):
            emeki_main()
        shutil.rmtree(TEST_DATA_DIR)

    def test_module_call(self):
        with mock.patch.object(main, "emeki_main", return_value=42):
            with mock.patch.object(main, "__name__", "__main__"):
                with mock.patch.object(main.sys, "exit") as mock_exit:
                    main.execute()
                    assert mock_exit.call_args[0][0] == 42

    pass
