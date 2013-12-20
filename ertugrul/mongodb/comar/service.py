from comar.service import *

import os

serviceType = "server"
serviceDefault = "off"

serviceDesc = _({"en": "Mongodb Database Server",
                 "tr": "Mongodb Veritabanı Sunucusu"})

PIDFILE = "/var/run/mongodb/mongodb.pid"
LOCKFILE= "/var/lib/mongodb/mongod.lock"

@synchronized
def start():
    startService(command="/usr/bin/mongod",
                 args = "--dbpath /var/lib/mongodb",
                 makepid=True,
                 pidfile=PIDFILE,
                 detach=True,
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/bin/mongod",
                donotify=True)

    if os.path.exists(LOCKFILE):
        os.unlink(LOCKFILE)
        
    if os.path.exists(PIDFILE):
        os.unlink(PIDFILE)

def status():
    return isServiceRunning(PIDFILE)
