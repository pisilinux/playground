#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

def setup():
    shelltools.system("ar x %s/spotify-client-0.9.17_0.9.17.8.gd06432d.31-1_amd64.deb" % get.workDIR())
    shelltools.system("tar xJvf %s/data.tar.xz --exclude=usr/bin/spotify" %get.workDIR())

def install():
    pisitools.insinto("/usr/", "usr/*")
    pisitools.removeDir("/usr/share/spotify")
    pisitools.remove("/usr/share/doc/spotify-client-0.9.17/changelog.Debian.gz")
    pisitools.insinto("/opt/", "opt/*")
    for i in [16,22,24,32,48,64,128,256,512]:
		pisitools.dosym("/opt/spotify/spotify-client/Icons/spotify-linux-%s.png" % i,"/usr/share/icons/hicolor/{0}x{0}/apps/spotify-client.png".format(i))
    pisitools.dosym("/opt/spotify/spotify-client/spotify.desktop","/usr/share/applications/spotify.desktop")
    pisitools.dodoc("opt/spotify/spotify-client/changelog","opt/spotify/spotify-client/licenses.xhtml")
    pisitools.dosym("/opt/spotify/spotify-client/spotify","/usr/bin/spotify")
    pisitools.dosym("/usr/lib/libudev.so","/usr/lib/libudev.so.0")
