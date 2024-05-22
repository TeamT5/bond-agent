from typing import Callable, Dict
from fastapi import Request, HTTPException
from fastapi.templating import Jinja2Templates

from libs.config import config


def create_exception_handler(
    handle_type_code: int, handle_code_message: Dict[str, str]
) -> Callable:
    """
    Create a custom exception handler for FastAPI.

    :param handle_type_code: [int] The HTTP status code to handle.
    :param handle_code_message: [Dict[str, str]] The message to display.
    :return: [Callable] The exception handler.
    """

    async def exception_handler(
        request: Request, exc: HTTPException
    ) -> Jinja2Templates:
        """
        Exception handler for FastAPI.

        :param request: [Request] The request object.
        :param exc: [HTTPException] The exception object.
        :return: [Jinja2Templates] The template response.
        """

        context = {
            "request": request,
            "version": config.VERSION,
            "http_code": handle_type_code,
            "http_code_content": handle_code_message["code_name"],
            "http_code_description": handle_code_message["message"],
        }

        return config.TEMPLATES.TemplateResponse("exception_error.html", context)

    return exception_handler
