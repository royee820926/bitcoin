# encoding=utf-8

import os
import time
import logging
from logging import handlers

class Logger:
    __log_handler = None
    __log_name = None
    __default_log_name = 'root'
    __log_array = []
    __log_path = 'logs'
    __log_level = logging.DEBUG
    __file_name = None
    __default_file_name = 'app.log'
    __backupCount = 0
    __config = {}

    def __init__(self, config, log_name='', file_name='', log_level=logging.DEBUG):
        self.set_config(config)
        self.set_log_name(log_name)
        self.set_file_name(file_name)
        self.set_log_level(log_level)
        self.init_log_handler()

    def log(self, message):
        """
        写入日志
        :param message:
        :return:
        """
        self.get_log_handler().log(self.get_log_level(), msg=message)

    def init_log_handler(self):
        # 创建log_name目录
        root_path = self.get_config('root_path')
        log_path = root_path + os.path.sep + 'logs' + os.path.sep + self.get_log_name()
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        path_file = log_path + '/' + self.__file_name
        logging.basicConfig()
        main_log = logging.getLogger(self.get_log_name())
        main_log.setLevel(self.get_log_level())

        handler = handlers.TimedRotatingFileHandler(path_file, when='D', backupCount=self.__backupCount, interval=1)
        handler.suffix = '%Y-%m-%d.log'
        # handler.setFormatter(logging.Formatter('%(asctime)s %(pathname)s[line:%(lineno)d][%(levelname)s] %(message)s'))
        handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        main_log.addHandler(handler)
        self.set_log_handler(main_log)

    def set_file_name(self, file_name):
        if file_name == '':
            # self.__file_name = self.__default_file_name
            self.__file_name = time.strftime("%Y-%m-%d.log", time.localtime(time.time()))
        else:
            self.__file_name = file_name

    def set_log_name(self, log_name):
        if log_name == '':
            self.__log_name = self.__default_log_name
        else:
            self.__log_name = log_name

    def get_log_name(self):
        if self.__log_name is None:
            return self.__default_log_name
        else:
            return self.__log_name

    def set_backup_count(self, backupCount):
        self.__backupCount = backupCount

    def set_config(self, config):
        self.__config = config

    def get_config(self, key):
        if key in self.__config:
            return self.__config[key]
        else:
            return ''

    def set_log_level(self, log_level):
        self.__log_level = log_level

    def get_log_level(self):
        return self.__log_level

    def set_log_handler(self, log_handler):
        self.__log_handler = log_handler

    def get_log_handler(self):
        if self.__log_handler is None:
            self.init_log_handler()
        return self.__log_handler
