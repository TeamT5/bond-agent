import time
import unittest
import requests
import multiprocessing
from libs.config import config
from main import bond_program


class TestBondServiceDerive(unittest.TestCase):
    def setUp(self) -> None:
        self.process = multiprocessing.Process(name="Bond-Agent", target=bond_program)
        self.process.start()
        time.sleep(3)  # 3 seconds for uvicorn to start

    def test_bond_heartbeat(self) -> None:
        response = requests.get(f"http://localhost:{config.UVICORN_PORT}/")
        self.assertEqual(response.status_code, 200)
        self.process.terminate()
        self.process.join()

    def test_bond_info(self) -> None:
        response = requests.get(f"http://localhost:{config.UVICORN_PORT}/bond_info")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())
        self.process.terminate()
        self.process.join()

    def test_upload_file(self) -> None:
        payload = {
            "target": "./file.txt",
            "file_content": "ZnJvbSBsaWJzLnNlcnZpY2UgaW1wb3J0IFNlcnZpY2UNCmZyb20gbGlicy5jb25maWcgaW1wb3J0IGNvbmZpZw0KDQoNCmRlZiBib25kX3Byb2dyYW0oKToNCiAgICBhcHAgPSBTZXJ2aWNlKA0KICAgICAgICB0aXRsZT1jb25maWcuU0VSVkVSVElUTEUsDQogICAgICAgIGRlc2NyaXB0aW9uPWNvbmZpZy5ERVNDUklQVElPTiwNCiAgICAgICAgdmVyc2lvbj1jb25maWcuVkVSU0lPTiwNCiAgICAgICAgZG9jc191cmw9Ii9kb2NzIiBpZiBjb25maWcuREVCVUcgZWxzZSBOb25lLA0KICAgICAgICByZWRvY191cmw9Ii9yZWRvYyIgaWYgY29uZmlnLkRFQlVHIGVsc2UgTm9uZQ0KICAgICkNCiAgICBhcHAucnVuKGhvc3Q9Y29uZmlnLlVWSUNPUk5fSE9TVCwgcG9ydD1jb25maWcuVVZJQ09STl9QT1JUKQ0KDQoNCmRlZiBtYWluKCk6DQogICAgaWYgY29uZmlnLk9TX1ZFUlNJT04gPT0gY29uZmlnLlN5c3RlbS5XSU5ET1dTOg0KICAgICAgICBmcm9tIHB5dWFjIGltcG9ydCBtYWluX3JlcXVpcmVzX2FkbWluDQogICAgICAgIGZyb20gbGlicy5zZXJ2aWNlLnN0cmF5IGltcG9ydCBTdHJheQ0KDQogICAgICAgIEBtYWluX3JlcXVpcmVzX2FkbWluDQogICAgICAgIGRlZiBjcmVhdGVfc3RyYXkoKToNCiAgICAgICAgICAgIHN0cmF5ID0gU3RyYXkoYm9uZF9wcm9ncmFtKQ0KICAgICAgICAgICAgc3RyYXkuaGlkZV9jb25zb2xlX3dpbmRvdygpDQogICAgICAgICAgICBzdHJheS5zdHJheSgpDQoNCiAgICAgICAgY3JlYXRlX3N0cmF5KCkNCiAgICBlbHNlOg0KICAgICAgICBib25kX3Byb2dyYW0oKQ0KDQoNCmlmIF9fbmFtZV9fID09ICdfX21haW5fXyc6DQogICAgbWFpbigpDQo=",
        }
        if config.OS_NAME == config.System_Name.WINDOWS:
            payload["target"] = "C:\\file.txt"
        response = requests.post(
            f"http://localhost:{config.UVICORN_PORT}/upload_file", json=payload
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["status"])
        self.process.terminate()
        self.process.join()
