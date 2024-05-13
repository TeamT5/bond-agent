import inspect
import unittest
from abc import ABC, abstractmethod
from libs.actions.ABC_Base.bond_service_abc import Bond_Service_ABC


class TestBondServiceABC(unittest.TestCase):
    def test_router_exists(self) -> None:
        self.assertTrue(hasattr(Bond_Service_ABC, "router"))
        self.assertIsNotNone(Bond_Service_ABC.router)

    def test_bond_heartbeat_is_abstract(self) -> None:
        self.assertTrue(issubclass(Bond_Service_ABC, ABC))
        self.assertTrue(
            getattr(Bond_Service_ABC.bond_heartbeat, "__isabstractmethod__", False)
        )

    def test_bond_info_is_abstract(self) -> None:
        self.assertTrue(issubclass(Bond_Service_ABC, ABC))
        self.assertTrue(
            getattr(Bond_Service_ABC.bond_info, "__isabstractmethod__", False)
        )

    def test_execute_file_is_abstract(self) -> None:
        self.assertTrue(issubclass(Bond_Service_ABC, ABC))
        self.assertTrue(
            getattr(Bond_Service_ABC.execute_file, "__isabstractmethod__", False)
        )

    def test_download_scanner_zip_is_abstract(self) -> None:
        self.assertTrue(issubclass(Bond_Service_ABC, ABC))
        self.assertTrue(
            getattr(
                Bond_Service_ABC.download_scanner_zip, "__isabstractmethod__", False
            )
        )

    def test_get_file_is_abstract(self) -> None:
        self.assertTrue(issubclass(Bond_Service_ABC, ABC))
        self.assertTrue(
            getattr(Bond_Service_ABC.get_file, "__isabstractmethod__", False)
        )
