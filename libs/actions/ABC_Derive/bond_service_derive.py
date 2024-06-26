import os
import base64
import tempfile
import platform
import subprocess
from fastapi import Request, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse

from loguru import logger
from libs.config import config
from libs.actions.common.Zip.zip import ZIP
from libs.actions.common.Windows import execute_file_utility
from libs.actions.common.File_read.file_reader import FileReader
from libs.actions.ABC_Base.bond_service_abc import Bond_Service_ABC
from libs.models.bond_service_models import (
    UploadFileModel,
    UploadFolderModel,
    ExecutePythonModel,
)


class Bond_Service_Derive(Bond_Service_ABC):
    @Bond_Service_ABC.router.get("/", name="Index", include_in_schema=False)
    def bond_index(request: Request) -> None:
        return config.TEMPLATES.TemplateResponse(
            "index.html",
            {
                "request": request,
                "debug": config.DEBUG,
                "version": config.VERSION,
                "DOCS_URL": config.DOCS_URL,
                "REDOC_URL": config.REDOC_URL,
            },
        )

    @Bond_Service_ABC.router.get("/bond_info", name="Bond_Info")
    def bond_info(request: Request) -> JSONResponse:
        info = dict(os.environ)
        info["platform"] = platform.platform()
        info["python_version"] = platform.python_version()
        for key, value in info.items():
            if isinstance(value, str):
                info[key] = value.strip().replace("\\", "/")
        info["bond_version"] = config.VERSION

        return JSONResponse(
            content=jsonable_encoder(info),
            status_code=200 if info else 400,
            media_type="application/json",
        )

    @Bond_Service_ABC.router.post("/upload_folder", name="Upload_Folder")
    def upload_folder(upload: UploadFolderModel) -> JSONResponse:
        try:
            target = upload.target.replace("\\", "/")
            folder_name = target.split("/")[-1]
            folder_content = upload.folder_content
            folder_data = base64.b64decode(folder_content.encode("utf-8"))

            with tempfile.TemporaryDirectory() as temp_dir:
                temp_zip = f"{temp_dir}/{folder_name}.zip"

                with open(temp_zip, "wb") as out_file:
                    out_file.write(folder_data)

                ZIP.unzip_file(temp_zip, target)

            resp_dict = {
                "status": True,
                "folder_path": target,
                "folder_name": folder_name,
                "info": {},
            }

            resp_dict["info"]["message"] = "Folder Uploaded Successfully"

        except BaseException as err:
            resp_dict["status"] = False
            resp_dict["info"]["message"] = "BaseException: Folder Uploaded Failed"
            resp_dict["info"]["error"] = str(err)

        finally:
            return JSONResponse(
                content=jsonable_encoder(resp_dict),
                status_code=200 if resp_dict["status"] else 400,
                media_type="application/json",
            )

    @Bond_Service_ABC.router.post("/upload_file", name="Upload_File")
    def upload_file(upload: UploadFileModel) -> JSONResponse:
        try:
            target = upload.target.replace("\\", "/")
            file_content = upload.file_content
            file_data = base64.b64decode(file_content.encode("utf-8"))

            resp_dict = {
                "status": True,
                "file_path": target,
                "file_name": target.split("/")[-1],
                "info": {},
            }
            with open(target, "wb") as out_file:
                out_file.write(file_data)
            resp_dict["info"]["message"] = "File Uploaded Successfully"

        except BaseException as err:
            resp_dict["status"] = False
            resp_dict["info"]["message"] = "BaseException: File Uploaded Failed"
            resp_dict["info"]["error"] = str(err)

        finally:
            return JSONResponse(
                content=jsonable_encoder(resp_dict),
                status_code=200 if resp_dict["status"] else 400,
                media_type="application/json",
            )

    @Bond_Service_ABC.router.get("/get_physical_file", name="Get_Physical_File")
    def get_physical_file(target: str) -> JSONResponse:
        result = FileReader.file_to_base64(target)

        return JSONResponse(
            content=result, status_code=200, media_type="application/json"
        )

    @Bond_Service_ABC.router.get(
        "/get_physical_folder_zip", name="get_physical_folder_zip"
    )
    def get_physical_folder_zip(
        target: str, background_tasks: BackgroundTasks
    ) -> StreamingResponse:
        zip_filename = ZIP.zip_folder(target)
        file_iterator = FileReader.file_iterator(zip_filename)

        background_tasks.add_task(lambda: os.remove(zip_filename))

        return StreamingResponse(
            file_iterator,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={zip_filename}"},
        )

    @Bond_Service_ABC.router.post(
        "/execute_python_folder", name="Execute_Python_Folder"
    )
    def execute_python_folder(execute: ExecutePythonModel) -> JSONResponse:
        """
        [API] Execute the python folder with the given executor and return the output.

        :param execute: [ExecuteFileModel] execute file model
        :return: JSONResponse
        """

        resp_data = {}
        resp_status_code = 200
        timeout = execute.timeout
        extra_args = execute.extra_args
        to_be_executed = execute.to_be_executed

        try:
            out, err, returncode = execute_file_utility.execute_python_command(
                to_be_executed=to_be_executed, timeout=timeout, extra_args=extra_args
            )
            resp_data["message"] = "Success" if returncode == 0 else "Failed"
            resp_data["stdout"] = str(out)
            resp_data["stderr"] = str(err)
        except subprocess.TimeoutExpired:
            logger.error("execute_file Timeout")
            resp_data["message"] = "Timeout"
            resp_status_code = 408

        except FileNotFoundError:
            logger.error("execute_file File not found")
            resp_data["message"] = "File not found"
            resp_data["executor"] = "python"
            resp_data["to_be_executed"] = to_be_executed
            resp_status_code = 404

        except BaseException as err:
            logger.error(err)
            resp_data["message"] = "Internal Server Error"
            resp_status_code = 500

        finally:
            return JSONResponse(
                content=jsonable_encoder(resp_data),
                status_code=resp_status_code,
                media_type="application/json",
            )
