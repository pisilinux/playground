#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    shelltools.system("sed -i -e 's:import PAM:import pam:' files/usr/lib/cinnamon-settings/modules/cs_user.py")
    shelltools.system("sed -i -e 's|/usr/bin/cinnamon-control-center|/usr/lib/cinnamon-control-center-1/panels|' files/usr/bin/cinnamon-settings")
    shelltools.system("sed -i -e 's/gksu/pkexec/' files/usr/bin/cinnamon-settings-users")
    autotools.autoreconf("-vif")
    shelltools.system("NOCONFIGURE=1 ./autogen.sh")
    autotools.configure("--localstatedir=/var \
                         --libexecdir=/usr/lib/cinnamon \
                         --sysconfdir=/etc \
                         --disable-static \
                         --disable-rpath \
                         --disable-schemas-compile \
                         --enable-compile-warnings=yes \
                         --with-ca-certificates=/etc/ssl/certs/ca-certificates.crt")
    
    pisitools.dosed("libtool"," -shared ", " -Wl,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    shelltools.makedirs("/usr/share/cinnamon/locale/")

    pisitools.dodoc("README", "AUTHORS")