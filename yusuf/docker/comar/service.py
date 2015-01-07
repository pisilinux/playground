# -*- coding: utf-8 -*-
from comar.service import *
import os

serviceType = "local"
serviceDefault = "off"
serviceDesc = _({"en": "Docker Management Service",
                 "tr": "Docker Yönetim Hizmeti"})

MSG_ERR_TIMDPTCH = _({"en": "Failed to set patchset %s for docker.",
                      "tr": "Yama kümesi %s docker'ye atanamadı.",
                      })

pidfile="/run/docker.pid"

def cgroupfs_mount():
    os.system("/bin/cgroupfs_mount")

@synchronized
def start():
    cgroupfs_mount()
    startService(command="/usr/bin/docker",
                 args="-d -D",
                 pidfile="/run/docker.pid",
                 makepid=True,
                 detach=True,
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/run/docker.pid",
                donotify=True)

    os.system("/bin/cgroupfs_umount")

def status():
    return isServiceRunning("/run/docker.pid")
