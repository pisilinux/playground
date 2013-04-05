#!/usr/bin/python
#-*- coding: UTF-8 -*-

from comar.service import *
import os

serviceType = "local"
serviceDesc = _({
    "en": "GNOME Desktop",
    "tr": "GNOME Masaüstü",
})

def start(boot=False):
    if status():
        fail("gdm is already running")

    if not call("zorg", "Xorg.Display", "ready", (boot,), 5 * 60):
        fail("Not starting as zorg returned an error")

    startDependencies("acpid","hal")
    loadEnvironment()

    startService(command="/usr/sbin/gdm-binary")

def stop():
    stopService(pidfile="/var/run/gdm.pid")

def status():
    return isServiceRunning("/var/run/gdm.pid")
