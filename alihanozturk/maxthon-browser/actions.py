#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir = "."
NoStrip = ["/"]

def install():
    pisitools.insinto("/opt/", "./*")
    shelltools.system("chown root:root %s/opt/maxthon/maxthon_sandbox" % get.installDIR())
    shelltools.system("chmod -v 4755 %s/opt/maxthon/maxthon_sandbox" %get.installDIR())
    pisitools.dosym("/opt/maxthon/maxthon-browser", "/usr/bin/maxthon")
    pisitools.dosym("/opt/maxthon/maxthon.desktop", "/usr/share/applications/maxthon-browser.desktop")
    pisitools.dosym("/opt/maxthon/product_logo_22.png", "/usr/share/icons/hicolor/22x22/apps/maxthon-browser.png")
    pisitools.dosym("/opt/maxthon/product_logo_24.png", "/usr/share/icons/hicolor/24x24/apps/maxthon-browser.png")
    pisitools.dosym("/opt/maxthon/product_logo_32.png", "/usr/share/icons/hicolor/32x32/apps/maxthon-browser.png")
    pisitools.dosym("/opt/maxthon/product_logo_48.png", "/usr/share/icons/hicolor/48x48/apps/maxthon-browser.png")
    pisitools.dosym("/opt/maxthon/product_logo_64.png", "/usr/share/icons/hicolor/64x64/apps/maxthon-browser.png")
    pisitools.dosym("/opt/maxthon/product_logo_128.png", "/usr/share/icons/hicolor/128x128/apps/maxthon-browser.png")
    pisitools.dosym("/opt/maxthon/product_logo_256.png", "/usr/share/icons/hicolor/256x256/apps/maxthon-browser.png")
    pisitools.dosym("/opt/maxthon/conf.d/pn", "/etc/default/maxthon.d/pn")
    pisitools.dosym("/usr/lib/libudev.so", "/opt/maxthon/libudev.so.0")
    pisitools.dosym("/usr/lib/libgcrypt.so.11.8.2", "/opt/maxthon/libgcrypt.so.11")
    pisitools.remove("/opt/pisiBuildState")