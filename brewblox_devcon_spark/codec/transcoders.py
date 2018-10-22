"""
Object-specific transcoders
"""

from brewblox_devcon_spark.codec import _path_extension  # isort:skip

from abc import ABC, abstractclassmethod, abstractmethod
from typing import Iterable, Union

from brewblox_service import brewblox_logger
from google.protobuf import json_format
from google.protobuf.message import Message

import ActuatorAnalogMock_pb2
import ActuatorOffset_pb2
import ActuatorPin_pb2
import ActuatorPwm_pb2
import Balancer_pb2
import brewblox_pb2
import EdgeCase_pb2
import Mutex_pb2
import nanopb_pb2
import OneWireBus_pb2
import Pid_pb2
import SetpointProfile_pb2
import SetpointSensorPair_pb2
import SetpointSimple_pb2
import SysInfo_pb2
import TempSensorMock_pb2
import TempSensorOneWire_pb2
import Ticks_pb2
import XboxController_pb2
from brewblox_devcon_spark.codec.modifiers import Modifier

ObjType_ = Union[int, str]
Decoded_ = dict
Encoded_ = bytes

_path_extension.avoid_lint_errors()
LOGGER = brewblox_logger(__name__)


class Transcoder(ABC):

    def __init__(self, mods: Modifier):
        self.mod = mods

    @abstractclassmethod
    def type_int(cls) -> int:
        pass  # pragma: no cover

    @abstractclassmethod
    def type_str(cls) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def encode(self, values: Decoded_) -> Encoded_:
        pass  # pragma: no cover

    @abstractmethod
    def decode(encoded: Encoded_) -> Decoded_:
        pass  # pragma: no cover

    @classmethod
    def get(cls, obj_type: ObjType_, mods: Modifier) -> 'Transcoder':
        try:
            return _TYPE_MAPPING[obj_type](mods)
        except KeyError:
            raise KeyError(f'No codec found for object type [{obj_type}]')


class LinkTypeTranscoder(Transcoder):

    @classmethod
    def type_int(cls) -> int:
        return cls._ENUM_VAL

    @classmethod
    def type_str(cls) -> str:
        return brewblox_pb2.BrewbloxFieldOptions.LinkType.Name(cls._ENUM_VAL)

    def encode(self, values: Decoded_) -> Encoded_:
        return b'\x00'

    def decode(self, values: Encoded_) -> Decoded_:
        return dict()


def link_type_factory(value: int) -> LinkTypeTranscoder:
    name = f'{brewblox_pb2.BrewbloxFieldOptions.LinkType.Name(value)}Transcoder'
    return type(name, (LinkTypeTranscoder, ), {'_ENUM_VAL': value})


class InactiveObjectTranscoder(Transcoder):

    @classmethod
    def type_int(cls) -> int:
        return 65535

    @classmethod
    def type_str(cls) -> str:
        return 'InactiveObject'

    def encode(self, values: Decoded_) -> Encoded_:
        type_id = values['actualType']
        encoded = Transcoder.get(type_id, self.mod).type_int().to_bytes(2, 'little')
        return encoded

    def decode(self, encoded: Encoded_) -> Decoded_:
        type_id = int.from_bytes(encoded, 'little')
        return {'actualType': Transcoder.get(type_id, self.mod).type_str()}


class ProfilesTranscoder(Transcoder):

    @classmethod
    def type_int(cls) -> int:
        return 65534

    @classmethod
    def type_str(cls) -> str:
        return 'Profiles'

    def encode(self, values: Decoded_) -> Encoded_:
        active = self.mod.pack_bit_flags(values.get('active', []))
        return active.to_bytes(1, 'little')

    def decode(self, encoded: Encoded_) -> Decoded_:
        active = self.mod.unpack_bit_flags(int.from_bytes(encoded, 'little'))
        return {'active': active}


class ProtobufTranscoder(Transcoder):

    @classmethod
    def type_int(cls) -> int:
        return cls._MESSAGE.DESCRIPTOR.GetOptions().Extensions[nanopb_pb2.nanopb_msgopt].msgid

    @classmethod
    def type_str(cls) -> str:
        return cls._MESSAGE.__name__

    def create_message(self) -> Message:
        return self.__class__._MESSAGE()

    def encode(self, values: Decoded_) -> Encoded_:
        LOGGER.debug(f'encoding {values} to {self.__class__._MESSAGE}')
        obj = json_format.ParseDict(values, self.create_message())
        data = obj.SerializeToString()
        return data + b'\x00'  # Include null terminator

    def decode(self, encoded: Encoded_) -> Decoded_:
        # Remove null terminator
        encoded = encoded[:-1]

        obj = self.create_message()
        obj.ParseFromString(encoded)
        decoded = json_format.MessageToDict(
            message=obj,
            preserving_proto_field_name=True,
            including_default_value_fields=True,
            use_integers_for_enums=True,
        )
        LOGGER.debug(f'decoded {self.__class__._MESSAGE} to {decoded}')
        return decoded


class OptionsTranscoder(ProtobufTranscoder):

    def encode(self, values: Decoded_) -> Encoded_:
        self.mod.encode_options(self.create_message(), values)
        return super().encode(values)

    def decode(self, encoded: Encoded_) -> Decoded_:
        decoded = super().decode(encoded)
        self.mod.decode_options(self.create_message(), decoded)
        return decoded


def options_type_factory(message):
    name = f'{message.__name__}Transcoder'
    return type(name, (OptionsTranscoder, ), {'_MESSAGE': message})


def _generate_mapping(vals: Iterable[Transcoder]):
    for trc in vals:
        yield trc.type_int(), trc
        yield trc.type_str(), trc


_TRANSCODERS = [
    # Raw system objects
    *[link_type_factory(v) for v in brewblox_pb2.BrewbloxFieldOptions.LinkType.values()],
    InactiveObjectTranscoder,
    ProfilesTranscoder,

    # Debugging objects
    *[options_type_factory(msg) for msg in [
        EdgeCase_pb2.EdgeCase,
        XboxController_pb2.XboxController,
    ]],

    # Protobuf objects
    *[options_type_factory(msg) for msg in [
        ActuatorAnalogMock_pb2.ActuatorAnalogMock,
        ActuatorOffset_pb2.ActuatorOffset,
        ActuatorPin_pb2.ActuatorPin,
        ActuatorPwm_pb2.ActuatorPwm,
        Balancer_pb2.Balancer,
        Mutex_pb2.Mutex,
        OneWireBus_pb2.OneWireBus,
        Pid_pb2.Pid,
        SetpointProfile_pb2.SetpointProfile,
        SetpointSensorPair_pb2.SetpointSensorPair,
        SetpointSimple_pb2.SetpointSimple,
        SysInfo_pb2.SysInfo,
        TempSensorMock_pb2.TempSensorMock,
        TempSensorOneWire_pb2.TempSensorOneWire,
        Ticks_pb2.Ticks,
    ]],
]

_TYPE_MAPPING = {k: v for k, v in _generate_mapping(_TRANSCODERS)}