#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import qt4

def setup():
    pisitools.dosed("menu/luckybackup-kde-su.desktop", "^(Exec=)(\/usr\/bin\/luckybackup)", r"\1xdg-su -c \2")
    pisitools.dosed("menu/luckybackup-kde-su.desktop", "^(X-KDE-SubstituteUID=)true", r"\1false")
    qt4.configure()

def build():
    qt4.make()

def install():
    qt4.install()

    pisitools.remove("/usr/share/applications/luckybackup-gnome-su.desktop")
# By PiSiDo 2.0.0
