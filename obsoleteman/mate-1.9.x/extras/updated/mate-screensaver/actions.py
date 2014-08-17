#!/usr/bin/python
# -*- coding: utf-8 -*-
#

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.configure("--disable-static \
                         --with-xscreensaverdir=/usr/share/xscreensaver/config \
                         --with-xscreensaverhackdir=/usr/lib/xscreensaver \
                         --with-mit-ext \
                         --with-console-kit \
                         --with-libnotify \
                         --without-systemd \
                         --enable-locking \
                         --with-gtk=2.0")

    # for fix unused dependency
    pisitools.dosed("libtool"," -shared ", " -Wl,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    # remove needless gsettings convert file to avoid slow session start
    pisitools.removeDir("/usr/share/MateConf")

    pisitools.dodoc("README", "NEWS", "ChangeLog", "AUTHORS", "COPYING")
