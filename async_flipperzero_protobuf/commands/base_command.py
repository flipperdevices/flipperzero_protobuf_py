from google.protobuf.internal.encoder import _VarintBytes
from flipperzero_protobuf_compiled import flipper_pb2
from connectors.base_connector import BaseConnector


class BaseCommand:
    def __init__(
        self,
        method_name: str,
        proto_class,
        command_status=flipper_pb2.CommandStatus.Value("OK"),
        has_next=False,
        callback=None,
    ):
        self.method_name = method_name
        self.proto_class = proto_class
        self.has_next = has_next
        self.command_status = command_status

    async def execute(self, command_id: int, connector: BaseConnector):
        message = self.create_message(command_id=command_id)
        await connector.write_and_drain(data=message)

    def create_message(self, command_id: int):
        cmd_data = self.proto_class()

        flipper_message = flipper_pb2.Main()
        flipper_message.command_id = command_id
        flipper_message.command_status = self.command_status
        flipper_message.has_next = self.has_next
        getattr(flipper_message, self.method_name).CopyFrom(cmd_data)
        return bytearray(_VarintBytes(flipper_message.ByteSize()) + flipper_message.SerializeToString())
