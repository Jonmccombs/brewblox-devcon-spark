# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: SensorSetPointPair.proto

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
  name='SensorSetPointPair.proto',
  package='blox',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x18SensorSetPointPair.proto\x12\x04\x62lox\x1a\x0e\x62rewblox.proto\"R\n\x12SensorSetPointPair\x12\x1b\n\x06sensor\x18\x01 \x01(\rB\x0b\x9a?\x08\x1a\x06Sensor\x12\x1f\n\x08setpoint\x18\x02 \x01(\rB\r\x9a?\n\x1a\x08SetPointb\x06proto3')
  ,
  dependencies=[brewblox__pb2.DESCRIPTOR,])




_SENSORSETPOINTPAIR = _descriptor.Descriptor(
  name='SensorSetPointPair',
  full_name='blox.SensorSetPointPair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sensor', full_name='blox.SensorSetPointPair.sensor', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\232?\010\032\006Sensor'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='setpoint', full_name='blox.SensorSetPointPair.setpoint', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\232?\n\032\010SetPoint'), file=DESCRIPTOR),
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
  serialized_start=50,
  serialized_end=132,
)

DESCRIPTOR.message_types_by_name['SensorSetPointPair'] = _SENSORSETPOINTPAIR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SensorSetPointPair = _reflection.GeneratedProtocolMessageType('SensorSetPointPair', (_message.Message,), dict(
  DESCRIPTOR = _SENSORSETPOINTPAIR,
  __module__ = 'SensorSetPointPair_pb2'
  # @@protoc_insertion_point(class_scope:blox.SensorSetPointPair)
  ))
_sym_db.RegisterMessage(SensorSetPointPair)


_SENSORSETPOINTPAIR.fields_by_name['sensor']._options = None
_SENSORSETPOINTPAIR.fields_by_name['setpoint']._options = None
# @@protoc_insertion_point(module_scope)
