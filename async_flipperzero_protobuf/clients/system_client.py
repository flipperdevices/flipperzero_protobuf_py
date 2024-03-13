from datetime import datetime

from google.protobuf.json_format import MessageToDict
from exceptions.base_exceptions import FlipperValidateException
from commands.system_commands import (
    SystemPlayAudiovisualAlertRequestCommand,
    SystemProtobufVersionRequestCommand,
    SystemFactoryResetRequestCommand,
    SystemSetDatetimeRequestCommand,
    SystemGetDatetimeRequestCommand,
    SystemDeviceInfoRequestCommand,
    SystemPowerInfoRequestCommand,
    SystemUpdateRequestCommand,
    SystemRebootRequestCommand,
    SystemPingRequestCommand,
    StopSessionCommand,
)
from clients.base_client import FlipperBaseProtoClient


class FlipperSystemProtoClient(FlipperBaseProtoClient):
    async def system_factory_reset_request(self, wait_for_response: bool = True):
        return await self.request(
            SystemFactoryResetRequestCommand(), wait_for_response=wait_for_response, to_validate=True
        )

    async def system_update_request(self, update_manifest: str, wait_for_response: bool = True):
        return await self.request(
            SystemUpdateRequestCommand(update_manifest=update_manifest),
            wait_for_response=wait_for_response,
            to_validate=True,
        )

    async def system_reboot_request(self, mode: str, wait_for_response: bool = True):
        return await self.request(
            SystemRebootRequestCommand(mode=mode),
            wait_for_response=wait_for_response,
            to_validate=False,  # don't validate
        )

    async def system_power_info_request(self, wait_for_response: bool = True):
        stream = await self.stream(SystemPowerInfoRequestCommand())

        response = await stream.__anext__()

        if response.command_status != 0:
            raise FlipperValidateException(
                f'Command status is not equal to 0, given command: {response.command_status}'
            )

        result = [(response.system_power_info_response.key, response.system_power_info_response.value)]

        while response.has_next:
            response = await stream.__anext__()
            result.append((response.system_power_info_response.key, response.system_power_info_response.value))

        return result

    async def system_device_info_request(self, wait_for_response: bool = True):
        stream = await self.stream(SystemDeviceInfoRequestCommand())

        response = await stream.__anext__()

        if response.command_status != 0:
            raise FlipperValidateException(
                f'Command status is not equal to 0, given command: {response.command_status}'
            )

        result = [(response.system_device_info_response.key, response.system_device_info_response.value)]

        while response.has_next:
            response = await stream.__anext__()
            result.append((response.system_device_info_response.key, response.system_device_info_response.value))

        return result

    async def system_protobuf_version_request(self, wait_for_response: bool = True):
        response = await self.request(
            SystemProtobufVersionRequestCommand(), wait_for_response=wait_for_response, to_validate=True
        )
        return (
            response.system_protobuf_version_response.major,
            response.system_protobuf_version_response.minor,
        )

    async def system_get_datetime_request(self, wait_for_response: bool = True):
        response = await self.request(
            SystemGetDatetimeRequestCommand(), wait_for_response=wait_for_response, to_validate=True
        )
        return MessageToDict(response.system_get_datetime_response)["datetime"]

    async def system_set_datetime_request(self, date: dict | datetime = None, wait_for_response: bool = True):
        if date is None:
            date = datetime.now()
        return await self.request(
            SystemSetDatetimeRequestCommand(date=date), wait_for_response=wait_for_response, to_validate=True
        )

    async def system_ping_request(self, data: bytes = bytes([0xDE, 0xAD, 0xBE, 0xEF]), wait_for_response: bool = True):
        response = await self.request(
            SystemPingRequestCommand(data=data), wait_for_response=wait_for_response, to_validate=True
        )
        return response.system_ping_response.data

    async def system_play_audiovisual_alert_request(self, wait_for_response: bool = True):
        return await self.request(
            SystemPlayAudiovisualAlertRequestCommand(), wait_for_response=wait_for_response, to_validate=True
        )

    async def stop_session(self, wait_for_response: bool = True):
        return await self.request(StopSessionCommand(), wait_for_response=wait_for_response, to_validate=True)
