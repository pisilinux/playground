 #!/usr/bin/python
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
--sysconfdir=/etc \
--localstatedir=/var \
--mandir=/usr/share/man \
--with-tables-directory=/usr/share/brltty \
--with-screen-driver=lx \
--enable-gpm \
--disable-java-bindings \
--disable-static")


def build():
    autotools.make()

def install():
     shelltools.copytree("lib", "%s/usr/lib/brltty" % get.installDIR())
     shelltools.copytree("Tables", "%s/usr/share/brltty" % get.installDIR())
     pisitools.insinto("/usr/bin/", "Programs/brltty", "brltty")
     pisitools.insinto("/usr/bin/", "Programs/brltty-config", "brltty-config")
     pisitools.insinto("/usr/bin/", "Programs/brltty-ctb", "brltty-ctb")
     pisitools.insinto("/usr/bin/", "Programs/brltty", "brltty-install")
     pisitools.insinto("/usr/bin/", "Programs/brltty", "brltty-trtxt")
     pisitools.insinto("/usr/bin/", "Programs/brltty", "brltty-ttb")
     pisitools.insinto("/usr/bin/", "Programs/brltty", "brltty-ttb")
     pisitools.insinto("/usr/bin/", "Programs/xbrlapi", "xbrlapi")
     pisitools.insinto("/etc", "Documents/brltty.conf", "brltty.conf")
     
  
     pisitools.dodoc("LICENSE-GPL","LICENSE-LGPL", "README")

