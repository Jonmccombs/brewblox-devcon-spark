# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Ticks.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import brewblox_pb2 as brewblox__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='Ticks.proto',
  package='blox',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0bTicks.proto\x12\x04\x62lox\x1a\x0e\x62rewblox.proto\"B\n\x05Ticks\x12\x1e\n\x0fmillisSinceBoot\x18\x01 \x01(\rB\x05\x9a?\x02(\x01\x12\x19\n\x11secondsSinceEpoch\x18\x02 \x01(\rb\x06proto3')
  ,
  dependencies=[brewblox__pb2.DESCRIPTOR,])




_TICKS = _descriptor.Descriptor(
  name='Ticks',
  full_name='blox.Ticks',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='millisSinceBoot', full_name='blox.Ticks.millisSinceBoot', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\232?\002(\001'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='secondsSinceEpoch', full_name='blox.Ticks.secondsSinceEpoch', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=37,
  serialized_end=103,
)

DESCRIPTOR.message_types_by_name['Ticks'] = _TICKS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Ticks = _reflection.GeneratedProtocolMessageType('Ticks', (_message.Message,), dict(
  DESCRIPTOR = _TICKS,
  __module__ = 'Ticks_pb2'
  # @@protoc_insertion_point(class_scope:blox.Ticks)
  ))
_sym_db.RegisterMessage(Ticks)


_TICKS.fields_by_name['millisSinceBoot']._options = None
# @@protoc_insertion_point(module_scope)
