from clients.application_client import FlipperApplicationProtoClient
from connectors.base_connector import BaseConnector
from clients.property_client import FlipperPropertyProtoClient
from clients.storage_client import FlipperStorageProtoClient
from clients.desktop_client import FlipperDesktopProtoClient
from clients.system_client import FlipperSystemProtoClient
from clients.gpio_client import FlipperGPIOProtoClient
from clients.base_client import FlipperBaseProtoClient
from clients.gui_client import FlipperGUIProtoClient
from executor import FlipperProtoExecutor


class FlipperProtobufClient(FlipperBaseProtoClient):
    def __init__(self, connector: BaseConnector):
        self.connector = connector
        self.executor = FlipperProtoExecutor(connector=connector)

        self.application = FlipperApplicationProtoClient(executor=self.executor)
        self.desktop = FlipperDesktopProtoClient(executor=self.executor)
        self.gpio = FlipperGPIOProtoClient(executor=self.executor)
        self.gui = FlipperGUIProtoClient(executor=self.executor)
        self.property = FlipperPropertyProtoClient(executor=self.executor)
        self.storage = FlipperStorageProtoClient(executor=self.executor)
        self.system = FlipperSystemProtoClient(executor=self.executor)

    async def __aenter__(self):
        await self.connector.open_connection()

        await self.connector.read_until(b">: ")
        await self.connector.write(b"start_rpc_session\r")
        await self.connector.read_until(b"\n")

        await self.executor.start()

        return self

    async def __aexit__(self, *args):
        await self.connector.close_connection()
        await self.executor.stop()
