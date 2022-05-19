# Python bindings for Flipper Zero protobuf protocol

Since our naming strategy is to use a "-" instead of "_", importing a submodule is not trivial.

```
import sys
import serial
import importlib

protoflipper_module = importlib.import_module(
    "flipperzero-protobuf-py.flipper_protobuf")


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

    # construct protobuf class
    proto = protoflipper_module.ProtoFlipper(flipper)
    #       ^^^^^^^^^^^^^^^^^^^

    print("Ping result: ")
    print(proto.cmd_system_ping())

if __name__ == '__main__':
    main()
```