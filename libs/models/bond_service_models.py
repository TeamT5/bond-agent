from pydantic import BaseModel


class ExecuteFileModel(BaseModel):
    to_be_executed: str
    timeout: int = 0
    extra_args: tuple = ()


class RubyExecuteFileModel(BaseModel):
    to_be_executed: str
    timeout: int = 0
    extra_args: tuple = ()


class GetFileModel(BaseModel):
    target: str
    file_content: str
