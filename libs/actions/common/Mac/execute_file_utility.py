import signal
import subprocess
from loguru import logger


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

    logger.debug(process)
    timeout_sec = timeout_sec if timeout_sec != 0 else None

    try:
        stdout, stderr = process.communicate(timeout=timeout_sec)
    except subprocess.TimeoutExpired:
        process.send_signal(signal.SIGKILL)

        stdout, stderr = process.communicate()

        raise subprocess.TimeoutExpired(command, timeout=timeout_sec)

    return [stdout, stderr, process.returncode]


def execute_command(
    executor: str, to_be_executed: str, timeout: int, extra_args: tuple = ()
) -> tuple:
    """
    Execute the command with the given executor and return the output.

    :param executor: [str] executor
    :param to_be_executed: [str] to be executed
    :param timeout: [int] timeout
    :param extra_args: [tuple] extra arguments
    :return: [tuple] out, err, returncode
    """

    out, err, returncode = "", "", 1
    if extra_args:
        to_be_executed = f"{to_be_executed} {' '.join(extra_args)}"
    run_command = f"{executor} {to_be_executed}"

    out, err, returncode = run_command_with_timeout(run_command, timeout)

    return out, err, returncode
