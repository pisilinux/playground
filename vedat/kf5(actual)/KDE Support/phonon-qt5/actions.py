#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get


def setup():
  
    cmaketools.configure("-DCMAKE_BUILD_TYPE=Release \
                          -DCMAKE_INSTALL_PREFIX=/usr \
                          -DPHONON_BUILD_PHONON4QT5=ON \
                          -DPHONON_INSTALL_QT_EXTENSIONS_INTO_SYSTEM_QT=ON \
                          -DCMAKE_INSTALL_LIBDIR=lib \
                          -DCMAKE_SKIP_RPATH=ON")

def install():
    cmaketools.rawInstall("DESTDIR=%s" % get.installDIR())
    

    #some applications like mediaplayer example of Qt needs this #11648
    #pisitools.dosym("/usr/include/KDE/Phonon", "/usr/include/Phonon")
