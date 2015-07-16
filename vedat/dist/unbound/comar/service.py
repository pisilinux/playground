# -*- coding: utf-8 -*-
from comar.service import *
import os

serviceType="server"
serviceDesc = _({"en": "Unbound DNS Resolver",
                 "tr": "Unbound DNS Çözümleyici"})
serviceDefault = "on"
PIDFILE = "/run/unbound.pid"

@synchronized
def start():
    startService(command="/usr/sbin/unbound",
                 pidfile=PIDFILE,
                 detach=True,
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile=PIDFILE,
                donotify=True)

    try:
        os.unlink(PIDFILE)
    except OSError:
        pass

def status():
    return isServiceRunning(PIDFILE)
