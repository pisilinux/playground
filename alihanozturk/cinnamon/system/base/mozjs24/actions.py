#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    shelltools.cd("js/src")
    shelltools.export("SHELL", "/bin/sh")
    autotools.configure("--with-system-nspr \
                         --disable-tests \
                         --disable-strip \
                         --enable-ctypes \
                         --enable-threadsafe \
                         --enable-readline \
                         --enable-system-ffi \
                         --disable-intl-api")

def build():
    shelltools.cd("js/src")
    autotools.make()

def check():
    shelltools.cd("js/src")
    autotools.make("check")

def install():
    shelltools.cd("js/src")
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
