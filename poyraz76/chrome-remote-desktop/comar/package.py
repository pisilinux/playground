from comar.service import *
import os

serviceType = "local"
serviceDesc = _({
    "en": "Chrome Remote Control Application",
    "tr": "Chrome Uzak Masaüstü Bağlantısı"})

serviceDefault = "on"


@synchronized
def start():
    loadEnvironment()
    startService(command="/opt/google/chrome-remote-desktop/start-host",
                 args="-d",
                 pidfile=pidFile,
                 makepid=True,
                 donotify=True)
        

@synchronized
def stop():
    stopService(pidfile=pidFile,
                donotify=True)
    os.unlink(pidFile)
             

def status():
    return isServiceRunning(pidFile)