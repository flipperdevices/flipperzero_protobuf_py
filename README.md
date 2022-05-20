# Python bindings for Flipper Zero protobuf protocol

Example:
```
#!/usr/bin/env python3

import sys
import serial

from flipperzero_protobuf_py.flipper_protobuf import ProtoFlipper
from flipperzero_protobuf_py.cli_helpers import *


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

    proto.cmd_gui_send_input("SHORT UP")

    print("Screen capture result: ")
    print_screen(proto.cmd_gui_snapshot_screen())


if __name__ == '__main__':
    main()
```
