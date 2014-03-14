from comar.service import *

serviceType = "local"
serviceDefault = "off"
serviceDesc = _({"en": "OpenCT SmartCard Reader Service",
                 "tr": "OpenCT Akıllı Kart Okuyucu Servisi"})
serviceConf = "openct"

@synchronized
def start():
    startService(command="/usr/bin/hostapd",
                 args="init",
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/bin/hostapd",
                args="shutdown",
                donotify=True)

def status():
    import os.path
    return os.path.exists("/run")
