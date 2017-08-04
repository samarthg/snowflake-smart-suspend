import argparse
import time
from smart_suspend import SmartSuspend
from snowflake_config import SnowflakeConnection
from daemonize import Daemon

def run_smart_suspend():
    parser = argparse.ArgumentParser()
    parser.add_argument("option", help="To start/stop/restart the service",
                        type=str, choices=['start', 'stop', 'restart'])
    parser.add_argument("-r", "--role", help="""Snowflake role to be used while running the service.""")
    parser.add_argument("-c", "--connection", help="""Snowflake profile to be used form configuration file.""")
    parser.add_argument("-s", "--suspend-after-minutes", type=int, help="""Minutes past which if warehouse is unused will be suspended""")
    parser.add_argument("-i", "--check-interval", type=int, help="""Interval between two checks to determine state of warehouse in seconds""")
    parser.add_argument("-w", "--warehouses-to-smart-suspend", dest="warehouses", nargs='+',
                        help="List of warehouses to smart suspend")
    parser.add_argument("--noop", help="won't actually suspend the warehouse, but would log if it was eligible for suspension",
                        action="store_true", default=False)
    parser.add_argument("-d", help="Enables debug logging", dest="is_debug",
                        action="store_true", default=False)
    args = parser.parse_args()

    connection_profile = args.connection if args.connection else 'connections'
    role = args.role
    suspend_after_minutes = args.suspend_after_minutes
    check_interval = args.check_interval if args.check_interval else 30
    warehouses_to_smart_suspend = args.warehouses
    noop = args.noop
    is_debug = args.is_debug
    '''sc = SnowflakeConnection(role, connection_profile)
    ss = SmartSuspend(sc, suspend_after_minutes, warehouses_to_smart_suspend)
    ss.suspend_running_warehouses()'''

    # TODO Periodic authentication as token expires with time
    # Make it a service
    # Logging
    # Profit tracking
    # configurable check interval
    # configure suspend after minute
    # configure list of warehouse to smart suspend
    # Conditionally check how long warehouse being unused before suspending

    class MyDaemon(Daemon):

        def run(self):
            sc = SnowflakeConnection(role, connection_profile)
            ss = SmartSuspend(sc, suspend_after_minutes, warehouses_to_smart_suspend, noop, is_debug)
            while True:
                ss.suspend_running_warehouses()
                time.sleep(check_interval)

    daemon = MyDaemon('/tmp/smart_suspend.pid')
    if args.option=='start':
        daemon.start()
    if args.option=='stop':
        daemon.stop()
    if args.option=='restart':
        daemon.restart()