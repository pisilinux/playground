#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import qt4

WorkDir = "qsopcast-0.3.8.1-qt4"

def setup():
    shelltools.cd("src")
    pisitools.dosed("qsopcast.pro", "/usr/local/bin","/usr/bin")
    pisitools.dosed("main.cpp", "/usr/local/include/qsopcast/","/usr/share/locale/qsopcast/")
    pisitools.dosed("qsopcast.pro", "/usr/local/include/qsopcast","/usr/share/locale/qsopcast")
    pisitools.dosed("qsopcast.pro", "language_br","language_tr")
    qt4.configure()



def build():
    shelltools.cd("src")
    qt4.make()

def install():
    shelltools.cd("src")
    qt4.install()
    shelltools.cd("..")
    pisitools.dodoc("AUTHORS", "COPYING", "README")
