#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import kde4
from pisi.actionsapi import get


def setup():
    kde4.configure("DQT_QMAKE_EXECUTABLE=qmake-qt4 \
                          DCMAKE_BUILD_TYPE=Release \
                          DCMAKE_INSTALL_PREFIX=`kde4-config --prefix`")

def build():
    kde4.make()

def install():
    kde4.install("DESTDIR=%s" % get.installDIR())