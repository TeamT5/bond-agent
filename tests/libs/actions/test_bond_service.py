import os
import time
import unittest
import requests
import multiprocessing
from libs.config import config
from main import bond_program


class TestBondService(unittest.TestCase):
    def setUp(self) -> None:
        self.process = multiprocessing.Process(name="Bond-Agent", target=bond_program)
        self.process.start()
        time.sleep(3)  # 3 seconds for uvicorn to start

    def test_execute_file(self) -> None:
        with open("./test.py", "w") as f:
            f.write('print("Hello world!")')

        payload = {"to_be_executed": "./test.py", "timeout": 10}
        response = requests.post(
            f"http://localhost:{config.UVICORN_PORT}/execute_file", json=payload
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find(b"Hello world!") != -1)
        os.remove("test.py")
        self.process.terminate()
        self.process.join()

    def test_execute_file_timeout(self) -> None:
        with open("test.py", "w") as f:
            f.write("""import time\ntime.sleep(3)""")

        payload = {"to_be_executed": "./test.py", "timeout": 1}
        response = requests.post(
            f"http://localhost:{config.UVICORN_PORT}/execute_file", json=payload
        )

        self.assertEqual(response.status_code, 408)
        self.assertTrue(response.content.find(b"Timeout") != -1)
        os.remove("test.py")
        self.process.terminate()
        self.process.join()

    def test_execute_file_not_found(self) -> None:
        payload = {"to_be_executed": "./test.py", "timeout": 1}
        response = requests.post(
            f"http://localhost:{config.UVICORN_PORT}/execute_file", json=payload
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find(b"No such file or directory") != -1)
        self.process.terminate()
        self.process.join()

    def test_infinite_wait(self) -> None:
        with open("test.py", "w") as f:
            f.write("""import time\ntime.sleep(3)""")

        payload = {"to_be_executed": "./test.py", "timeout": 0}
        response = requests.post(
            f"http://localhost:{config.UVICORN_PORT}/execute_file", json=payload
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find(b"Timeout") == -1)
        os.remove("test.py")
        self.process.terminate()
        self.process.join()

    def test_execute_file_with_extra_args(self) -> None:
        with open("test.py", "w") as f:
            f.write("""import sys\nprint(sys.argv[1])""")

        payload = {
            "to_be_executed": "./test.py",
            "timeout": 10,
            "extra_args": ('''"Hello world!"''',),
        }
        response = requests.post(
            f"http://localhost:{config.UVICORN_PORT}/execute_file", json=payload
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find(b"Hello world!") != -1)
        os.remove("test.py")
        self.process.terminate()
        self.process.join()

    def test_execute_file_with_extra_args_timeout(self) -> None:
        with open("test.py", "w") as f:
            f.write("""import sys\nimport time\ntime.sleep(3)\nprint(sys.argv[1])""")

        payload = {
            "to_be_executed": "./test.py",
            "timeout": 1,
            "extra_args": ('''"Hello world!"''',),
        }
        response = requests.post(
            f"http://localhost:{config.UVICORN_PORT}/execute_file", json=payload
        )

        self.assertEqual(response.status_code, 408)
        self.assertTrue(response.content.find(b"Timeout") != -1)
        os.remove("test.py")
        self.process.terminate()
        self.process.join()

    def test_execute_file_with_extra_args_2(self) -> None:
        with open("test.py", "w") as f:
            f.write("""import sys\nprint(sys.argv[1], sys.argv[2])""")

        payload = {
            "to_be_executed": "./test.py",
            "timeout": 10,
            "extra_args": ('''"Hello world!"''', '''"Hello world!"'''),
        }
        response = requests.post(
            f"http://localhost:{config.UVICORN_PORT}/execute_file", json=payload
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find(b"Hello world! Hello world!") != -1)
        os.remove("test.py")
        self.process.terminate()
        self.process.join()
