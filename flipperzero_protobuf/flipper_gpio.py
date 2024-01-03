#!/usr/bin/env python3
"""
FlipperProto GPIO function Class
"""

# import sys
# import os

# from nis import match
# from google.protobuf.internal.encoder import _VarintBytes

# pylint: disable=line-too-long, no-member

from .flipper_base import FlipperProtoException, InputTypeException
from .flipperzero_protobuf_compiled import gpio_pb2

__all__ = ["FlipperProtoGpio"]


class FlipperProtoGpio:
    """

     Methods
     -------
    cmd_gpio_get_pin_mode(pin):
            get GPIO pin mode

    cmd_gpio_set_pin_mode(pin, mode):
            set GPIO pin mode

    cmd_gpio_write_pin(pin, value):
            set GPIO pin

    cmd_gpio_read_pin(pin):
            query GPIO pin

    cmd_gpio_set_input_pull(pin, pull_mode):
            Set GPIO pill Input

        GpioPin ID:
            0 = 'PC0'
            1 = 'PC1'
            2 = 'PC3'
            3 = 'PB2'
            4 = 'PB3'
            5 = 'PA4'
            6 = 'PA6'
            7 = 'PA7'

        GpioInputPull
            0 = 'NO'
            1 = 'UP'
            2 = 'DOWN'

        GpioPinMode
            0 = 'OUTPUT'
            1 = 'INPUT'
    """

    # GetPinMode
    def rpc_gpio_get_pin_mode(self, pin) -> str:
        """get GPIO pin mode

        Parameters
        ----------
        pin : int or str
            0 = 'PC0'
            1 = 'PC1'
            2 = 'PC3'
            3 = 'PB2'
            4 = 'PB3'
            5 = 'PA4'
            6 = 'PA6'
            7 = 'PA7'

        Returns:
        ----------
        str
            'OUTPUT'
            'INPUT'

        Raises
        ----------
        InputTypeException
        FlipperProtoException

        """

        cmd_data = gpio_pb2.GetPinMode()
        if pin not in ["PC0", "PC1", "PC3", "PB2", "PB3", "PA4", "PA6", "PA7"]:
            raise InputTypeException("Invalid pin")

        if isinstance(pin, int):
            cmd_data.pin = pin
        else:
            cmd_data.pin = getattr(gpio_pb2, pin)

        # if _debug:
        #    print(f"gpio_pb2.GetPinMode pin={pin} cmd_data.pin={cmd_data.pin}")

        rep_data = self._rpc_send_and_read_answer(cmd_data, "gpio_get_pin_mode")

        # gpio_pb2.DESCRIPTOR.enum_types_by_name['GpioPinMode'].values_by_number[0].name
        if rep_data.command_status != 0:
            raise FlipperProtoException(
                f"{self.Status_values_by_number[rep_data.command_status].name} pin={pin}"
            )

        # return rep_data.gpio_get_pin_mode_response.mode
        return (
            gpio_pb2.DESCRIPTOR.enum_types_by_name["GpioPinMode"]
            .values_by_number[rep_data.gpio_get_pin_mode_response.mode]
            .name
        )

    # SetPinMode
    def rpc_gpio_set_pin_mode(self, pin, mode) -> None:
        """set GPIO pin mode

        Parameters
        ----------
        pin : int or str
            0 = 'PC0'
            1 = 'PC1'
            2 = 'PC3'
            3 = 'PB2'
            4 = 'PB3'
            5 = 'PA4'
            6 = 'PA6'
            7 = 'PA7'

        mode : str
            0 = 'OUTPUT'
            1 = 'INPUT'

        Returns:
        ----------
        None

        Raises
        ----------
        InputTypeException
        FlipperProtoException

        """

        cmd_data = gpio_pb2.SetPinMode()

        if isinstance(pin, int):
            cmd_data.pin = pin
        else:
            if pin not in ["PC0", "PC1", "PC3", "PB2", "PB3", "PA4", "PA6", "PA7"]:
                raise InputTypeException("Invalid pin")
            cmd_data.pin = getattr(gpio_pb2, pin)

        if mode not in ["OUTPUT", "INPUT"]:
            raise InputTypeException("Invalid mode")
        cmd_data.mode = getattr(gpio_pb2, mode)

        rep_data = self._rpc_send_and_read_answer(cmd_data, "gpio_set_pin_mode")

        if rep_data.command_status != 0:
            raise FlipperProtoException(
                f"{self.Status_values_by_number[rep_data.command_status].name} pin={pin} mode={mode}"
            )

    # WritePin
    def rpc_gpio_write_pin(self, pin, value) -> None:
        """write GPIO pin

        Parameters
        ----------
        pin : int or str
            0 = 'PC0'
            1 = 'PC1'
            2 = 'PC3'
            3 = 'PB2'
            4 = 'PB3'
            5 = 'PA4'
            6 = 'PA6'
            7 = 'PA7'

        value : int

        Returns:
        ----------
        None

        Raises
        ----------
        InputTypeException
        FlipperProtoException

        """

        cmd_data = gpio_pb2.WritePin()

        if isinstance(pin, int):
            cmd_data.pin = pin
        else:
            if pin not in ["PC0", "PC1", "PC3", "PB2", "PB3", "PA4", "PA6", "PA7"]:
                raise InputTypeException("Invalid pin")
            cmd_data.pin = getattr(gpio_pb2, pin)

        cmd_data.value = value

        rep_data = self._rpc_send_and_read_answer(cmd_data, "gpio_write_pin")

        if rep_data.command_status != 0:
            raise FlipperProtoException(
                f"{self.Status_values_by_number[rep_data.command_status].name} pin={pin} value={value}"
            )

    # ReadPin
    def rpc_gpio_read_pin(self, pin) -> int:
        """query GPIO pin

        Parameters
        ----------
        pin : int or str
            0 = 'PC0'
            1 = 'PC1'
            2 = 'PC3'
            3 = 'PB2'
            4 = 'PB3'
            5 = 'PA4'
            6 = 'PA6'
            7 = 'PA7'

        Returns:
        ----------
        int
            pin value

        Raises
        ----------
        InputTypeException
        FlipperProtoException

        """

        cmd_data = gpio_pb2.ReadPin()

        if isinstance(pin, int):
            cmd_data.pin = pin
        else:
            if pin not in ["PC0", "PC1", "PC3", "PB2", "PB3", "PA4", "PA6", "PA7"]:
                raise InputTypeException("Invalid pin")
            cmd_data.pin = getattr(gpio_pb2, pin)

        rep_data = self._rpc_send_and_read_answer(cmd_data, "gpio_read_pin")

        if rep_data.command_status != 0:
            raise FlipperProtoException(
                f"{self.Status_values_by_number[rep_data.command_status].name} pin={pin}"
            )

        return rep_data.read_pin_response.value

    # SetInputPull
    def rpc_gpio_set_input_pull(self, pin, pull_mode) -> None:
        """Set GPIO pill Input

        Parameters
        ----------
        pin : int or str
            0 = 'PC0'
            1 = 'PC1'
            2 = 'PC3'
            3 = 'PB2'
            4 = 'PB3'
            5 = 'PA4'
            6 = 'PA6'
            7 = 'PA7'

        pull_mode : str
            0 = 'NO'
            1 = 'UP'
            2 = 'DOWN'

        Returns:
        ----------
        None

        Raises
        ----------
        InputTypeException
        FlipperProtoException

        """

        cmd_data = gpio_pb2.SetInputPull()
        if isinstance(pin, int):
            cmd_data.pin = pin
        else:
            if pin not in ["PC0", "PC1", "PC3", "PB2", "PB3", "PA4", "PA6", "PA7"]:
                raise InputTypeException("Invalid pin")
            cmd_data.pin = getattr(gpio_pb2, pin)

        if pull_mode not in ["NO", "UP", "DOWN"]:
            raise InputTypeException("Invalid pull_mode")
        cmd_data.pull_mode = getattr(gpio_pb2, pull_mode)

        rep_data = self._rpc_send_and_read_answer(cmd_data, "gpio_set_input_pull")

        if rep_data.command_status != 0:
            raise FlipperProtoException(
                f"{self.Status_values_by_number[rep_data.command_status].name} pin={pin} pull_mode={pull_mode}"
            )
