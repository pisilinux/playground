#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import mesontools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    mesontools.configure("--prefix=/usr \
                          --libexecdir=/usr/lib \
                          -Dfallback-session=gnome")

def build():
    mesontools.build()

def install():
    mesontools.install()

    pisitools.dodoc("README.md")
