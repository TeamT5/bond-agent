from pydantic import BaseModel


class ExecutePythonModel(BaseModel):
    to_be_executed: str
    timeout: int = 0
    extra_args: tuple = ()


class ExecuteFileModel(BaseModel):
    to_be_executed: str
    timeout: int = 0
    extra_args: tuple = ()


class RubyExecuteFileModel(BaseModel):
    to_be_executed: str
    timeout: int = 0
    extra_args: tuple = ()


class UploadFileModel(BaseModel):
    target: str
    file_content: str


class UploadFolderModel(BaseModel):
    target: str
    folder_content: str
