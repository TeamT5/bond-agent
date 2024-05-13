import os
import logging
from uvicorn import run as uvicorn_run
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from libs.config import config
from libs.config import http_code
from libs.service.utility import exception_handle_text

# *----- handler exec 依賴套件，勿刪 -----*
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

# *----- handler exec 依賴套件，勿刪 -----*


class Service(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._routes = []

    def route(self, path, **kwargs):
        def decorator(func):
            self._routes.append((path, func, kwargs))
            return func

        return decorator

    def register_default_actions(self):
        if config.DEBUG:

            @self.get(config.DOCS_URL, include_in_schema=False)
            def swagger_ui_html():
                return get_swagger_ui_html(
                    openapi_url=self.openapi_url,
                    title=f"{config.SERVERTITLE} | Swagger UI",
                    swagger_favicon_url=config.FAVICON_URL,
                )

            @self.get(config.REDOC_URL, include_in_schema=False)
            def redoc_ui_html():
                return get_redoc_html(
                    openapi_url=self.openapi_url,
                    title=f"{config.SERVERTITLE} | ReDOC UI",
                    redoc_favicon_url=config.FAVICON_URL,
                )

        @self.on_event("startup")
        def startup_event():
            logger = logging.getLogger(config.ACCESS_LOG_NAME)
            localpath = os.getcwd().replace("\\", "/")
            logs_path = localpath + "/" + config.ACCESS_LOG_PATH

            if not os.path.isdir(logs_path):
                os.makedirs(logs_path)

            handler = logging.handlers.RotatingFileHandler(
                filename=rf"{localpath}/{config.ACCESS_LOG_PATH}/{config.ACCESS_LOG_FILE_NAME}",
                mode=config.ACCESS_LOG_MODE,
                encoding=config.ACCESS_LOG_ENCODING,
                maxBytes=config.ACCESS_LOG_SIZE * 1024,
                backupCount=config.ACCESS_LOG_BACKUP_COUNT,
            )

            handler.setFormatter(
                logging.Formatter("%(asctime)s %(name)s [%(levelname)s] | %(message)s")
            )

            logger.addHandler(handler)

    def checker_bond_modules(self):
        if config.OS_NAME == config.System_Name.WINDOWS:
            from libs.actions.windows_bond_service import Windows_Bond_Service

            self.include_router(Windows_Bond_Service.router)

        elif config.OS_NAME == config.System_Name.LINUX:
            from libs.actions.linux_bond_service import Linux_Bond_Service

            self.include_router(Linux_Bond_Service.router)

        elif config.OS_NAME == config.System_Name.MAC:
            from libs.actions.mac_bond_service import Mac_Bond_Service

            self.include_router(Mac_Bond_Service.router)

    def bond_run(self):
        self.mount(
            "/static", StaticFiles(directory=config.STATIC_PATH), config.STATIC_PATH
        )
        self.register_default_actions()

        for path, func, kwargs in self._routes:
            self.add_api_route(path, func, **kwargs)

        self.checker_bond_modules()
        for (
            http_exception_code,
            http_exception_message,
        ) in http_code.HTTP_STATUS_CODE_DICT.items():
            handle_resouse_text = exception_handle_text.exception_handler(
                http_exception_code, http_exception_message
            )
            exec(handle_resouse_text)

    def uvicorn_runner(self, host: str = "localhost", port: int = 8086):
        self.bond_run()
        uvicorn_run(self, host=host, port=port)
