from commands.desktop_commands import (
    DesktopIsLockedRequestCommand,
    DesktopUnlockRequestCommand,
)
from clients.base_client import FlipperBaseProtoClient


class FlipperDesktopProtoClient(FlipperBaseProtoClient):
    async def desktop_is_locked_request(self, wait_for_response: bool = True):
        return await self.request(
            DesktopIsLockedRequestCommand(), wait_for_response=wait_for_response, to_validate=True
        )

    async def desktop_unlock_request(self, wait_for_response: bool = True):
        return await self.request(DesktopUnlockRequestCommand(), wait_for_response=wait_for_response, to_validate=True)
