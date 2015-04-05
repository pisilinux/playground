#!/usr/bin/python

import os, re


def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    try:
        os.system ("groupadd --system sddm")
        os.system ('useradd -c "Simple Desktop Display Manager" --system -d /var/lib/sddm -s /usr/bin/nologin -g sddm sddm')
        os.system ("passwd -l sddm > /dev/null")
        os.system ("chown -R sddm:sddm /var/lib/sddm > /dev/null")
    except:
        pass

def postRemove():
    try:
        os.system ("userdel sddm")
        os.system ("groupdel sddm")
    except:
        pass