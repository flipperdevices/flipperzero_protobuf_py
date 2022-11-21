#!/usr/bin/env python3

import sys

from flipperzero_protobuf import *
from flipperzero_protobuf.cli_helpers import *


def print_key_value_list(kvl):
    for el in kvl:
        print(f"{el[0]} : {el[1]}")


def test_ping(proto) -> None:
    print("-- Ping --")
    print_hex(proto.rpc_system_ping())


def test_device_info(proto) -> None:
    print("-- Device Info --")
    print_key_value_list(proto.rpc_device_info())


def test_power_info(proto) -> None:
    print("-- Power Info --")
    print_key_value_list(proto.rpc_power_info())


def test_property_get(proto, key: str) -> None:
    print(f"-- Property Get ({key}) --")
    print_key_value_list(proto.rpc_property_get(key))


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <port_name>")
        exit(1)

    try:
        proto = FlipperProto(sys.argv[1])
        test_ping(proto)
        test_device_info(proto)
        test_power_info(proto)

        test_property_get(proto, "power.charge.level")
        test_property_get(proto, "power.charge")
        test_property_get(proto, "power")

        test_property_get(proto, "system.radio.fus.minor")
        test_property_get(proto, "system.radio.fus")
        test_property_get(proto, "system.hardware")
        test_property_get(proto, "system")

    except Exception as e:
        print(f"An error has occured: {e}")
        exit(1)


if __name__ == '__main__':
    main()
