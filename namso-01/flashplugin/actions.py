# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools

ARCH = "i386" if get.ARCH() == "i686" else "x86_64"
WorkDir = get.ARCH()
NoStrip = "/"

def install():
    shelltools.copy("*", "flashplugin-11.2.202.332-x86_64/usr/")
    distdir = "%s-%s-%s" % (get.srcNAME(), get.srcVERSION(), ARCH)

    shelltools.copytree("%s/usr" % distdir, "%s/usr" % get.installDIR())

    if get.ARCH() == "x86_64":
        pisitools.remove("/usr/lib/kde4/kcm_adobe_flash_player.so")
        pisitools.insinto("/usr/lib/kde4", "%s/%s/%s/usr/lib64/kde4/kcm_adobe_flash_player.so" % (get.workDIR(), get.ARCH(), distdir))
        pisitools.removeDir("/usr/lib64")

    pisitools.doexe("%s/usr/libflashplayer.so" % distdir, "/usr/lib/browser-plugins")
    
    pisitools.remove("/usr/readme.txt")
    pisitools.remove("/usr/libflashplayer.so")

