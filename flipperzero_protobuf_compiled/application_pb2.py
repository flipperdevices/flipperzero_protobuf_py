"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11application.proto\x12\x06PB_App"*\n\x0cStartRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04args\x18\x02 \x01(\t"\x13\n\x11LockStatusRequest"$\n\x12LockStatusResponse\x12\x0e\n\x06locked\x18\x01 \x01(\x08"\x10\n\x0eAppExitRequest""\n\x12AppLoadFileRequest\x12\x0c\n\x04path\x18\x01 \x01(\t"%\n\x15AppButtonPressRequest\x12\x0c\n\x04args\x18\x01 \x01(\t"\x19\n\x17AppButtonReleaseRequestB!\n\x1fcom.flipperdevices.protobuf.appb\x06proto3')
_STARTREQUEST = DESCRIPTOR.message_types_by_name['StartRequest']
_LOCKSTATUSREQUEST = DESCRIPTOR.message_types_by_name['LockStatusRequest']
_LOCKSTATUSRESPONSE = DESCRIPTOR.message_types_by_name['LockStatusResponse']
_APPEXITREQUEST = DESCRIPTOR.message_types_by_name['AppExitRequest']
_APPLOADFILEREQUEST = DESCRIPTOR.message_types_by_name['AppLoadFileRequest']
_APPBUTTONPRESSREQUEST = DESCRIPTOR.message_types_by_name['AppButtonPressRequest']
_APPBUTTONRELEASEREQUEST = DESCRIPTOR.message_types_by_name['AppButtonReleaseRequest']
StartRequest = _reflection.GeneratedProtocolMessageType('StartRequest', (_message.Message,), {'DESCRIPTOR': _STARTREQUEST, '__module__': 'application_pb2'})
_sym_db.RegisterMessage(StartRequest)
LockStatusRequest = _reflection.GeneratedProtocolMessageType('LockStatusRequest', (_message.Message,), {'DESCRIPTOR': _LOCKSTATUSREQUEST, '__module__': 'application_pb2'})
_sym_db.RegisterMessage(LockStatusRequest)
LockStatusResponse = _reflection.GeneratedProtocolMessageType('LockStatusResponse', (_message.Message,), {'DESCRIPTOR': _LOCKSTATUSRESPONSE, '__module__': 'application_pb2'})
_sym_db.RegisterMessage(LockStatusResponse)
AppExitRequest = _reflection.GeneratedProtocolMessageType('AppExitRequest', (_message.Message,), {'DESCRIPTOR': _APPEXITREQUEST, '__module__': 'application_pb2'})
_sym_db.RegisterMessage(AppExitRequest)
AppLoadFileRequest = _reflection.GeneratedProtocolMessageType('AppLoadFileRequest', (_message.Message,), {'DESCRIPTOR': _APPLOADFILEREQUEST, '__module__': 'application_pb2'})
_sym_db.RegisterMessage(AppLoadFileRequest)
AppButtonPressRequest = _reflection.GeneratedProtocolMessageType('AppButtonPressRequest', (_message.Message,), {'DESCRIPTOR': _APPBUTTONPRESSREQUEST, '__module__': 'application_pb2'})
_sym_db.RegisterMessage(AppButtonPressRequest)
AppButtonReleaseRequest = _reflection.GeneratedProtocolMessageType('AppButtonReleaseRequest', (_message.Message,), {'DESCRIPTOR': _APPBUTTONRELEASEREQUEST, '__module__': 'application_pb2'})
_sym_db.RegisterMessage(AppButtonReleaseRequest)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x1fcom.flipperdevices.protobuf.app'
    _STARTREQUEST._serialized_start = 29
    _STARTREQUEST._serialized_end = 71
    _LOCKSTATUSREQUEST._serialized_start = 73
    _LOCKSTATUSREQUEST._serialized_end = 92
    _LOCKSTATUSRESPONSE._serialized_start = 94
    _LOCKSTATUSRESPONSE._serialized_end = 130
    _APPEXITREQUEST._serialized_start = 132
    _APPEXITREQUEST._serialized_end = 148
    _APPLOADFILEREQUEST._serialized_start = 150
    _APPLOADFILEREQUEST._serialized_end = 184
    _APPBUTTONPRESSREQUEST._serialized_start = 186
    _APPBUTTONPRESSREQUEST._serialized_end = 223
    _APPBUTTONRELEASEREQUEST._serialized_start = 225
    _APPBUTTONRELEASEREQUEST._serialized_end = 250