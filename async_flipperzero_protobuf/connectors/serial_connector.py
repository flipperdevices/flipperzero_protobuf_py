from typing import Any

from connectors.base_connector import BaseConnector
from serial_asyncio import open_serial_connection


class SerialConnector(BaseConnector):
    def __init__(self, url: str, baud_rate: int, **kwargs):
        super().__init__(**kwargs)

        self.url = url
        self.baud_rate = baud_rate

        self._reader = None
        self._writer = None

    async def open_connection(self):
        reader, writer = await open_serial_connection(url=self.url, baudrate=self.baud_rate)
        self._reader = reader
        self._writer = writer

        return self

    async def close_connection(self):
        self._writer.close()
        await self._writer.wait_closed()

    async def __aenter__(self):
        await self.open_connection()
        return self

    async def __aexit__(self, *args):
        await self.close_connection()

    async def is_closing(self):
        return self._writer.is_closing()

    async def read(self, n: int = -1):
        return await self._reader.read(n=n)

    async def read_exactly(self, n: int):
        return await self._reader.readexactly(n=n)

    async def read_until(self, separator: str):
        return await self._reader.readuntil(separator=separator)

    async def write(self, data: Any):
        self._writer.write(data)

    async def write_and_drain(self, data: Any):
        await self.write(data=data)
        await self._writer.drain()
