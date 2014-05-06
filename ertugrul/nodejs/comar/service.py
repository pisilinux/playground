
from comar.service import *

serviceType = "local"
serviceConf = "nodejs"
serviceDefault = "conditional"

serviceDesc = _({"en": "Nodejs",
                 "tr": "Nodejs"})

@synchronized
def start():
    startService(command="/usr/sbin/nodejs",
                 args = config.get("args", "destroy"),
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/sbin/nodejs",
                donotify=True)

def ready():
    import os
    status = is_on()
    if status == "on" or (status == "conditional" and os.path.exists("/sys/coffee/ready")):
        start()

def status():
    return checkDaemon("/var/run/nodejs.pid")

