#!/usr/bin/python
# -*- coding: utf-8 -*-

from comar.service import *
import os 


serviceType = "server"
serviceDesc = _({"en": "Server",
    "tr": "Sunucu"})

from comar.service import *

@synchronized
def start():
    startService(command="/etc/webmin/start",
            args="start",
            pidfile="/var/log/webmin/miniserv.pid",
            donotify=True)

@synchronized
def stop():
    stopService(command="/etc/webmin/stop",
            args="stop",
            donotify=True)

def status():
    return isServiceRunning("/var/log/webmin/miniserv.pid")
