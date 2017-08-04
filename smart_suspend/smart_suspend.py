import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from pytz import timezone
import copy
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

log_file_path = '/var/log/smartsuspend/system.log'
log_dir_path = os.path.dirname(os.path.abspath(log_file_path))
if not os.path.exists(log_dir_path):
    os.makedirs(log_dir_path)
handler = TimedRotatingFileHandler(log_file_path, when='d')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

debug_log_file_path = '/var/log/smartsuspend/debug.log'
debug_handler = TimedRotatingFileHandler(debug_log_file_path, when='d')
debug_handler.setLevel(logging.DEBUG)
#debug_handler.setFormatter(formatter)

logger.addHandler(debug_handler)


class SmartSuspend(object):

    def __init__(self, snowflake_connection, suspend_after_minutes, warehouses_to_smart_suspend, noop=False, debug=False):
        self.cursor = snowflake_connection.get_snowflake_cursor(True)
        self.suspend_after_minutes = suspend_after_minutes
        self.warehouses_to_smart_suspend = warehouses_to_smart_suspend
        self.noop = noop
        self.debug = debug

    def suspend_running_warehouses(self):
        warehouses_eligible_to_suspend = self.get_warehouses_to_suspend()
        warehouses_to_suspend = list((set(warehouses_eligible_to_suspend)).intersection(set(self.warehouses_to_smart_suspend)))
        if warehouses_to_suspend:
            for warehouse in warehouses_to_suspend:
                self.suspend_warehouse(warehouse)
        else:
            logger.info("Nothing to suspend")

    def get_snowflake_cursor(self):
        return self.cursor

    def suspend_warehouse(self, warehouse):
        if not self.noop:
            self.cursor.execute('alter warehouse %s SUSPEND' % warehouse)
            logger.info('{"name": "%s", "current_time": "%s", "state": "SMART_SUSPENDED"} ' % (warehouse, str(datetime.utcnow())))
        else:
            logger.info('noop: suspended warehouse %s' % warehouse)

    def get_running_warehouses(self):
        self.cursor.execute('show warehouses')
        warehouses_details = self.cursor.fetchall()
        if self.debug:
            self.log_warehouse_details(copy.deepcopy(warehouses_details))
        running_unused_warehouses = [warehouse_info for warehouse_info in warehouses_details if
                                     (warehouse_info['state']=='STARTED' and warehouse_info['running']==0 and warehouse_info['queued']==0)]
        return running_unused_warehouses

    def get_warehouses_to_suspend(self):
        running_warehouses = self.get_running_warehouses()
        warehouses_to_suspend = []
        for warehouse_info in running_warehouses:
            resumed_on = warehouse_info['resumed_on']
            current_time = resumed_on.now(tz=resumed_on.tzinfo)
            uptime = current_time - resumed_on
            minutes_from_current_hour = int((uptime.seconds/60)%60)
            if minutes_from_current_hour > self.suspend_after_minutes:
                warehouses_to_suspend.append(warehouse_info['name'])
        return warehouses_to_suspend

    def log_warehouse_details(self, warehouses_details):
        for warehouse_info in warehouses_details:
            logging_info = {}
            logging_info['current_time'] = str(datetime.utcnow())
            resumed_on = warehouse_info['resumed_on']
            logging_info['resumed_on'] = str(resumed_on.astimezone(timezone('UTC')))
            logging_info['state'] = warehouse_info['state']
            logging_info['name'] = warehouse_info['name']
            logging_info['queued'] = warehouse_info['queued']
            logging_info['running'] = warehouse_info['running']
            logger.info(json.dumps(logging_info))