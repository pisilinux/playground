from comar.service import *
import os
serviceType = "server"
serviceDesc = _({"en": "Zebra text indexing and retrieval engine",
                 "tr": "Zebra metin indeksleme ve alma motoru"})
@synchronized
def start():
    startService(command="/usr/bin/zebrasrv",
                 args="-p /var/run/zebra.pid -f /etc/koha/koha-conf.xml",
                 detach=True,
                 donotify=True)
@synchronized
def stop():
    stopService(pidfile="/var/run/zebra.pid",
                donotify=True)
def status():
    return isServiceRunning("/var/run/zebra.pid")