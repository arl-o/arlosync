# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: arlosync.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='arlosync.proto',
  package='arlosync',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0e\x61rlosync.proto\x12\x08\x61rlosync\"b\n\x13\x44irectoryDescriptor\x12\x32\n\x10\x66ile_descriptors\x18\x01 \x03(\x0b\x32\x18.arlosync.FileDescriptor\x12\x17\n\x0fsub_directories\x18\x02 \x03(\t\"?\n\x0e\x46ileDescriptor\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x10\n\x08\x66ilesize\x18\x02 \x01(\x03\x12\r\n\x05mtime\x18\x03 \x01(\x01\"Y\n\rFileAndTokens\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x11\n\tchecksums\x18\x02 \x03(\r\x12\x13\n\x0bhash_tokens\x18\x03 \x03(\x0c\x12\x12\n\nchunk_size\x18\x04 \x01(\x03\"o\n\x0e\x42ytesAndTokens\x12\x17\n\rliteral_bytes\x18\x01 \x01(\x0cH\x00\x12+\n\x0bhash_tokens\x18\x02 \x01(\x0b\x32\x14.arlosync.HashTokensH\x00\x42\x17\n\x15\x62ytes_or_tokens_oneof\"\x1c\n\nHashTokens\x12\x0e\n\x06tokens\x18\x01 \x03(\x0c\x32\xc1\x01\n\nSyncClient\x12Q\n\x18GetBytesAndTokensForFile\x12\x17.arlosync.FileAndTokens\x1a\x18.arlosync.BytesAndTokens\"\x00\x30\x01\x12`\n\'GetBytesAndTokensForDirectoryDescriptor\x12\x17.arlosync.FileAndTokens\x1a\x18.arlosync.BytesAndTokens\"\x00\x30\x01\x62\x06proto3'
)




_DIRECTORYDESCRIPTOR = _descriptor.Descriptor(
  name='DirectoryDescriptor',
  full_name='arlosync.DirectoryDescriptor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_descriptors', full_name='arlosync.DirectoryDescriptor.file_descriptors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sub_directories', full_name='arlosync.DirectoryDescriptor.sub_directories', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=126,
)


_FILEDESCRIPTOR = _descriptor.Descriptor(
  name='FileDescriptor',
  full_name='arlosync.FileDescriptor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='arlosync.FileDescriptor.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filesize', full_name='arlosync.FileDescriptor.filesize', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mtime', full_name='arlosync.FileDescriptor.mtime', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=128,
  serialized_end=191,
)


_FILEANDTOKENS = _descriptor.Descriptor(
  name='FileAndTokens',
  full_name='arlosync.FileAndTokens',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='arlosync.FileAndTokens.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='checksums', full_name='arlosync.FileAndTokens.checksums', index=1,
      number=2, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hash_tokens', full_name='arlosync.FileAndTokens.hash_tokens', index=2,
      number=3, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='chunk_size', full_name='arlosync.FileAndTokens.chunk_size', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=193,
  serialized_end=282,
)


_BYTESANDTOKENS = _descriptor.Descriptor(
  name='BytesAndTokens',
  full_name='arlosync.BytesAndTokens',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='literal_bytes', full_name='arlosync.BytesAndTokens.literal_bytes', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hash_tokens', full_name='arlosync.BytesAndTokens.hash_tokens', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='bytes_or_tokens_oneof', full_name='arlosync.BytesAndTokens.bytes_or_tokens_oneof',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=284,
  serialized_end=395,
)


_HASHTOKENS = _descriptor.Descriptor(
  name='HashTokens',
  full_name='arlosync.HashTokens',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tokens', full_name='arlosync.HashTokens.tokens', index=0,
      number=1, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=397,
  serialized_end=425,
)

_DIRECTORYDESCRIPTOR.fields_by_name['file_descriptors'].message_type = _FILEDESCRIPTOR
_BYTESANDTOKENS.fields_by_name['hash_tokens'].message_type = _HASHTOKENS
_BYTESANDTOKENS.oneofs_by_name['bytes_or_tokens_oneof'].fields.append(
  _BYTESANDTOKENS.fields_by_name['literal_bytes'])
