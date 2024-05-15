from fastapi import APIRouter
from abc import ABC, abstractmethod


class Bond_Service_ABC(ABC):
    router = APIRouter(
        tags=["Bond_service"],
    )

    @classmethod
    @abstractmethod
    def bond_heartbeat(cls): ...

    @classmethod
    @abstractmethod
    def bond_info(cls): ...

    @classmethod
    @abstractmethod
    def execute_file(cls): ...

    @classmethod
    @abstractmethod
    def download_scanner_zip(cls): ...

    @classmethod
    @abstractmethod
    def get_file(cls): ...

    @classmethod
    @abstractmethod
    def get_physical_file(cls): ...
