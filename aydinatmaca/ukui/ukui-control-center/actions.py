#!/usr/bin/python
# -*- coding: utf-8 -*-
#

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get
from pisi.actionsapi import qt5

def setup():
    shelltools.system('qmake CONFIG+="configure WITH_I18N" \
    QMAKE_CFLAGS_ISYSTEM= \
    PREFIX=/usr \
    LIBPREFIX=/usr/lib \
    L_MANDIR=/usr/share/man \
    QT5LIBDIR=/usr/lib/qt5 \
    L_ETCDIR="/etc" \
    ukui-control-center.pro')

def build():
    qt5.make()

def install():
    qt5.install()
 
