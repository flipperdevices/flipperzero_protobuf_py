#!/usr/bin/env python3



from .flipperzero_protobuf_compiled import gui_pb2
from .flipper_base import InputTypeException
# from .flipper_base import *

# pylint: disable=line-too-long, no-member

__all__ = [ 'FlipperProtoGui' ]



class FlipperProtoGui:

    # StartVirtualDisplay
    # StopVirtualDisplay

    # StartScreenStream
    def cmd_gui_start_screen_stream(self):
        """Start screen stream"""
        cmd_data = gui_pb2.StartScreenStreamRequest()
        data = self._cmd_send_and_read_answer(
            cmd_data, 'gui_start_screen_stream_request')
        return data

    # StopScreenStream
    def cmd_gui_stop_screen_stream(self):
        """Stop screen stream"""
        cmd_data = gui_pb2.StopScreenStreamRequest()
        data = self._cmd_send_and_read_answer(
            cmd_data, 'gui_stop_screen_stream_request')
        return data

    def cmd_gui_snapshot_screen(self):
        """Snapshot screen"""
        self.cmd_gui_start_screen_stream()
        data = self._cmd_read_answer(0)
        self.cmd_gui_stop_screen_stream()
        return data.gui_screen_frame.data

    # SendInputEvent
    def cmd_gui_send_input_event_request(self, key, ftype):
        """Send Input Event Request Key"""
        cmd_data = gui_pb2.SendInputEventRequest()
        cmd_data.key = getattr(gui_pb2, key)
        cmd_data.type = getattr(gui_pb2, ftype)
        data = self._cmd_send_and_read_answer(
            cmd_data, 'gui_send_input_event_request')
        return data

    def cmd_gui_send_input(self, key):
        """Send Input Event Request Type"""
        ftype, key = key.split(" ")

        # if ftype != 'SHORT' and ftype != 'LONG':
        if ftype not in ['SHORT', 'LONG']:
            raise InputTypeException('Incorrect type')

         #if key != 'UP' and key != 'DOWN' and key != 'LEFT' and key != 'RIGHT' and key != 'OK' and key != 'BACK':
        if key not in ['UP', 'DOWN', 'LEFT', 'RIGHT', 'OK', 'BACK']:
            raise InputTypeException('Incorrect key')

        self.cmd_gui_send_input_event_request(key, 'PRESS')
        self.cmd_gui_send_input_event_request(key, ftype)
        self.cmd_gui_send_input_event_request(key, 'RELEASE')
