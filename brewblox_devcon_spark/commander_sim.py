"""
Monkey patches commander.SparkCommander to not require an actual connection.
"""

from itertools import count

from aiohttp import web
from brewblox_service import features

from brewblox_devcon_spark import commander, commands, exceptions, status
from brewblox_devcon_spark.commands import (OBJECT_DATA_KEY, OBJECT_ID_KEY,
                                            OBJECT_LIST_KEY, OBJECT_TYPE_KEY,
                                            PROFILE_LIST_KEY)

OBJECT_ID_START = 256


def setup(app: web.Application):
    # Register as a SparkCommander, so features.get(app, SparkCommander) still works
    features.add(app, SimulationCommander(app), key=commander.SparkCommander)


class SimulationResponder():

    def __init__(self):
        self._generators = {
            commands.ReadObjectCommand: self._read_object,
            commands.WriteObjectCommand: self._write_object,
            commands.CreateObjectCommand: self._create_object,
            commands.DeleteObjectCommand: self._delete_object,
            commands.ListActiveObjectsCommand: self._list_active_objects,
            commands.ListStoredObjectsCommand: self._list_stored_objects,
            commands.ClearObjectsCommand: self._clear_objects,
            commands.FactoryResetCommand: self._factory_reset,
            commands.RebootCommand: self._reboot,
        }

        self._id_counter = count(start=OBJECT_ID_START)
        self._active_profiles = [0]

        def all_profiles():
            return [i for i in range(8)]

        self._objects = {
            1: {  # SysInfo
                OBJECT_ID_KEY: 1,
                OBJECT_TYPE_KEY: 264,
                PROFILE_LIST_KEY: all_profiles(),
                OBJECT_DATA_KEY: b'\x00',
            },
            2: {  # Ticks
                OBJECT_ID_KEY: 2,
                OBJECT_TYPE_KEY: 262,
                PROFILE_LIST_KEY: all_profiles(),
                OBJECT_DATA_KEY: b'\x00',
            },
            3: {  # OneWireBus
                OBJECT_ID_KEY: 3,
                OBJECT_TYPE_KEY: 256,
                PROFILE_LIST_KEY: all_profiles(),
                OBJECT_DATA_KEY: b'\x00',
            },
            4: {  # Profiles
                OBJECT_ID_KEY: 4,
                OBJECT_TYPE_KEY: 263,
                PROFILE_LIST_KEY: all_profiles(),
                OBJECT_DATA_KEY: b'\x08\x01\x00',  # active = 1 (profiles=[0])
            }
        }

    def respond(self, cmd) -> commands.Command:
        # Encode + decode request
        args = cmd.from_encoded(cmd.encoded_request, None).decoded_request

        func = self._generators[type(cmd)]
        retv = func(args)

        # Encode + decode response
        encoding_cmd = cmd.from_decoded(cmd.decoded_request, retv or dict())
        return cmd.from_encoded(encoding_cmd.encoded_request, encoding_cmd.encoded_response)

    def _read_object(self, request):
        try:
            return self._objects[request[OBJECT_ID_KEY]]
        except KeyError:
            raise exceptions.CommandException(f'{request} not found')

    def _write_object(self, request):
        key = request[OBJECT_ID_KEY]
        if key not in self._objects:
            raise exceptions.CommandException(f'{key} not found')

        self._objects[key] = request
        return request

    def _create_object(self, request):
        key = request.get(OBJECT_ID_KEY)
        obj = request

        if not key:
            key = next(self._id_counter)
            obj[OBJECT_ID_KEY] = key
        elif key in self._objects:
            raise exceptions.CommandException(f'Object {key} already exists')

        self._objects[key] = obj
        return obj

    def _delete_object(self, request):
        key = request[OBJECT_ID_KEY]
        del self._objects[key]

    def _list_active_objects(self, request):
        return {
            PROFILE_LIST_KEY: self._active_profiles,
            OBJECT_LIST_KEY: [
                obj for obj in self._objects.values()
                if obj[OBJECT_ID_KEY] < OBJECT_ID_START
                or set(obj[PROFILE_LIST_KEY]) & set(self._active_profiles)
            ]
        }

    def _list_stored_objects(self, request):
        return {
            PROFILE_LIST_KEY: self._active_profiles,
            OBJECT_LIST_KEY: [obj for obj in self._objects.values()]
        }

    def _clear_objects(self, request):
        self._objects = {k: v for k, v in self._objects.items() if k < OBJECT_ID_START}

    def _factory_reset(self, request):
        pass

    def _reboot(self, request):
        pass


class SimulationCommander(commander.SparkCommander):

    def __init__(self, app: web.Application):
        super().__init__(app)
        self._responder = SimulationResponder()

    async def startup(self, app: web.Application):
        status.get_status(app).connected.set()

    async def shutdown(self, _):
        pass

    async def execute(self, command: commands.Command) -> dict:
        return self._responder.respond(command).decoded_response
