#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import libtools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    libtools.libtoolize()
    autotools.configure("-prefix=/usr \
                         --sbindir=/usr/bin \
                         --with-systemd=/usr/lib/systemd/system/ \
                         --with-openssl \
                         --sysconfdir=/etc/bacula \
                         --enable-smartalloc \
                         --enable-bat \
                         --with-mysql \
                         --with-smtp-host=localhost \
                         --with-scriptdir=/etc/bacula/scripts")

def build():
    autotools.make("depend")
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.dodoc("COPYING", "AUTHORS", "VERIFYING", "SUPPORT", "LICENSE", "INSTALL", "COPYRIGHT")

