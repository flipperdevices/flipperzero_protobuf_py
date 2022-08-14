"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tgui.proto\x12\x06PB_Gui"\x1b\n\x0bScreenFrame\x12\x0c\n\x04data\x18\x01 \x01(\x0c"\x1a\n\x18StartScreenStreamRequest"\x19\n\x17StopScreenStreamRequest"W\n\x15SendInputEventRequest\x12\x1d\n\x03key\x18\x01 \x01(\x0e2\x10.PB_Gui.InputKey\x12\x1f\n\x04type\x18\x02 \x01(\x0e2\x11.PB_Gui.InputType"F\n\x1aStartVirtualDisplayRequest\x12(\n\x0bfirst_frame\x18\x01 \x01(\x0b2\x13.PB_Gui.ScreenFrame"\x1b\n\x19StopVirtualDisplayRequest*C\n\x08InputKey\x12\x06\n\x02UP\x10\x00\x12\x08\n\x04DOWN\x10\x01\x12\t\n\x05RIGHT\x10\x02\x12\x08\n\x04LEFT\x10\x03\x12\x06\n\x02OK\x10\x04\x12\x08\n\x04BACK\x10\x05*D\n\tInputType\x12\t\n\x05PRESS\x10\x00\x12\x0b\n\x07RELEASE\x10\x01\x12\t\n\x05SHORT\x10\x02\x12\x08\n\x04LONG\x10\x03\x12\n\n\x06REPEAT\x10\x04B$\n"com.flipperdevices.protobuf.screenb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gui_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n"com.flipperdevices.protobuf.screen'
    _INPUTKEY._serialized_start = 295
    _INPUTKEY._serialized_end = 362
    _INPUTTYPE._serialized_start = 364
    _INPUTTYPE._serialized_end = 432
    _SCREENFRAME._serialized_start = 21
    _SCREENFRAME._serialized_end = 48
    _STARTSCREENSTREAMREQUEST._serialized_start = 50
    _STARTSCREENSTREAMREQUEST._serialized_end = 76
    _STOPSCREENSTREAMREQUEST._serialized_start = 78
    _STOPSCREENSTREAMREQUEST._serialized_end = 103
    _SENDINPUTEVENTREQUEST._serialized_start = 105
    _SENDINPUTEVENTREQUEST._serialized_end = 192
    _STARTVIRTUALDISPLAYREQUEST._serialized_start = 194
    _STARTVIRTUALDISPLAYREQUEST._serialized_end = 264
    _STOPVIRTUALDISPLAYREQUEST._serialized_start = 266
    _STOPVIRTUALDISPLAYREQUEST._serialized_end = 293