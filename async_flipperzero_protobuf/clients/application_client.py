from commands.application_commands import (
    ApplicationButtonReleaseRequestCommand,
    ApplicationDataExchangeRequestCommand,
    ApplicationButtonPressRequestCommand,
    ApplicationLockStatusRequestCommand,
    ApplicationLoadFileRequestCommand,
    ApplicationGetErrorRequestCommand,
    ApplicationStartRequestCommand,
    ApplicationExitRequestCommand,
)
from clients.base_client import FlipperBaseProtoClient


class FlipperApplicationProtoClient(FlipperBaseProtoClient):
    async def app_lock_status_request(self, wait_for_response: bool = True):
        return await self.request(
            ApplicationLockStatusRequestCommand(), wait_for_response=wait_for_response, to_validate=True
        )

    async def app_start_request(self, name: str, args: str, wait_for_response: bool = True):
        return await self.request(
            ApplicationStartRequestCommand(name=name, args=args), wait_for_response=wait_for_response, to_validate=True
        )

    async def app_exit_request(self, wait_for_response: bool = True):
        return await self.request(
            ApplicationExitRequestCommand(), wait_for_response=wait_for_response, to_validate=True
        )

    async def app_load_file_request(self, path: str, wait_for_response: bool = True):
        return await self.request(
            ApplicationLoadFileRequestCommand(path=path), wait_for_response=wait_for_response, to_validate=True
        )

    async def app_button_press_request(self, args: str, wait_for_response: bool = True):
        return await self.request(
            ApplicationButtonPressRequestCommand(args=args), wait_for_response=wait_for_response, to_validate=True
        )

    async def app_button_release_request(self, wait_for_response: bool = True):
        return await self.request(
            ApplicationButtonReleaseRequestCommand(), wait_for_response=wait_for_response, to_validate=True
        )

    async def app_get_error_request(self, wait_for_response: bool = True):
        return await self.request(
            ApplicationGetErrorRequestCommand(), wait_for_response=wait_for_response, to_validate=True
        )

    async def app_data_exchange_request(self, data: bytes, wait_for_response: bool = True):
        return await self.request(
            ApplicationDataExchangeRequestCommand(data=data), wait_for_response=wait_for_response, to_validate=True
        )

    async def data_exchange_receive(self):
        raise NotImplementedError()  # TODO: implement it
