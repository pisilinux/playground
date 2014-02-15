
from comar.service import *

serviceType = "local"
serviceConf = "imagewriter"
serviceDefault = "conditional"

serviceDesc = _({"en": "Imagewriter",
                 "tr": "Imagewriter"})

@synchronized
def start():
    startService(command="/usr/sbin/imagewriter",
                 args = config.get("args", "destroy"),
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/sbin/imagewriter",
                donotify=True)

def ready():
    import os
    status = is_on()
    if status == "on" or (status == "conditional" and os.path.exists("/sys/coffee/ready")):
        start()

def status():
    return checkDaemon("/var/run/imagewriter.pid")

