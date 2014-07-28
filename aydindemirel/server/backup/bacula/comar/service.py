# -*- coding: utf-8 -*-
from comar.service import *
import os

serviceType = "server"
serviceDesc = _({"en": "Bacula Daemon",
                 "tr": "Bacula Servisi"})
BACULA-DIR-PID = "/run/bacula-dir.9101.pid"
BACULA-FD-PID = "/run/bacula-fd.9102.pid"
BACULA-SD-PID = "/run/bacula-sd.9103.pid"
PIDFILE = "/run/bacula.pid"

@synchronized
def start():
    startService(command="/usr/bin/bacula",
                 args="start",
                 pidfile=PIDFILE,
                 makepid=True,
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/bin/bacula",
                args="stop",
                donotify=True)
    if os.path.exists(BACULA-DIR-PID):
        os.unlink(BACULA-DIR-PID)
    if os.path.exists(BACULA-FD-PID):
        os.unlink(BACULA-FD-PID)
    if os.path.exists(BACULA-SD-PID):
        os.unlink(BACULA-SD-PID)

def status():
    return isServiceRunning(pidfile=PIDFILE)
