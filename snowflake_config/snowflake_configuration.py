#!/usr/bin/env python
import configparser
import snowflake.connector
from snowflake.connector import DictCursor
import os

class SnowflakeConfigurations(object):

    def __init__(self, profile="connections"):
        self.config = configparser.ConfigParser()
        self.config.read(os.path.abspath(os.path.join(os.getenv('HOME'), ".snowsql", "config")))
        self.profile = profile

    def get_accountname(self):
        return self.config.get(self.profile, "accountname")

    def get_user(self):
        return self.config.get(self.profile, "username")

    def get_password(self):
        return self.config.get(self.profile, "password")

class SnowflakeConnection(object):

    def __init__(self, role, profile="connections"):
        config = SnowflakeConfigurations(profile)
        accountname = config.get_accountname()
        user = config.get_user()
        password = config.get_password()
        self.ctx = snowflake.connector.connect(
            user=user,
            password=password,
            account=accountname,
            role=role,
        )

    def get_snowflake_cursor(self, is_dict_cursor=False):
        if is_dict_cursor:
            return self.ctx.cursor(DictCursor)
        return self.ctx.cursor()