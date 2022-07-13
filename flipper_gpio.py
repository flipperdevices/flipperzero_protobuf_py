#!/usr/bin/env python3

#import sys
#import os

# from nis import match
# from google.protobuf.internal.encoder import _VarintBytes
# from numpy import mat

# pylint: disable=line-too-long, no-member

from .flipperzero_protobuf_compiled import  gpio_pb2

__all__ = [ 'FlipperProtoGpio' ]

class FlipperProtoGpio:

    # GetPinMode

    # SetPinMode
    def cmd_gpio_set_pin_mode(self, pin, mode):
        cmd_data = gpio_pb2.SetPinMode()
        cmd_data.pin = pin
        cmd_data.mode = mode

        return self._cmd_send_and_read_answer(cmd_data, "gpio_set_pin_mode")

    # WritePin
    def cmd_gpio_write_pin(self, pin, value):
        cmd_data = gpio_pb2.WritePin()
        cmd_data.pin = pin
        cmd_data.value = value

        return self._cmd_send_and_read_answer(cmd_data, "gpio_write_pin")

    # ReadPin
    def cmd_gpio_read_pin(self, pin):
        cmd_data = gpio_pb2.ReadPin()
        cmd_data.pin = pin

        return self._cmd_send_and_read_answer(cmd_data, "gpio_read_pin")

    # SetInputPull
    def cmd_gpio_set_input_pull(self, pin, pull_mode):
        cmd_data = gpio_pb2.SetInputPull()
        cmd_data.pin = pin
        cmd_data.pull_mode = pull_mode

        return self._cmd_send_and_read_answer(cmd_data, "gpio_set_input_pull")
