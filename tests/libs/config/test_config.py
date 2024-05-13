import unittest
import sys
from libs.config import config


class TestSystem(unittest.TestCase):
    def test_os_version(self) -> None:
        os_version = sys.platform
        self.assertIn(os_version, config.SYSTEM_CHART)

    def test_os_name(self) -> None:
        os_version = sys.platform
        os_name = config.SYSTEM_CHART.get(os_version)
        self.assertIsNotNone(os_name)
        self.assertIsInstance(os_name, str)
