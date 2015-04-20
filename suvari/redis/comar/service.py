#!/usr/bin/python

from comar.service import *

serviceType="server"
serviceDesc = _({"en": "redis Server",
                 "tr": "redis Sunucusu"})

@synchronized
def start():
    startService(command="/usr/bin/redis",
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/var/run/redis.pid",
                donotify=True)

def status():
    return isServiceRunning("/var/run/redis.pid")
