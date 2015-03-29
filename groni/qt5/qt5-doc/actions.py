#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import qt5
from pisi.actionsapi import get

def setup():
    shelltools.system("qmake-qt5 qtdoc.pro")
    shelltools.cd("doc/src")
    shelltools.system("qhelpgenerator *.qdoc")
def build():
    qt5.make()

def install():
    qt5.install("INSTALL_ROOT=%s" % get.installDIR())
    #pisitools.insinto("/usr/share/licenses/qt5-doc/", "LGPL_EXCEPTION.txt")
