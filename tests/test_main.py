# Test main could be invoked in command line:
# python main.py
# Close the app with Ctrl+C

from unittest import TestCase
from main import main
import subprocess
import time
import signal

from libs.config import config


class TestMain(TestCase):
    def test_main(self) -> None:
        self.assertTrue(callable(main))

    def test_main_run(self) -> None:
        # run main in a subprocess and wait for 3 seconds, terminate it via
        # SIGINT
        p = subprocess.Popen(["python", "main.py"])
        time.sleep(3)
        # If os is Windows, use SIGBREAK instead of SIGINT
        if config.OS_NAME == config.System_Name.WINDOWS:
            p.send_signal(signal.CTRL_C_EVENT)
        else:
            p.send_signal(signal.SIGINT)

        status = p.wait()
        self.assertTrue(status is not None)
