from commands.gui_commands import (
    StartVirtualDisplayRequestCommand,
    StopVirtualDisplayRequestCommand,
    StartScreenStreamRequestCommand,
    StopScreenStreamRequestCommand,
    SendInputEventRequestCommand,
)
from clients.base_client import FlipperBaseProtoClient


class FlipperGUIProtoClient(FlipperBaseProtoClient):
    async def gui_send_input_event_request(self, key: str, itype: str, wait_for_response: bool = True):
        """
        Parameters
        ----------
        key : str
            'UP', 'DOWN', 'RIGHT', 'LEFT', 'OK'
        itype : str
            'PRESS', 'RELEASE', 'SHORT', 'LONG', 'REPEAT'
        :return:
        """
        return await self.request(
            SendInputEventRequestCommand(key=key, itype=itype), wait_for_response=wait_for_response, to_validate=True
        )

    async def gui_start_virtual_display_request(self, data: bytes, wait_for_response: bool = True):
        return await self.request(
            StartVirtualDisplayRequestCommand(data=data), wait_for_response=wait_for_response, to_validate=True
        )

    async def gui_stop_virtual_display_request(self, wait_for_response: bool = True):
        return await self.request(
            StopVirtualDisplayRequestCommand(), wait_for_response=wait_for_response, to_validate=True
        )

    async def gui_start_screen_stream_request(self, wait_for_response: bool = True):
        return await self.request(
            StartScreenStreamRequestCommand(), wait_for_response=wait_for_response, to_validate=True
        )

    async def gui_stop_screen_stream_request(self, wait_for_response: bool = True):
        return await self.request(
            StopScreenStreamRequestCommand(), wait_for_response=wait_for_response, to_validate=True
        )

    async def snapshot_screen(self, wait_for_response: bool = True):
        raise NotImplementedError()  # TODO implement it
