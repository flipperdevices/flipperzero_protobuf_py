#!/usr/bin/env python3
"""FlipperProto Class init function calls"""

import sys
import os
from typing import Union
import serial
import serial.tools.list_ports

from google.protobuf.internal.encoder import _VarintBytes

# pylint: disable=line-too-long, no-member

from .version import __version__
from .flipperzero_protobuf_compiled import flipper_pb2

# VERSION = '0.1.20220806'

__all__ = ['Varint32Exception', 'InputTypeException',
           'FlipperProtoBase', 'FlipperProtoException']


class Varint32Exception(Exception):
    """Protobuf protocal communication error Exception"""


class InputTypeException(Exception):
    """FlipperProto input error Exception"""


class FlipperProtoException(Exception):
    """FlipperProto callback Exception"""
    def __init__(self, msg):
        Exception.__init__(self, msg)


class FlipperProtoBase:
    """Meta base Class for FlipperProto"""

    def __init__(self, serial_port=None, debug=0) -> None:

        # self.info = {}

        self._debug = debug
        self._in_session = False        # flag if connecion if in RPC or command mode
        self.version = __version__

        self._command_id = 0
        if isinstance(serial_port, serial.Serial):
            self._serial = serial_port
        else:
            try:
                self._serial = self._open_serial(serial_port)
                # print("._get_startup_info")
                self.device_info = self._get_startup_info()
                self.start_rpc_session()
            except serial.serialutil.SerialException as e:
                print(f"SerialException: {e}")
                sys.exit(0)

        # for easy lookup later
        self.Status_values_by_number = flipper_pb2.DESCRIPTOR.enum_types_by_name['CommandStatus'].values_by_number

    def port(self) -> str:
        """Return serial port"""
        if self._serial is None:
            return ""
        return self._serial.port

    def _get_startup_info(self) -> dict:
        """read / record info during startip"""
        # cache some data
        ret = {}
        self._serial.read_until(b'>: ')
        self._serial.write(b"!\r")
        while True:
            r = self._serial.readline().decode('utf-8')

            if r.startswith('>: '):
                break
            if r.startswith('\r\n'):
                break

            if len(r) > 5:
                k, v = r.split(':')
                ret[k.strip()] = v.strip()

        return ret

    # COM4: USB Serial Device (COM4) [USB VID:PID=0483:5740 SER=FLIP_UNYANA LOCATION=1-3:x.0]
    # /dev/cu.usbmodemflip_Unyana1: Flipper Unyana [USB VID:PID=0483:5740 SER=flip_Unyana LOCATION=20-2]
    def _find_port(self) -> Union[str, None]:  # -> str | None:
        """find serial device"""

        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in ports:
            if self._debug:
                print(f"{port}: {desc} [{hwid}]")

            a = hwid.split()
            if 'VID:PID=0483:5740' in a:
                return port

            # a[2].startswith("SER=flip")
            # if desc.startswith("Flipper") or desc.startswith("Rogue"):
            #     return port

        return None

    def _open_serial(self, dev=None) -> serial.Serial:
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

        return flipper

    def send_cmd(self, cmd_str) -> None:
        """ send non rpc command to flipper """
        if self._in_session:
            raise FlipperProtoException('rpc_session is active')

        self._serial.read_until(b'>: ')
        self._serial.write(cmd_str + '\r')

        while True:

            r = self._serial.readline().decode('utf-8')
            print(r)

            if r.startswith('>: '):
                break

    def start_rpc_session(self) -> None:
        """ start rpc session """
        # wait for prompt
        self._serial.read_until(b'>: ')

        # send command and skip answer
        self._serial.write(b"start_rpc_session\r")
        self._serial.read_until(b'\n')
        self._in_session = True

    def _read_varint_32(self) -> int:
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

    def _get_command_id(self) -> int:
        """Increment and get command id"""
        self._command_id += 1
        result = self._command_id
        return result

    def _rpc_send(self, cmd_data, cmd_name, has_next=None, command_id=None) -> None:
        """Send command"""

        if self._in_session is False:
            raise FlipperProtoException('rpc_session is not active')

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

    def _rpc_send_and_read_answer(self, cmd_data, cmd_name, has_next=False, command_id=None) -> flipper_pb2.Main:
        """Send command and read answer"""
        self._rpc_send(cmd_data, cmd_name, has_next=has_next, command_id=command_id)
        return self._rpc_read_answer()

    def _rpc_read_answer(self, command_id=None) -> flipper_pb2.Main:
        """Read answer from serial port and filter by command id"""
        # message->DebugString()

        if self._in_session is False:
            raise FlipperProtoException('rpc_session is not active')

        if command_id is None:
            command_id = self._command_id

        while True:
            data = self._rpc_read_any()
            if data.command_id == command_id:
                break
        return data

    def _rpc_read_any(self) -> flipper_pb2.Main:
        """Read answer from serial port"""
        length = self._read_varint_32()
        data = flipper_pb2.Main()
        data.ParseFromString(self._serial.read(size=length))
        return data
