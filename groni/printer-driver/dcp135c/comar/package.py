#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    if not os.path.exists("/usr/share/cups/model/brdcp135c.ppd"):
        os.system("/usr/local/Brother/Printer/dcp135c/cupswrapper/cupswrapperdcp135c -i")

def preRemove():
    if os.path.exists("/usr/share/cups/model/brdcp135c.ppd"):
        os.system("/usr/local/Brother/Printer/dcp135c/cupswrapper/cupswrapperdcp135c -e")
