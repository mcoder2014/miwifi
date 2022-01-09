#!/usr/bin/python3
import configparser
from . import exception


class Config:
    def __init__(self):
        # 默认配置
        self.password = 'PASSWORD'
        self.route_ip = "192.168.31.1"
        self.max_retries = 3
        self.timeout = 600000
        self.reqTimeout = 10

    def Load(self, filepath):
        config = configparser.ConfigParser()
        result = config.read(filepath)
        if len(result) == 0:
            raise exception.ConfigError("read config file failed. program exit")
        self.password = config.get('config', 'PASSWORD')
        self.route_ip = config.get('config', 'ROUTE_IP')
        self.max_retries = config.getint('config', 'MAX_RETRIES')
        self.timeout = config.getint('config', 'TIMEOUT')
        self.teqTimeout = config.getint('config', 'REQ_TIMEOUT')
