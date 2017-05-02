import logging
import os
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
log_file_path = '/var/log/smartsuspend/system.log'
log_dir_path = os.path.dirname(os.path.abspath(log_file_path))
if not os.path.exists(log_dir_path):
    os.makedirs()
handler = TimedRotatingFileHandler(log_file_path, when='d')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class SmartSuspend(object):

    def __init__(self, snowflake_connection, suspend_after_minutes, warehouses_to_smart_suspend):
        self.cursor = snowflake_connection.get_snowflake_cursor(True)
        self.suspend_after_minutes = suspend_after_minutes
        self.warehouses_to_smart_suspend = warehouses_to_smart_suspend

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
        self.cursor.execute('suspend warehouse %s' % warehouse)
        logger.info('suspended warehouse %s' % warehouse)

    def get_running_warehouses(self):
        self.cursor.execute('show warehouses')
        warehouses_details = self.cursor.fetchall()
        running_unused_warehouses = [warehouse_info for warehouse_info in warehouses_details if
                                     (warehouse_info['state']=='STARTED' and warehouse_info['running']==0)]
        return running_unused_warehouses

    def get_warehouses_to_suspend(self):
        running_warehouses = self.get_running_warehouses()
        print(running_warehouses)

        warehouses_to_suspend = []
        for warehouse_info in running_warehouses:
            resumed_on = warehouse_info['resumed_on']
            current_time = resumed_on.now(tz=resumed_on.tzinfo)
            uptime = current_time - resumed_on
            minutes_from_current_hour = int((uptime.seconds/60)%60)
            if minutes_from_current_hour > self.suspend_after_minutes:
                warehouses_to_suspend.append(warehouse_info['name'])
        return warehouses_to_suspend