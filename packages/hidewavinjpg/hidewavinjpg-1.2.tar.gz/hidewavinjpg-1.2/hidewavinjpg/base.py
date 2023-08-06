from abc import ABC, abstractmethod
from typing import Any


class BaseCodec(ABC):
    @abstractmethod
    def encode(self, carrier: Any, payload: Any) -> Any:
        ...

    @abstractmethod
    def decode(self, carrier: Any) -> Any:
        ...
