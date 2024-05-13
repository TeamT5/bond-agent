import os
from pathlib import Path
from libs.config import config


def dir_maker(dir_name: str) -> dict:
    """
    Create directory maker function.

    :param dir_name: [str] directory name
    :return: [dict] directory maker response
    """

    try:
        path_split = dir_name.split("/")
        if len(path_split) == 1 and path_split[0].title() != config.DOWNLOAD_DIR_NAME:
            path_split[0] = config.DOWNLOAD_DIR_NAME
        elif path_split[0] == "" and path_split[1].title() != config.DOWNLOAD_DIR_NAME:
            path_split[0] = config.DOWNLOAD_DIR_NAME
        elif (
            path_split[0].title() != config.DOWNLOAD_DIR_NAME
            and path_split[1].title() != config.DOWNLOAD_DIR_NAME
        ):
            path_split.insert(0, config.DOWNLOAD_DIR_NAME)

        pathname = "./"
        for path in path_split:
            pathname += path + "/"
            str_to_path = Path(pathname)
            if not os.path.exists(str_to_path):
                os.makedirs(str_to_path)

        return {"status": True, "path": pathname}
    except Exception as err:
        return {"status": False, "path": dir_name, "error": err}


def file_writer(file_path: str, file_name: str, file_content: str) -> dict:
    """
    File writer function.

    :param file_path: [str] file path
    :param file_name: [str] file name
    :param file_content: [str] file content
    :return: [dict] file writer response
    """

    try:
        dir_maker_resp = dir_maker(file_path)
        if not dir_maker_resp["status"]:
            raise {
                "status": False,
                "path": file_path,
                "file": file_name,
                "error": dir_maker_resp["error"],
            }
        with open(f"{file_path}/{file_name}", "wb") as f:
            f.write(file_content)
        return {"status": True, "path": file_name}
    except Exception as err:
        return {"status": False, "path": file_name, "error": err}


def split_file_type(filename: str) -> str:
    """
    Check the file type and return the extension.

    :param filename: [str] file name
    :return: [str] file extension
    """

    basename, extension = os.path.splitext(filename)
    if extension == "":
        extension = ".others"
    elif extension == ".gz" or extension == ".bz2":
        split_basename = basename.split(".")
        if split_basename[-1] == "tar":
            extension = f".tar{extension}"
    return extension.replace('"', "").replace("'", "")
