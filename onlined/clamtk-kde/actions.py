#!/usr/bin/python
# -*- coding: utf-8 -*-

from pisi.actionsapi import pisitools

def install():
    pisitools.dodoc("CHANGES","README","LICENSE")
    pisitools.doman("clamtk-kde.1.gz")
    pisitools.insinto("/usr/share/kde4/services","clamtk-kde.desktop")
