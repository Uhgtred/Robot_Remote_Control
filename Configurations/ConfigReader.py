#!/usr/bin/env python3
# @author      Markus Kösters

import os
from pathlib import Path


class ConfigReader:

    def __init__(self):
        __filePath = Path(os.path.abspath(__file__))
        __filePath = __filePath.parent
        self.__confFile = os.path.join(__filePath, 'Configurations.conf')

    def readConfig(self):
        """Reads and returns Configurations.conf as dictionary."""
        configList = {}
        __configInfo = ''
        __configParameter = ''
        with open(self.__confFile, 'r') as __file:
            for __line in __file:
                __line = __line.strip()
                if __line and not __line.startswith('#'):
                    if '#' in __line:
                        __line = (__line.split('#'))[0]
                    __configParameter, __configInfo = __line.split('=')
                    __configInfo = __configInfo.strip()
                    if __configInfo.startswith('='):
                        __configInfo = __configInfo[1:].strip()
                configList[str(__configParameter).strip()] = __configInfo
        return configList

    def readConfigParameter(self, parameter):
        """Reads and returns a single Parameter from config dictionary"""
        configList = {}
        configList = self.readConfig()
        __parameter = parameter.strip()
        __configInfo = str(configList.get(__parameter))
        if ',' in __configInfo:
            __configInfo = __configInfo.split(',')
            for i in range(len(__configInfo)):
                __configInfo[i] = __configInfo[i].strip()
        elif __configInfo == 'None':
            __configInfo = None
        else:
            __configInfo = str(__configInfo).strip()
        return __configInfo
