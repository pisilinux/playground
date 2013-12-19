#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import perlmodules
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools

def setup():
    shelltools.export("KOHA_CONF_DIR", "/etc/koha")
    perlmodules.configure()

def build():
    perlmodules.make()

def install():
    perlmodules.install()
    shelltools.system("sed -i 's|%s||g' %s/etc/koha/{*.conf,*.xml}"  % (get.installDIR(), get.installDIR()))
    shelltools.system("sed -i 's|%s||g' %s/etc/koha/zebradb/*.cfg" % (get.installDIR(), get.installDIR()))
    shelltools.system("sed -i 's|%s||g' %s/usr/share/koha/bin/{*.sh,*.pl}" % (get.installDIR(), get.installDIR()))
    pisitools.dodoc("README")
