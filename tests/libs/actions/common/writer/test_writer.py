import os
import unittest
from libs.config import config
from libs.actions.common.writer.writer import dir_maker, file_writer, split_file_type


class TestFileUtils(unittest.TestCase):
    def test_dir_maker_subdirectory_path(self) -> None:
        # dir name only has subdirectory path
        dir_name = "path/to/directory"
        expected_result = {
            "status": True,
            "path": f"./{config.DOWNLOAD_DIR_NAME}/{dir_name}/",
        }
        self.assertEqual(dir_maker(dir_name), expected_result)
        self.assertTrue(os.path.exists(f"./{config.DOWNLOAD_DIR_NAME}/{dir_name}"))

    def test_dir_maker_both_path(self) -> None:
        # dir name has Downloads dir & subdirectory path
        dir_name = "Downloads/path/to/directory"
        expected_result = {"status": True, "path": f"./{dir_name}/"}
        self.assertEqual(dir_maker(dir_name), expected_result)
        self.assertTrue(os.path.exists(f"./{dir_name}/"))

    def test_dir_maker_downloads_path(self) -> None:
        # dir name only has Downloads dir
        dir_name = "Downloads"
        expected_result = {"status": True, "path": f"./{dir_name}/"}
        self.assertEqual(dir_maker(dir_name), expected_result)
        self.assertTrue(os.path.exists(f"./{dir_name}/"))

    def test_dir_maker_empty_path(self) -> None:
        # dir name has nothing path
        dir_name = ""
        expected_result = {"status": True, "path": f"./{config.DOWNLOAD_DIR_NAME}/"}
        self.assertEqual(dir_maker(dir_name), expected_result)
        self.assertTrue(os.path.exists(f"./{config.DOWNLOAD_DIR_NAME}/"))

    def test_file_writer(self) -> None:
        file_path = f"./{config.DOWNLOAD_DIR_NAME}/path/to/directory"
        file_name = "test.txt"
        file_content = b"Hello, world!"

        expected_result = {"status": True, "path": file_name}

        result = file_writer(file_path, file_name, file_content)

        self.assertEqual(result, expected_result)
        self.assertTrue(
            os.path.exists(f"./{config.DOWNLOAD_DIR_NAME}/path/to/directory/test.txt")
        )
        with open(
            f"./{config.DOWNLOAD_DIR_NAME}/path/to/directory/test.txt", "rb"
        ) as f:
            self.assertEqual(f.read(), file_content)

    def test_file_writer_error(self) -> None:
        file_path = "non_existent_dir"
        file_name = "test.txt"
        file_content = b"Hello, world!"

        expected_result = {
            "status": False,
            "path": file_name,
            "error": FileNotFoundError,
        }

        result = file_writer(file_path, file_name, file_content)

        self.assertEqual(result["status"], expected_result["status"])
        self.assertEqual(result["path"], expected_result["path"])
        self.assertIsInstance(result["error"], expected_result["error"])

    def test_split_file_type_one_extension(self) -> None:
        filename = "test.txt"
        expected_result = ".txt"
        self.assertEqual(split_file_type(filename), expected_result)
        filename = "image.jpg"
        expected_result = ".jpg"
        self.assertEqual(split_file_type(filename), expected_result)

    def test_split_file_type_tar_and_gzip_extension(self) -> None:
        filename = "archive.tar.gz"
        expected_result = ".tar.gz"
        self.assertEqual(split_file_type(filename), expected_result)

    def test_split_file_type_tar_and_bzip2_extension(self) -> None:
        filename = "archive.tar.bz2"
        expected_result = ".tar.bz2"
        self.assertEqual(split_file_type(filename), expected_result)

    def test_split_file_type_tar_extension(self) -> None:
        filename = "archive.tar"
        expected_result = ".tar"
        self.assertEqual(split_file_type(filename), expected_result)

    def test_split_file_type_gzip_extension(self) -> None:
        filename = "archive.gz"
        expected_result = ".gz"
        self.assertEqual(split_file_type(filename), expected_result)

    def test_split_file_type_no_extension(self) -> None:
        filename = "script"
        expected_result = ".others"
        self.assertEqual(split_file_type(filename), expected_result)
