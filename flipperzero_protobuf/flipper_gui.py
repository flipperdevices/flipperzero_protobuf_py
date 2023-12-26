#!/usr/bin/env python3
"""
FlipperProto Input UI function Class
"""

from .flipper_base import FlipperProtoException, InputTypeException
from .flipperzero_protobuf_compiled import gui_pb2

# from .flipper_base import *

# pylint: disable=line-too-long, no-member

__all__ = ["FlipperProtoGui"]

"""
    InputKey
        0 UP
        1 DOWN
        2 RIGHT
        3 LEFT
        4 OK

    InputType
        1 RELEASE
        2 SHORT
        3 LONG
        4 REPEAT
"""


class FlipperProtoGui:
    """
    FlipperProto Input UI function Class
    """

    # StartVirtualDisplay
    def rpc_start_virtual_display(self, data) -> None:
        """Start Virtual Display

        Parameters
        ----------
        data : bytes

        Returns
        -------
        None

        Raises
        ----------
        FlipperProtoException

        """

        cmd_data = gui_pb2.StartVirtualDisplayRequest()
        cmd_data.first_frame.data = data
        rep_data = self._rpc_send_and_read_answer(
            cmd_data, "gui_start_virtual_display_request"
        )
        if rep_data.command_status != 0:
            raise FlipperProtoException(
                self.Status_values_by_number[rep_data.command_status].name
            )

    # SendVirtualDisplayFrame
    def rpc_send_virtual_display_frame(self, data) -> None:
        """Send Frame to Virtual Display

        Parameters
        ----------
        data : bytes

        Returns
        -------
        None

        """
        cmd_data = gui_pb2.ScreenFrame()
        cmd_data.data = data
        self._rpc_send(cmd_data, "gui_screen_frame")

    # StopVirtualDisplay
    def rpc_stop_virtual_display(self) -> None:
        """Stop Virtual Display

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ----------
        FlipperProtoException

        """

        cmd_data = gui_pb2.StopVirtualDisplayRequest()
        rep_data = self._rpc_send_and_read_answer(
            cmd_data, "gui_stop_virtual_display_request"
        )
        if rep_data.command_status != 0:
            raise FlipperProtoException(
                self.Status_values_by_number[rep_data.command_status].name
            )

    # StartScreenStream
    def rpc_gui_start_screen_stream(self) -> None:
        """Start screen stream

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ----------
        FlipperProtoException

        """

        cmd_data = gui_pb2.StartScreenStreamRequest()
        rep_data = self._rpc_send_and_read_answer(
            cmd_data, "gui_start_screen_stream_request"
        )
        if rep_data.command_status != 0:
            raise FlipperProtoException(
                self.Status_values_by_number[rep_data.command_status].name
            )

    # StopScreenStream
    def rpc_gui_stop_screen_stream(self) -> None:
        """Stop screen stream

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ----------
        FlipperProtoException

        """

        cmd_data = gui_pb2.StopScreenStreamRequest()
        rep_data = self._rpc_send_and_read_answer(
            cmd_data, "gui_stop_screen_stream_request"
        )

        if rep_data.command_status != 0:
            raise FlipperProtoException(
                self.Status_values_by_number[rep_data.command_status].name
            )

    def rpc_gui_snapshot_screen(self) -> bytes:
        """Snapshot screen

        Parameters
        ----------
        None

        Returns
        -------
            bytes

        Raises
        ----------
        FlipperProtoException

        """

        self.rpc_gui_start_screen_stream()
        data = self._rpc_read_answer(0)
        self.rpc_gui_stop_screen_stream()
        return data.gui_screen_frame.data

    # SendInputEvent
    def rpc_gui_send_input_event_request(self, key, itype) -> None:
        """Send Input Event Request Key

        Parameters
        ----------
        key : str
            'UP', 'DOWN', 'RIGHT', 'LEFT', 'OK'
        itype : str
            'PRESS', 'RELEASE', 'SHORT', 'LONG', 'REPEAT'

        Returns
        -------
        None

        Raises
        ----------
        FlipperProtoException

        """

        cmd_data = gui_pb2.SendInputEventRequest()
        cmd_data.key = getattr(gui_pb2, key)
        cmd_data.type = getattr(gui_pb2, itype)
        rep_data = self._rpc_send_and_read_answer(
            cmd_data, "gui_send_input_event_request"
        )

        if rep_data.command_status != 0:
            raise FlipperProtoException(
                f"{self.Status_values_by_number[rep_data.command_status].name} {key}, {itype}"
            )

    def rpc_gui_send_input(self, key_arg) -> None:
        """Send Input Event Request Type

        Parameters
        ----------
        key_arg : tuple
            tuple = (InputKey, InputType)
            valid InputKeykey values: 'UP', 'DOWN', 'RIGHT', 'LEFT', 'OK'
            valid InputType values: 'PRESS', 'RELEASE', 'SHORT', 'LONG', 'REPEAT'

        Returns
        -------
        None

        Raises
        ----------
        FlipperProtoException
        InputTypeException

        """
        itype, ikey = key_arg.split(" ")

        # if itype != 'SHORT' and itype != 'LONG':
        if itype not in ["SHORT", "LONG"]:
            raise InputTypeException("Incorrect type")

        # if ikey != 'UP' and ikey != 'DOWN' and ikey != 'LEFT' and ikey != 'RIGHT' and ikey != 'OK' and ikey != 'BACK':
        if ikey not in ["UP", "DOWN", "LEFT", "RIGHT", "OK", "BACK"]:
            raise InputTypeException("Incorrect key")

        self.rpc_gui_send_input_event_request(ikey, "PRESS")
        self.rpc_gui_send_input_event_request(ikey, itype)
        self.rpc_gui_send_input_event_request(ikey, "RELEASE")
