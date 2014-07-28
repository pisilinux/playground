from comar.service import *

serviceType = "server"
serviceDesc = _({"en": "Snort Network Intrusion Prevention and Detection System ",
                 "tr": "Snort Ağ Zaafiyet Tespit ve Önleme Sistemi"})

@synchronized
def start():
    startService(command="/usr/bin/snort",
                 ARGS=" -c /etc/snort/snort.conf -l /var/log/snort/",
                 pidfile="/run/snort/snort.pid",
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/run/snort/snort.pid",
                donotify=True)

def status():
    return isServiceRunning("/run/snort/snort.pid")
