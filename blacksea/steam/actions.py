#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt


from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir="steam"
NoStrip = ["/"]
datadir = "/usr/share"



def install():
    installdir = get.installDIR()+ datadir
    pisitools.dodir(datadir)
    pisitools.dodir("%s/applications" % datadir)

    shelltools.copytree("%s/steam" % get.workDIR(), "%s/" % installdir)

    pisitools.dobin("%s/steam/steam" % installdir)
    pisitools.insinto("/usr/lib/steam/","bootstraplinux_ubuntu12_32.tar.xz","bootstraplinux_ubuntu12_32.tar.xz")
    
    