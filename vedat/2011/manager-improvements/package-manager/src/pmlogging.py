#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import sys
import logging

class Logger:

    def __init__(self):
        self.__initLogger()
        self.__setStreamHandler()
        self.__setupLogFile()

    def __initLogger(self):
        self.logger = logging.getLogger('package-manager')
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s\t%(message)s')
        self.logger.setLevel(logging.DEBUG)

    def __setStreamHandler(self):
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def __setupLogFile(self):
        logfile = os.path.join(os.environ['HOME'], ".package-manager.log")
        handler = logging.FileHandler(logfile)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.info(message)

logger = Logger()
