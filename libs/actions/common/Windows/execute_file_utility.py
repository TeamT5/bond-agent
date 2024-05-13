import subprocess


def execute_command(
    executor: str, to_be_executed: str, timeout: int, extra_args: tuple = ()
) -> tuple:
    """
    The cmd.exe needs "/c" flag to execute the command.
    The cmd.exe must be contained in the executor's postfix.
    We define a specific flag for cmd.exe or future use.

    :param executor: [str] executor
    :param to_be_executed: [str] to be executed
    :param timeout: [int] timeout
    :param extra_args: [tuple] extra arguments
    :return: [tuple] out, err, returncode
    """

    out, err, returncode = "", "", 1
    if extra_args:
        to_be_executed = f"{to_be_executed} {' '.join(extra_args)}"

    special_flag = ""
    if executor.endswith("cmd.exe"):
        special_flag = "/c"

    run_command = f"{executor} {special_flag} {to_be_executed}"
    out, err, returncode = run_command_with_timeout(run_command, timeout)

    return out, err, returncode


def run_command_with_timeout(command: str, timeout_sec: int) -> list:
    """
    Run the command with timeout.

    :param command: [str] command
    :param timeout_sec: [int] timeout in seconds
    :return: [list] stdout, stderr, returncode
    """

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )

    timeout_sec = timeout_sec if timeout_sec != 0 else None
    try:
        stdout, stderr = process.communicate(timeout=timeout_sec)

    except subprocess.TimeoutExpired:
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(process.pid)], check=True)

        stdout, stderr = process.communicate()

        raise subprocess.TimeoutExpired(command, timeout=timeout_sec)

    return [stdout, stderr, process.returncode]
