"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ngpio.proto\x12\x07PB_Gpio"O\n\nSetPinMode\x12\x1d\n\x03pin\x18\x01 \x01(\x0e2\x10.PB_Gpio.GpioPin\x12"\n\x04mode\x18\x02 \x01(\x0e2\x14.PB_Gpio.GpioPinMode"X\n\x0cSetInputPull\x12\x1d\n\x03pin\x18\x01 \x01(\x0e2\x10.PB_Gpio.GpioPin\x12)\n\tpull_mode\x18\x02 \x01(\x0e2\x16.PB_Gpio.GpioInputPull"+\n\nGetPinMode\x12\x1d\n\x03pin\x18\x01 \x01(\x0e2\x10.PB_Gpio.GpioPin"8\n\x12GetPinModeResponse\x12"\n\x04mode\x18\x01 \x01(\x0e2\x14.PB_Gpio.GpioPinMode"(\n\x07ReadPin\x12\x1d\n\x03pin\x18\x01 \x01(\x0e2\x10.PB_Gpio.GpioPin" \n\x0fReadPinResponse\x12\r\n\x05value\x18\x02 \x01(\r"8\n\x08WritePin\x12\x1d\n\x03pin\x18\x01 \x01(\x0e2\x10.PB_Gpio.GpioPin\x12\r\n\x05value\x18\x02 \x01(\r*Q\n\x07GpioPin\x12\x07\n\x03PC0\x10\x00\x12\x07\n\x03PC1\x10\x01\x12\x07\n\x03PC3\x10\x02\x12\x07\n\x03PB2\x10\x03\x12\x07\n\x03PB3\x10\x04\x12\x07\n\x03PA4\x10\x05\x12\x07\n\x03PA6\x10\x06\x12\x07\n\x03PA7\x10\x07*$\n\x0bGpioPinMode\x12\n\n\x06OUTPUT\x10\x00\x12\t\n\x05INPUT\x10\x01*)\n\rGpioInputPull\x12\x06\n\x02NO\x10\x00\x12\x06\n\x02UP\x10\x01\x12\x08\n\x04DOWN\x10\x02B"\n com.flipperdevices.protobuf.gpiob\x06proto3')
_GPIOPIN = DESCRIPTOR.enum_types_by_name['GpioPin']
GpioPin = enum_type_wrapper.EnumTypeWrapper(_GPIOPIN)
_GPIOPINMODE = DESCRIPTOR.enum_types_by_name['GpioPinMode']
GpioPinMode = enum_type_wrapper.EnumTypeWrapper(_GPIOPINMODE)
_GPIOINPUTPULL = DESCRIPTOR.enum_types_by_name['GpioInputPull']
GpioInputPull = enum_type_wrapper.EnumTypeWrapper(_GPIOINPUTPULL)
PC0 = 0
PC1 = 1
PC3 = 2
PB2 = 3
PB3 = 4
PA4 = 5
PA6 = 6
PA7 = 7
OUTPUT = 0
INPUT = 1
NO = 0
UP = 1
DOWN = 2
_SETPINMODE = DESCRIPTOR.message_types_by_name['SetPinMode']
_SETINPUTPULL = DESCRIPTOR.message_types_by_name['SetInputPull']
_GETPINMODE = DESCRIPTOR.message_types_by_name['GetPinMode']
_GETPINMODERESPONSE = DESCRIPTOR.message_types_by_name['GetPinModeResponse']
_READPIN = DESCRIPTOR.message_types_by_name['ReadPin']
_READPINRESPONSE = DESCRIPTOR.message_types_by_name['ReadPinResponse']
_WRITEPIN = DESCRIPTOR.message_types_by_name['WritePin']
SetPinMode = _reflection.GeneratedProtocolMessageType('SetPinMode', (_message.Message,), {'DESCRIPTOR': _SETPINMODE, '__module__': 'gpio_pb2'})
_sym_db.RegisterMessage(SetPinMode)
SetInputPull = _reflection.GeneratedProtocolMessageType('SetInputPull', (_message.Message,), {'DESCRIPTOR': _SETINPUTPULL, '__module__': 'gpio_pb2'})
_sym_db.RegisterMessage(SetInputPull)
GetPinMode = _reflection.GeneratedProtocolMessageType('GetPinMode', (_message.Message,), {'DESCRIPTOR': _GETPINMODE, '__module__': 'gpio_pb2'})
_sym_db.RegisterMessage(GetPinMode)
GetPinModeResponse = _reflection.GeneratedProtocolMessageType('GetPinModeResponse', (_message.Message,), {'DESCRIPTOR': _GETPINMODERESPONSE, '__module__': 'gpio_pb2'})
_sym_db.RegisterMessage(GetPinModeResponse)
ReadPin = _reflection.GeneratedProtocolMessageType('ReadPin', (_message.Message,), {'DESCRIPTOR': _READPIN, '__module__': 'gpio_pb2'})
_sym_db.RegisterMessage(ReadPin)
ReadPinResponse = _reflection.GeneratedProtocolMessageType('ReadPinResponse', (_message.Message,), {'DESCRIPTOR': _READPINRESPONSE, '__module__': 'gpio_pb2'})
_sym_db.RegisterMessage(ReadPinResponse)
WritePin = _reflection.GeneratedProtocolMessageType('WritePin', (_message.Message,), {'DESCRIPTOR': _WRITEPIN, '__module__': 'gpio_pb2'})
_sym_db.RegisterMessage(WritePin)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n com.flipperdevices.protobuf.gpio'
    _GPIOPIN._serialized_start = 431
    _GPIOPIN._serialized_end = 512
    _GPIOPINMODE._serialized_start = 514
    _GPIOPINMODE._serialized_end = 550
    _GPIOINPUTPULL._serialized_start = 552
    _GPIOINPUTPULL._serialized_end = 593
    _SETPINMODE._serialized_start = 23
    _SETPINMODE._serialized_end = 102
    _SETINPUTPULL._serialized_start = 104
    _SETINPUTPULL._serialized_end = 192
    _GETPINMODE._serialized_start = 194
    _GETPINMODE._serialized_end = 237
    _GETPINMODERESPONSE._serialized_start = 239
    _GETPINMODERESPONSE._serialized_end = 295
    _READPIN._serialized_start = 297
    _READPIN._serialized_end = 337
    _READPINRESPONSE._serialized_start = 339
    _READPINRESPONSE._serialized_end = 371
    _WRITEPIN._serialized_start = 373
    _WRITEPIN._serialized_end = 429