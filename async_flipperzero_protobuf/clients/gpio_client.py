from flipperzero_protobuf_compiled import gpio_pb2
from commands.gpio_commands import (
    GPIOSetInputPullCommand,
    GPIOSetPinModeCommand,
    GPIOGetPinModeCommand,
    GPIOWritePinCommand,
    GPIOReadPinCommand,
)
from clients.base_client import FlipperBaseProtoClient


class FlipperGPIOProtoClient(FlipperBaseProtoClient):
    async def gpio_get_pin_mode(self, pin: str | int, wait_for_response: bool = True):
        response = await self.request(
            GPIOGetPinModeCommand(pin=pin), wait_for_response=wait_for_response, to_validate=True
        )
        return (
            gpio_pb2.DESCRIPTOR.enum_types_by_name["GpioPinMode"]
            .values_by_number[response.gpio_get_pin_mode_response.mode]
            .name
        )

    async def gpio_set_pin_mode(self, pin: str | int, mode: str, wait_for_response: bool = True):
        return await self.request(
            GPIOSetPinModeCommand(pin=pin, mode=mode), wait_for_response=wait_for_response, to_validate=True
        )

    async def gpio_write_pin(self, pin: str | int, value: int, wait_for_response: bool = True):
        return await self.request(
            GPIOWritePinCommand(pin=pin, value=value), wait_for_response=wait_for_response, to_validate=True
        )

    async def gpio_read_pin(self, pin: str | int, wait_for_response: bool = True):
        response = await self.request(
            GPIOReadPinCommand(pin=pin), wait_for_response=wait_for_response, to_validate=True
        )
        return response.read_pin_response.value

    async def gpio_set_input_pull(self, pin: str | int, pull_mode: str, wait_for_response: bool = True):
        return await self.request(
            GPIOSetInputPullCommand(pin=pin, pull_mode=pull_mode), wait_for_response=wait_for_response, to_validate=True
        )
