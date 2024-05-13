import time
import unittest
import multiprocessing
from libs.config import config
from main import bond_program
from libs.actions.common.Console_Executor.console_executor import parse_executor


class TestParseExecutor(unittest.TestCase):
    def setUp(self) -> None:
        self.process = multiprocessing.Process(name="Bond-Agent", target=bond_program)
        self.process.start()
        time.sleep(3)  # 3 seconds for uvicorn to start

    def test_parse_executor(self) -> None:
        self.assertTrue(parse_executor("test.py").find("python") != -1)
        if config.OS_NAME == config.System_Name.WINDOWS:
            self.assertTrue(parse_executor("test.exe").find("cmd.exe") != -1)
            self.assertTrue(parse_executor("test.bat").find("cmd.exe") != -1)
            self.assertTrue(parse_executor("test.ps1").find("powershell.exe") != -1)
        elif (
            config.OS_NAME == config.System_Name.LINUX
            or config.OS_NAME == config.System_Name.MAC
        ):
            self.assertTrue(parse_executor("test.sh").find("sh") != -1)
        self.assertTrue(parse_executor("test").find("test") != -1)
        self.process.terminate()
        self.process.join()
