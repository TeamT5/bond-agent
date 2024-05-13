import os
import base64
import platform
from fastapi import Request, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse
from libs.actions.ABC_Base.bond_service_abc import Bond_Service_ABC

from libs.config import config
from libs.actions.common.Zip.zip import ZIP
from libs.actions.common.File_read.file_reader import FileReader

from libs.models.bond_service_models import (
    GetFileModel,
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

    @Bond_Service_ABC.router.post("/upload_file", name="Upload_File")
    def upload_file(file_model: GetFileModel) -> JSONResponse:
        try:
            file_target_path = file_model.target.replace("\\", "/")
            file_content = file_model.file_content
            file_data = base64.b64decode(file_content.encode("utf-8"))

            resp_dict = {
                "status": True,
                "file_path": file_target_path,
                "file_name": file_target_path.split("/")[-1],
                "info": {},
            }
            with open(file_target_path, "wb") as out_file:
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
