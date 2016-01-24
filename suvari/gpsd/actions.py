#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import scons
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    shelltools.cd("..")
    shelltools.cd("gpsd-3.16")
    
    #shelltools.export("NCURSES_CONFIG", "/usr/bin/ncursesw6-config")

def build():
    shelltools.cd("..")
    shelltools.cd("gpsd-3.16")
    scons.make("prefix=/usr \
                libQgpsmm=no \
                gpsd_group=uucp \
                ncursesdir=/usr/bin/ncursesw6-config \
                sbindir=/usr/bin")
    # fix python 2.7 path
    #shelltools.system("sed -i -e "s|#![ ]*/usr/bin/python$|#!/usr/bin/python2|"
                              #-e "s|#![ ]*/usr/bin/env python$|#!/usr/bin/env python2|" \
    #$(find . -name *.py)
    shelltools.system("sed -i 's|/usr/bin/env python|/usr/bin/env python|' gegps \
                                                                            gpscat gpsfake gpsprof xgps xgpsspeed")
    shelltools.system("sed -i 's/sbin/bin/g' comar/*.service")

    #autotools.make()

def install():
    shelltools.cd("..")
    shelltools.cd("gpsd-3.16")
    #autotools.install()

    # We're using conf.d instead of sysconfig
    pisitools.dosed("gpsd.hotplug.wrapper", "sysconfig\/", "conf.d/")

    # Install UDEV files
    pisitools.insinto("/lib/udev/rules.d", "gpsd.rules", "99-gpsd.rules")
    pisitools.dobin("gpsd.hotplug", "/lib/udev")
    pisitools.dobin("gpsd.hotplug.wrapper", "/lib/udev")

    # Fix permissions
    shelltools.chmod("%s/usr/lib/%s/site-packages/gps/gps.py" % (get.installDIR(), get.curPYTHON()))

    pisitools.dodoc("README", "TODO", "AUTHORS", "COPYING")
