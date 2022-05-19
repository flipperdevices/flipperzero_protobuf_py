#!/usr/bin/env python3

import sys
import serial

from cli_helpers import print_hex, print_screen
from flipper_protobuf import ProtoFlipper


def main():
    # open serial port
    flipper = serial.Serial(sys.argv[1], timeout=1)
    flipper.baudrate = 230400
    flipper.flushOutput()
    flipper.flushInput()

    # disable timeout
    flipper.timeout = None

    # wait for prompt
    flipper.read_until(b'>: ')

    # send command and skip answer
    flipper.write(b"start_rpc_session\r")
    flipper.read_until(b'\n')

    # construct protobuf worker
    proto = ProtoFlipper(flipper)

    print("Ping result: ")
    print_hex(proto.cmd_system_ping())

    proto.cmd_gui_send_input_long_down()

    print("Screen capture result: ")
    print_screen(proto.cmd_gui_snapshot_screen())


if __name__ == '__main__':
    main()
