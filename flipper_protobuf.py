#!/usr/bin/env python3

from nis import match
from google.protobuf.internal.encoder import _VarintBytes
from numpy import mat

from .flipperzero_protobuf_compiled import flipper_pb2, system_pb2, gui_pb2, application_pb2


class Varint32Exception(Exception):
    pass


class InputTypeException(Exception):
    pass


class ProtoFlipper:
    def __init__(self, serial):
        self._serial = serial
        self._command_id = 0

    def _read_varint_32(self):
        """Read varint from serial port"""
        MASK = (1 << 32) - 1

        result = 0
        shift = 0
        while 1:
            b = int.from_bytes(self._serial.read(size=1),
                               byteorder='little', signed=False)
            result |= ((b & 0x7f) << shift)
            if not (b & 0x80):
                result &= MASK
                result = int(result)
                return result
            shift += 7
            if shift >= 64:
                raise Varint32Exception(
                    'Too many bytes when decoding varint.')

    def _get_command_id(self):
        """Increment and get command id"""
        self._command_id += 1
        result = self._command_id
        return result

    def _cmd_send(self, cmd_data, cmd_name, has_next=False):
        """Send command"""
        flipper_message = flipper_pb2.Main()
        flipper_message.command_id = self._get_command_id()
        flipper_message.command_status = flipper_pb2.CommandStatus.Value('OK')
        flipper_message.has_next = has_next
        getattr(flipper_message, cmd_name).CopyFrom(cmd_data)
        data = bytearray(_VarintBytes(flipper_message.ByteSize()
                                      ) + flipper_message.SerializeToString())
        self._serial.write(data)

    def _cmd_send_and_read_answer(self, cmd_data, cmd_name, has_next=False):
        """Send command and read answer"""
        self._cmd_send(cmd_data, cmd_name, has_next)
        return self._cmd_read_answer()

    def _cmd_read_answer(self, command_id=None):
        """Read answer from serial port and filter by command id"""
        if command_id == None:
            command_id = self._command_id

        while True:
            data = self._cmd_read_any()
            if data.command_id == command_id:
                break
        return data

    def _cmd_read_any(self):
        """Read answer from serial port"""
        length = self._read_varint_32()
        data = flipper_pb2.Main()
        data.ParseFromString(self._serial.read(size=length))
        return data

    def cmd_system_ping(self, data=bytes([0xde, 0xad, 0xbe, 0xef])):
        """Ping flipper"""
        cmd_data = system_pb2.PingRequest()
        cmd_data.data = data
        data = self._cmd_send_and_read_answer(cmd_data, 'system_ping_request')
        return data.system_ping_response.data

    def cmd_system_audiovisual_alert(self):
        """Launch audiovisual alert on flipper"""
        cmd_data = system_pb2.PlayAudiovisualAlertRequest()
        data = self._cmd_send_and_read_answer(
            cmd_data, 'system_play_audiovisual_alert_request')
        return data

    def cmd_gui_start_screen_stream(self):
        """Start screen stream"""
        cmd_data = gui_pb2.StartScreenStreamRequest()
        data = self._cmd_send_and_read_answer(
            cmd_data, 'gui_start_screen_stream_request')
        return data

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

    def cmd_gui_send_input_event_request(self, key, type):
        """Send Input Event Request Key"""
        cmd_data = gui_pb2.SendInputEventRequest()
        cmd_data.key = getattr(gui_pb2, key)
        cmd_data.type = getattr(gui_pb2, type)
        data = self._cmd_send_and_read_answer(
            cmd_data, 'gui_send_input_event_request')
        return data

    def cmd_gui_send_input(self, key):
        """Send Input Event Request Type"""
        type, key = key.split(" ")

        if type != 'SHORT' and type != 'LONG':
            raise InputTypeException('Incorrect type')

        if key != 'UP' and key != 'DOWN' and key != 'LEFT' and key != 'RIGHT' and key != 'OK' and key != 'BACK':
            raise InputTypeException('Incorrect key')

        self.cmd_gui_send_input_event_request(key, 'PRESS')
        self.cmd_gui_send_input_event_request(key, type)
        self.cmd_gui_send_input_event_request(key, 'RELEASE')
    
    def cmd_app_start(self, name, args):
        """Start application"""
        cmd_data = application_pb2.StartRequest()
        cmd_data.name = name
        cmd_data.args = args
        data = self._cmd_send_and_read_answer(cmd_data, 'app_start_request')
        return data

    def cmd_app_exit(self):
        """Send exit command to app"""
        cmd_data = application_pb2.AppExitRequest()
        data = self._cmd_send_and_read_answer(cmd_data, 'app_exit_request')
        return data

    def cmd_app_load_file(self, path):
        """Send load file command to app"""
        cmd_data = application_pb2.AppLoadFileRequest()
        cmd_data.path = path
        data = self._cmd_send_and_read_answer(cmd_data, 'app_load_file_request')
        return data

    def cmd_app_button_press(self, args):
        """Send button press command to app"""
        cmd_data = application_pb2.AppButtonPressRequest()
        cmd_data.args = args
        data = self._cmd_send_and_read_answer(cmd_data, 'app_button_press_request')
        return data

    def cmd_app_button_release(self):
        """Send button release command to app"""
        cmd_data = application_pb2.AppButtonReleaseRequest()
        data = self._cmd_send_and_read_answer(cmd_data, 'app_button_release_request')
        return data

    def cmd_flipper_stop_session(self):
        """Stop RPC session"""
        cmd_data = flipper_pb2.StopSession()
        data = self._cmd_send(
            cmd_data, 'stop_session')
        return data