from typing import Any
from abc import abstractmethod, ABC

from exceptions.base_exceptions import Varint32Exception


class BaseConnector(ABC):
    @abstractmethod
    async def open_connection(self):
        pass

    @abstractmethod
    async def close_connection(self):
        pass

    @abstractmethod
    async def is_closing(self):
        pass

    @abstractmethod
    async def write(self, data: Any):
        pass

    @abstractmethod
    async def write_and_drain(self, data: Any):
        pass

    @abstractmethod
    async def read(self, n: int):
        pass

    @abstractmethod
    async def read_exactly(self, n: int):
        pass

    @abstractmethod
    async def read_until(self, separator: str):
        pass

    async def read_varint_32(self) -> int:
        """Read varint from serial port"""
        MASK = (1 << 32) - 1

        result = 0
        shift = 0
        while 1:
            b = int.from_bytes(await self.read_exactly(n=1), byteorder="little", signed=False)
            result |= (b & 0x7F) << shift

            if not b & 0x80:
                result &= MASK
                result = int(result)
                return result
            shift += 7
            if shift >= 64:
                raise Varint32Exception("Too many bytes when decoding varint.")
