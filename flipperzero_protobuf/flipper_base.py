#!/usr/bin/env python3

# pylint: disable=too-few-public-methods

import sys
import os
import serial
import serial.tools.list_ports

from google.protobuf.internal.encoder import _VarintBytes

# pylint: disable=line-too-long, no-member

from .flipperzero_protobuf_compiled import flipper_pb2

__all__ = ['Varint32Exception', 'InputTypeException', 'cmdException',
           'FlipperProtoBase']


class Varint32Exception(Exception):
    pass


class InputTypeException(Exception):
    pass


class cmdException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class FlipperProtoBase:
    def __init__(self, serial_port=None, debug=0):

        self.rdir = '/ext'

        # self.info = {}

        self._debug = debug
        self._in_session = False

        self._command_id = 0
        if isinstance(serial_port, serial.Serial):
            self._serial = serial_port
        else:
            try:
                self._serial = self._open_serial(serial_port)
                self.start_rpc_session()
            except serial.serialutil.SerialException as e:
                print(f"SerialException: {e}")
                sys.exit(0)

        self.Status_values_by_number = flipper_pb2.DESCRIPTOR.enum_types_by_name['CommandStatus'].values_by_number

    def port(self):
        return self._serial.port

    def _find_port(self):
        """find serial device"""

        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in ports:
            if self._debug:
                print(f"{port}: {desc} [{hwid}]")
            if desc.startswith("Flipper"):
                return port
            # print("{}: {} [{}]".format(port, desc, hwid))

        return None

    def _open_serial(self, dev=None):   # get_startup_info=False):
        """open serial device"""

        serial_dev = dev or self._find_port()

        if serial_dev is None:
            print("can not find Flipper serial dev")
            sys.exit(0)

        if not os.path.exists(serial_dev):
            print(f"can not open {serial_dev}")
            sys.exit(0)

        if self._debug:
            print(f"Using port {serial_dev}")

        # open serial port
        # serial.serialutil.SerialException
        # flipper = serial.Serial(sys.argv[1], timeout=1)
        flipper = serial.Serial(serial_dev, timeout=1)
        flipper.baudrate = 230400
        flipper.flushOutput()
        flipper.flushInput()

        # disable timeout
        flipper.timeout = None

        # wait for prompt
        # flipper.read_until(b'>: ')

        # cache some data
        # if get_startup_info:
        #     flipper.write(b"!\r\r")
        #     while True:
        #
        #         r = flipper.readline().decode('utf-8')
        #
        #         if r.startswith('>: '):
        #             break
        #
        #         if len(r) > 5:
        #             k, v = r.split(':')
        #             self.info[k.strip()] = v.strip()

        return flipper

    def send_cmd(self, cmd_str):
        """ send non rpc command to flipper """
        if self._in_session:
            raise cmdException('rpc_session is active')

        self._serial.read_until(b'>: ')
        self._serial.write(cmd_str + '\r')

        while True:

            r = self._serial.readline().decode('utf-8')
            print(r)

            if r.startswith('>: '):
                break

    def start_rpc_session(self):
        """ start rpc session """
        # wait for prompt
        self._serial.read_until(b'>: ')

        # send command and skip answer
        self._serial.write(b"start_rpc_session\r")
        self._serial.read_until(b'\n')
        self._in_session = True

    def _read_varint_32(self):
        """Read varint from serial port"""
        MASK = (1 << 32) - 1

        result = 0
        shift = 0
        while 1:
            b = int.from_bytes(self._serial.read(size=1),
                               byteorder='little', signed=False)
            result |= ((b & 0x7f) << shift)

            if not b & 0x80:
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

    def _rpc_send(self, cmd_data, cmd_name, has_next=None, command_id=None):
        """Send command"""

        if self._in_session is False:
            raise cmdException('rpc_session is not active')

        flipper_message = flipper_pb2.Main()
        if command_id is None:
            flipper_message.command_id = self._get_command_id()
        else:
            flipper_message.command_id = command_id

        flipper_message.command_status = flipper_pb2.CommandStatus.Value('OK')
        if has_next:
            flipper_message.has_next = has_next
        getattr(flipper_message, cmd_name).CopyFrom(cmd_data)
        data = bytearray(_VarintBytes(flipper_message.ByteSize()
                                      ) + flipper_message.SerializeToString())
        self._serial.write(data)

    def _rpc_send_and_read_answer(self, cmd_data, cmd_name, has_next=False, command_id=None):
        """Send command and read answer"""
        self._rpc_send(cmd_data, cmd_name, has_next=has_next, command_id=command_id)
        return self._rpc_read_answer()

    def _rpc_read_answer(self, command_id=None):
        """Read answer from serial port and filter by command id"""
        # message->DebugString()

        if self._in_session is False:
            raise cmdException('rpc_session is not active')

        if command_id is None:
            command_id = self._command_id

        while True:
            data = self._rpc_read_any()
            if data.command_id == command_id:
                break
        return data

    def _rpc_read_any(self):
        """Read answer from serial port"""
        length = self._read_varint_32()
        data = flipper_pb2.Main()
        data.ParseFromString(self._serial.read(size=length))
        return data
