from abc import ABC, abstractmethod
from datetime import datetime


class DataSourcePlugin(ABC):
    """Base interface for all external data-source plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def connect(self, credentials: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def sync_accounts(self, user_id: int) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    async def sync_transactions(self, user_id: int, since: datetime) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    async def get_balances(self, user_id: int) -> list[dict]:
        raise NotImplementedError
