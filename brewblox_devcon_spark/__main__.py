"""
Example of how to import and use the brewblox service
"""

from brewblox_codec_spark import codec
from brewblox_devcon_spark import (broadcaster, commander, commander_sim,
                                   communication, datastore, device)
from brewblox_devcon_spark.api import (alias_api, conflict_api, debug_api,
                                       error_response, object_api, profile_api,
                                       system_api)
from brewblox_service import brewblox_logger, events, service

LOGGER = brewblox_logger(__name__)


def create_parser(default_name='spark'):
    parser = service.create_parser(default_name='spark')
    parser.add_argument('--database',
                        help='Backing file for the object database. [%(default)s]',
                        default='brewblox_db.json')
    parser.add_argument('--system-database',
                        help='Backing file for the system object database. [%(default)s]',
                        default='config/brewblox_sys_db.json')
    parser.add_argument('--device-port',
                        help='Spark device port. Automatically determined if not set. [%(default)s]')
    parser.add_argument('--device-id',
                        help='Spark serial number. Any spark is valid if not set. '
                        'This will be ignored if --device-port is specified. [%(default)s]')
    parser.add_argument('--simulation',
                        help='Start in simulator mode. Will not connect to a physical device. [%(default)s]',
                        action='store_true')
    parser.add_argument('--broadcast-interval',
                        help='Interval (in seconds) between broadcasts of controller state. [%(default)s]',
                        type=int,
                        default=5)
    parser.add_argument('--broadcast-exchange',
                        help='Eventbus exchange to which controller state should be broadcasted. [%(default)s]',
                        default='brewcast')
    parser.add_argument('--unit-system-file',
                        help='User configuration for units [%(default)s]')
    return parser


def main():
    app = service.create_app(parser=create_parser())

    if app['config']['simulation']:
        commander_sim.setup(app)
    else:
        communication.setup(app)
        commander.setup(app)

    codec.setup(app)
    datastore.setup(app)
    device.setup(app)

    error_response.setup(app)
    debug_api.setup(app)
    alias_api.setup(app)
    conflict_api.setup(app)
    object_api.setup(app)
    profile_api.setup(app)
    system_api.setup(app)

    events.setup(app)
    broadcaster.setup(app)

    service.furnish(app)

    # service.run() will start serving clients async
    service.run(app)


if __name__ == '__main__':
    main()
