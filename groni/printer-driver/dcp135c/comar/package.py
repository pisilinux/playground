#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    if not os.path.exists("/usr/local/Brother/cupswrapper/cupswrapperDCP7030-2.0.2"):
        os.system("/usr/local/Brother/cupswrapper/cupswrapperDCP7030-2.0.2 -i")

def preRemove():
    if os.path.exists("/usr/local/Brother/cupswrapper/cupswrapperDCP7030-2.0.2"):
        os.system("/usr/local/Brother/cupswrapper/cupswrapperDCP7030-2.0.2 -e")
