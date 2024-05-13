from libs.config import config


def exception_handler(handle_type_code: int, handle_code_message: str) -> str:
    """
    if the http status code is not 200, then return the html string

    :param handle_type_code: [int] http status code
    :param handle_code_message: [str] http status code message
    :return: [str] html string
    """

    http_code_description = (
        handle_code_message["message"].replace("\n", "").replace(" ", "")
    )

    result = (
        f"""
@self.exception_handler({handle_type_code})
def exception_{handle_type_code}_handler(request: Request, exc: HTTPException):
    return config.TEMPLATES.TemplateResponse(
        'exception_error.html', """
        + "{"
        + f"""
        'request': request,
        'version': '{config.VERSION}',
        "http_code": '{handle_type_code}',
        "http_code_content": '{handle_code_message["code_name"]}',
        "http_code_description": '{http_code_description}'
    """
        + "})"
    )

    return result