_BYTESANDTOKENS.fields_by_name['literal_bytes'].containing_oneof = _BYTESANDTOKENS.oneofs_by_name['bytes_or_tokens_oneof']
_BYTESANDTOKENS.oneofs_by_name['bytes_or_tokens_oneof'].fields.append(
  _BYTESANDTOKENS.fields_by_name['hash_tokens'])
_BYTESANDTOKENS.fields_by_name['hash_tokens'].containing_oneof = _BYTESANDTOKENS.oneofs_by_name['bytes_or_tokens_oneof']
DESCRIPTOR.message_types_by_name['DirectoryDescriptor'] = _DIRECTORYDESCRIPTOR
DESCRIPTOR.message_types_by_name['FileDescriptor'] = _FILEDESCRIPTOR
DESCRIPTOR.message_types_by_name['FileAndTokens'] = _FILEANDTOKENS
DESCRIPTOR.message_types_by_name['BytesAndTokens'] = _BYTESANDTOKENS
DESCRIPTOR.message_types_by_name['HashTokens'] = _HASHTOKENS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DirectoryDescriptor = _reflection.GeneratedProtocolMessageType('DirectoryDescriptor', (_message.Message,), {
  'DESCRIPTOR' : _DIRECTORYDESCRIPTOR,
  '__module__' : 'arlosync_pb2'
  # @@protoc_insertion_point(class_scope:arlosync.DirectoryDescriptor)
  })
_sym_db.RegisterMessage(DirectoryDescriptor)

FileDescriptor = _reflection.GeneratedProtocolMessageType('FileDescriptor', (_message.Message,), {
  'DESCRIPTOR' : _FILEDESCRIPTOR,
  '__module__' : 'arlosync_pb2'
  # @@protoc_insertion_point(class_scope:arlosync.FileDescriptor)
  })
_sym_db.RegisterMessage(FileDescriptor)

FileAndTokens = _reflection.GeneratedProtocolMessageType('FileAndTokens', (_message.Message,), {
  'DESCRIPTOR' : _FILEANDTOKENS,
  '__module__' : 'arlosync_pb2'
  # @@protoc_insertion_point(class_scope:arlosync.FileAndTokens)
  })
_sym_db.RegisterMessage(FileAndTokens)

BytesAndTokens = _reflection.GeneratedProtocolMessageType('BytesAndTokens', (_message.Message,), {
  'DESCRIPTOR' : _BYTESANDTOKENS,
  '__module__' : 'arlosync_pb2'
  # @@protoc_insertion_point(class_scope:arlosync.BytesAndTokens)
  })
_sym_db.RegisterMessage(BytesAndTokens)

HashTokens = _reflection.GeneratedProtocolMessageType('HashTokens', (_message.Message,), {
  'DESCRIPTOR' : _HASHTOKENS,
  '__module__' : 'arlosync_pb2'
  # @@protoc_insertion_point(class_scope:arlosync.HashTokens)
  })
_sym_db.RegisterMessage(HashTokens)



_SYNCCLIENT = _descriptor.ServiceDescriptor(
  name='SyncClient',
  full_name='arlosync.SyncClient',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=428,
  serialized_end=621,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetBytesAndTokensForFile',
    full_name='arlosync.SyncClient.GetBytesAndTokensForFile',
    index=0,
    containing_service=None,
    input_type=_FILEANDTOKENS,
    output_type=_BYTESANDTOKENS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetBytesAndTokensForDirectoryDescriptor',
    full_name='arlosync.SyncClient.GetBytesAndTokensForDirectoryDescriptor',
    index=1,
    containing_service=None,
    input_type=_FILEANDTOKENS,
    output_type=_BYTESANDTOKENS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SYNCCLIENT)

DESCRIPTOR.services_by_name['SyncClient'] = _SYNCCLIENT

# @@protoc_insertion_point(module_scope)
