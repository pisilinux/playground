# -*- coding: utf-8 -*-

from comar.service import *

serviceType = "local"
serviceDesc = _({"en": "FIXME",
                 "tr": "FIXME"})

serviceDefault = "off"

PIDFILE = "/run/bumblebeed.pid"
DAEMON = "/usr/sbin/bumblebeed"

@synchronized
def start():
    startService(command=DAEMON,
                 args="--daemon",
                 pidfile=PIDFILE,
                 detach=True)

@synchronized
def stop():
    stopService(pidfile=PIDFILE,
                donotify=True)

def status():
    return isServiceRunning(pidfile=PIDFILE)
