#!/usr/bin/env python3


from google.protobuf.internal.encoder import _VarintBytes

from flipperzero_protobuf_compiled import flipper_pb2, system_pb2, gui_pb2


class Varint32Exception(Exception):
    pass


class ProtoFlipper:
    def __init__(self, serial):
        self._serial = serial
        self._command_id = 0

    def read_varint_32(self):
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
        self._command_id += 1
        result = self._command_id
        return result

    def _cmd_send(self, cmd_data, cmd_name, has_next=False):
        flipper_message = flipper_pb2.Main()
        flipper_message.command_id = self._get_command_id()
        flipper_message.command_status = flipper_pb2.CommandStatus.Value('OK')
        flipper_message.has_next = has_next
        getattr(flipper_message, cmd_name).CopyFrom(cmd_data)
        data = bytearray(_VarintBytes(flipper_message.ByteSize()
                                      ) + flipper_message.SerializeToString())
        self._serial.write(data)

    def _cmd_read_answer(self, command_id=None):
        if command_id == None:
            command_id = self._command_id

        while True:
            data = self._cmd_read_any()
            if data.command_id == command_id:
                break
        return data

    def _cmd_read_any(self):
        length = self.read_varint_32()
        data = flipper_pb2.Main()
        data.ParseFromString(self._serial.read(size=length))
        return data

    def cmd_system_ping(self, data=bytes([0xde, 0xad, 0xbe, 0xef])):
        cmd_data = system_pb2.PingRequest()
        cmd_data.data = data
        self._cmd_send(cmd_data, 'system_ping_request')
        data = self._cmd_read_answer()
        return data.system_ping_response.data

    def cmd_system_audiovisual_alert(self):
        cmd_data = system_pb2.PlayAudiovisualAlertRequest()
        self._cmd_send(cmd_data, 'system_play_audiovisual_alert_request')
        data = self._cmd_read_answer()
        return data

    def cmd_gui_start_screen_stream(self):
        cmd_data = gui_pb2.StartScreenStreamRequest()
        self._cmd_send(cmd_data, 'gui_start_screen_stream_request')
        data = self._cmd_read_answer()
        return data

    def cmd_gui_stop_screen_stream(self):
        cmd_data = gui_pb2.StopScreenStreamRequest()
        self._cmd_send(cmd_data, 'gui_stop_screen_stream_request')
        data = self._cmd_read_answer()
        return data

    def cmd_gui_snapshot_screen(self):
        self.cmd_gui_start_screen_stream()
        data = self._cmd_read_answer(0)
        self.cmd_gui_stop_screen_stream()
        return data.gui_screen_frame.data
