"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rstorage.proto\x12\nPB_Storage"x\n\x04File\x12\'\n\x04type\x18\x01 \x01(\x0e2\x19.PB_Storage.File.FileType\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0c\n\x04size\x18\x03 \x01(\r\x12\x0c\n\x04data\x18\x04 \x01(\x0c"\x1d\n\x08FileType\x12\x08\n\x04FILE\x10\x00\x12\x07\n\x03DIR\x10\x01"\x1b\n\x0bInfoRequest\x12\x0c\n\x04path\x18\x01 \x01(\t"7\n\x0cInfoResponse\x12\x13\n\x0btotal_space\x18\x01 \x01(\x04\x12\x12\n\nfree_space\x18\x02 \x01(\x04"\x1b\n\x0bStatRequest\x12\x0c\n\x04path\x18\x01 \x01(\t".\n\x0cStatResponse\x12\x1e\n\x04file\x18\x01 \x01(\x0b2\x10.PB_Storage.File"\x1b\n\x0bListRequest\x12\x0c\n\x04path\x18\x01 \x01(\t".\n\x0cListResponse\x12\x1e\n\x04file\x18\x01 \x03(\x0b2\x10.PB_Storage.File"\x1b\n\x0bReadRequest\x12\x0c\n\x04path\x18\x01 \x01(\t".\n\x0cReadResponse\x12\x1e\n\x04file\x18\x01 \x01(\x0b2\x10.PB_Storage.File"<\n\x0cWriteRequest\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x1e\n\x04file\x18\x02 \x01(\x0b2\x10.PB_Storage.File"0\n\rDeleteRequest\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x11\n\trecursive\x18\x02 \x01(\x08"\x1c\n\x0cMkdirRequest\x12\x0c\n\x04path\x18\x01 \x01(\t"\x1d\n\rMd5sumRequest\x12\x0c\n\x04path\x18\x01 \x01(\t" \n\x0eMd5sumResponse\x12\x0e\n\x06md5sum\x18\x01 \x01(\t"3\n\rRenameRequest\x12\x10\n\x08old_path\x18\x01 \x01(\t\x12\x10\n\x08new_path\x18\x02 \x01(\t"+\n\x13BackupCreateRequest\x12\x14\n\x0carchive_path\x18\x01 \x01(\t",\n\x14BackupRestoreRequest\x12\x14\n\x0carchive_path\x18\x01 \x01(\tB%\n#com.flipperdevices.protobuf.storageb\x06proto3')
_FILE = DESCRIPTOR.message_types_by_name['File']
_INFOREQUEST = DESCRIPTOR.message_types_by_name['InfoRequest']
_INFORESPONSE = DESCRIPTOR.message_types_by_name['InfoResponse']
_STATREQUEST = DESCRIPTOR.message_types_by_name['StatRequest']
_STATRESPONSE = DESCRIPTOR.message_types_by_name['StatResponse']
_LISTREQUEST = DESCRIPTOR.message_types_by_name['ListRequest']
_LISTRESPONSE = DESCRIPTOR.message_types_by_name['ListResponse']
_READREQUEST = DESCRIPTOR.message_types_by_name['ReadRequest']
_READRESPONSE = DESCRIPTOR.message_types_by_name['ReadResponse']
_WRITEREQUEST = DESCRIPTOR.message_types_by_name['WriteRequest']
_DELETEREQUEST = DESCRIPTOR.message_types_by_name['DeleteRequest']
_MKDIRREQUEST = DESCRIPTOR.message_types_by_name['MkdirRequest']
_MD5SUMREQUEST = DESCRIPTOR.message_types_by_name['Md5sumRequest']
_MD5SUMRESPONSE = DESCRIPTOR.message_types_by_name['Md5sumResponse']
_RENAMEREQUEST = DESCRIPTOR.message_types_by_name['RenameRequest']
_BACKUPCREATEREQUEST = DESCRIPTOR.message_types_by_name['BackupCreateRequest']
_BACKUPRESTOREREQUEST = DESCRIPTOR.message_types_by_name['BackupRestoreRequest']
_FILE_FILETYPE = _FILE.enum_types_by_name['FileType']
File = _reflection.GeneratedProtocolMessageType('File', (_message.Message,), {'DESCRIPTOR': _FILE, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(File)
InfoRequest = _reflection.GeneratedProtocolMessageType('InfoRequest', (_message.Message,), {'DESCRIPTOR': _INFOREQUEST, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(InfoRequest)
InfoResponse = _reflection.GeneratedProtocolMessageType('InfoResponse', (_message.Message,), {'DESCRIPTOR': _INFORESPONSE, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(InfoResponse)
StatRequest = _reflection.GeneratedProtocolMessageType('StatRequest', (_message.Message,), {'DESCRIPTOR': _STATREQUEST, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(StatRequest)
StatResponse = _reflection.GeneratedProtocolMessageType('StatResponse', (_message.Message,), {'DESCRIPTOR': _STATRESPONSE, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(StatResponse)
ListRequest = _reflection.GeneratedProtocolMessageType('ListRequest', (_message.Message,), {'DESCRIPTOR': _LISTREQUEST, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(ListRequest)
ListResponse = _reflection.GeneratedProtocolMessageType('ListResponse', (_message.Message,), {'DESCRIPTOR': _LISTRESPONSE, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(ListResponse)
ReadRequest = _reflection.GeneratedProtocolMessageType('ReadRequest', (_message.Message,), {'DESCRIPTOR': _READREQUEST, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(ReadRequest)
ReadResponse = _reflection.GeneratedProtocolMessageType('ReadResponse', (_message.Message,), {'DESCRIPTOR': _READRESPONSE, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(ReadResponse)
WriteRequest = _reflection.GeneratedProtocolMessageType('WriteRequest', (_message.Message,), {'DESCRIPTOR': _WRITEREQUEST, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(WriteRequest)
DeleteRequest = _reflection.GeneratedProtocolMessageType('DeleteRequest', (_message.Message,), {'DESCRIPTOR': _DELETEREQUEST, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(DeleteRequest)
MkdirRequest = _reflection.GeneratedProtocolMessageType('MkdirRequest', (_message.Message,), {'DESCRIPTOR': _MKDIRREQUEST, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(MkdirRequest)
Md5sumRequest = _reflection.GeneratedProtocolMessageType('Md5sumRequest', (_message.Message,), {'DESCRIPTOR': _MD5SUMREQUEST, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(Md5sumRequest)
Md5sumResponse = _reflection.GeneratedProtocolMessageType('Md5sumResponse', (_message.Message,), {'DESCRIPTOR': _MD5SUMRESPONSE, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(Md5sumResponse)
RenameRequest = _reflection.GeneratedProtocolMessageType('RenameRequest', (_message.Message,), {'DESCRIPTOR': _RENAMEREQUEST, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(RenameRequest)
BackupCreateRequest = _reflection.GeneratedProtocolMessageType('BackupCreateRequest', (_message.Message,), {'DESCRIPTOR': _BACKUPCREATEREQUEST, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(BackupCreateRequest)
BackupRestoreRequest = _reflection.GeneratedProtocolMessageType('BackupRestoreRequest', (_message.Message,), {'DESCRIPTOR': _BACKUPRESTOREREQUEST, '__module__': 'storage_pb2'})
_sym_db.RegisterMessage(BackupRestoreRequest)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n#com.flipperdevices.protobuf.storage'
    _FILE._serialized_start = 29
    _FILE._serialized_end = 149
    _FILE_FILETYPE._serialized_start = 120
    _FILE_FILETYPE._serialized_end = 149
    _INFOREQUEST._serialized_start = 151
    _INFOREQUEST._serialized_end = 178
    _INFORESPONSE._serialized_start = 180
    _INFORESPONSE._serialized_end = 235
    _STATREQUEST._serialized_start = 237
    _STATREQUEST._serialized_end = 264
    _STATRESPONSE._serialized_start = 266
    _STATRESPONSE._serialized_end = 312
    _LISTREQUEST._serialized_start = 314
    _LISTREQUEST._serialized_end = 341
    _LISTRESPONSE._serialized_start = 343
    _LISTRESPONSE._serialized_end = 389
    _READREQUEST._serialized_start = 391
    _READREQUEST._serialized_end = 418
    _READRESPONSE._serialized_start = 420
    _READRESPONSE._serialized_end = 466
    _WRITEREQUEST._serialized_start = 468
    _WRITEREQUEST._serialized_end = 528
    _DELETEREQUEST._serialized_start = 530
    _DELETEREQUEST._serialized_end = 578
    _MKDIRREQUEST._serialized_start = 580
    _MKDIRREQUEST._serialized_end = 608
    _MD5SUMREQUEST._serialized_start = 610
    _MD5SUMREQUEST._serialized_end = 639
    _MD5SUMRESPONSE._serialized_start = 641
    _MD5SUMRESPONSE._serialized_end = 673
    _RENAMEREQUEST._serialized_start = 675
    _RENAMEREQUEST._serialized_end = 726
    _BACKUPCREATEREQUEST._serialized_start = 728
    _BACKUPCREATEREQUEST._serialized_end = 771
    _BACKUPRESTOREREQUEST._serialized_start = 773
    _BACKUPRESTOREREQUEST._serialized_end = 817