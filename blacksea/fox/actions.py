#!/usr/bin/pytho
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.configure("--prefix=/usr \
                --enable-release \
                --with-xft=yes \
                --with-opengl=yes \
                --with-xim \
                --with-xshm \
                --with-shape \
                --with-xcursor \
                --with-xrender \
                --with-xrandr \
                --with-xfixes \
                --with-xinput")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("AUTHORS","README")
