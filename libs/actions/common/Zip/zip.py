import os
import zipfile


class ZIP:
    @staticmethod
    def _zipdir(folder_path: str, ziph: zipfile.ZipFile) -> None:
        """
        Create zipdir function.

        :param folder_path: [str] folder path
        :param ziph: [zipfile.ZipFile] zipfile object
        """

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                ziph.write(
                    os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file), folder_path),
                )

    @classmethod
    def zip_folder(cls, folder_path: str) -> str:
        """
        Create zip_folder function.

        :param folder_path: [str] folder path
        :return: [str] archive name
        """

        base_name = os.path.basename(folder_path)
        archive_name = f"{base_name}.zip"
        with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            cls._zipdir(folder_path, zipf)
        return archive_name

    @staticmethod
    def unzip_file(zip_path: str, extract_to: str) -> None:
        """
        Unzip the file.

        :param zip_path: [str] zip path
        :param extract_to: [str] extract to path
        """
        os.makedirs(extract_to, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zipf:
            zipf.extractall(extract_to)
