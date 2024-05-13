import os
import base64


class FileReader:
    @staticmethod
    def file_iterator(file_name: str, chunk_size=8192) -> bytes:
        """
        File iterator function.

        :param file_name: [str] file name
        :param chunk_size: [int] chunk size
        :return: [bytes] file content
        """

        with open(file_name, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    def file_to_base64(file_path: str) -> dict:
        """
        Read a file and return a dictionary with filename and its base64 content.

        :param file_path: [str] file path
        :return: [dict] file base64 content
        """

        with open(file_path, "rb") as file:
            file_content = file.read()
            encoded_content = base64.b64encode(file_content).decode("utf-8")

        filename = os.path.basename(file_path)
        return {"filename": filename, "file_base64": encoded_content}
