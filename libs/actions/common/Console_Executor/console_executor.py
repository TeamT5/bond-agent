import os


def parse_executor(executee: str) -> str:
    # Parsing the corresponding executor from the environment
    # If the executor is not found, return the default executor

    # A table that maps the executor to the corresponding file
    executor_table = {
        "py": "python",
        "exe": "cmd",
        "sh": "bash",
        "bat": "cmd",
        "ps1": "powershell",
        "jar": "java",
        "js": "node",
    }

    # Select executor from the table by the file extension
    # If the file extension is not found, return the default executor
    # Default executor is itself
    executor = executor_table.get(executee.split(".")[-1], executee)

    if executor == "python":
        return "python"
    elif executor == executee:
        return executor

    # Windows system uses '\' as the directory delimiter
    dir_delim = "\\" if os.name == "nt" else "/"
    # Windows system uses .exe as the file extension
    extra_file_extension = ".exe" if os.name == "nt" else ""

    path_list = os.environ["PATH"].split(os.pathsep)
    for path in path_list:
        path = os.path.normpath(path)
        entire_path = path + dir_delim + executor + extra_file_extension
        if os.path.exists(entire_path):
            return entire_path

    raise FileNotFoundError(f"Not supported file type: {executee}")
