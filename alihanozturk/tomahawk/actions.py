#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import kde5
from pisi.actionsapi import get
from pisi.actionsapi import pisitools

def setup():
    kde5.configure("-DBUILD_WITH_QT4:BOOL=OFF")

def build():
    kde5.make()

def install():
    kde5.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("ChangeLog", "AUTHORS", "LICENSE*", "PACKAGING*", "README*")
