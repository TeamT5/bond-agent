import subprocess
from loguru import logger
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from libs.actions.common.Linux import execute_file_utility
from libs.models.bond_service_models import ExecuteFileModel
from libs.actions.common.Console_Executor import console_executor
from libs.actions.ABC_Derive.bond_service_derive import Bond_Service_Derive


class Linux_Bond_Service(Bond_Service_Derive):
    @Bond_Service_Derive.router.post("/execute_file", name="Execute_File")
    def execute_file(execute: ExecuteFileModel) -> JSONResponse:
        """
        [API] Execute the file with the given executor and return the output.

        :param execute: [ExecuteFileModel] execute file model
        :return: JSONResponse
        """

        to_be_executed = execute.to_be_executed
        resp_data = {}
        resp_status_code = 200
        executor = console_executor.parse_executor(to_be_executed)
        extra_args = execute.extra_args

        try:
            out, err, returncode = execute_file_utility.execute_command(
                executor, to_be_executed, execute.timeout, extra_args
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
            resp_data["executor"] = executor
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
