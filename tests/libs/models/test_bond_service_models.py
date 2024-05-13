import unittest
from pydantic import ValidationError
from libs.models.bond_service_models import (
    DownloadScannerZipModel,
    ExecuteFileModel,
    GetFileModel,
)


class TestModels(unittest.TestCase):
    def test_download_scanner_zip_model(self) -> None:
        valid_data = {"url": "https://example.com/scanner.zip"}
        model = DownloadScannerZipModel(**valid_data)
        self.assertEqual(model.url, valid_data["url"])

        invalid_data = {"url": 123}
        model = DownloadScannerZipModel(**invalid_data)
        self.assertNotEqual(type(model.url), type(invalid_data["url"]))

    def test_execute_file_model(self) -> None:
        valid_data = {"to_be_executed": "script.sh", "timeout": 10}
        model = ExecuteFileModel(**valid_data)
        self.assertEqual(model.to_be_executed, valid_data["to_be_executed"])
        self.assertEqual(model.timeout, valid_data["timeout"])

        missing_data = {}
        with self.assertRaises(ValidationError):
            ExecuteFileModel(**missing_data)

        invalid_data = {"to_be_executed": "script.sh", "timeout": "invalid"}
        with self.assertRaises(ValidationError):
            ExecuteFileModel(**invalid_data)

    def test_get_file_model(self) -> None:
        valid_data = {
            "target": "file.txt",
            "file_content": "Lorem ipsum dolor sit amet",
        }
        model = GetFileModel(**valid_data)
        self.assertEqual(model.target, valid_data["target"])
        self.assertEqual(model.file_content, valid_data["file_content"])

        invalid_data = {"target": 123, "file_content": 123}
        model = GetFileModel(**invalid_data)
        self.assertNotEqual(type(model.target), type(invalid_data["target"]))
        self.assertNotEqual(
            type(model.file_content), type(invalid_data["file_content"])
        )

        missing_data = {"target": "file.txt"}
        with self.assertRaises(ValidationError):
            GetFileModel(**missing_data)
