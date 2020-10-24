
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt
from pisi.actionsapi import get, pisitools, shelltools

NoStrip = '/'


def setup():
    shelltools.system("ar xf brave-browser-nightly_1.18.6_amd64.deb")
    shelltools.system("tar xvf %s/data.tar.xz --exclude=usr/share/gnome-control-center --exclude=usr/bin --exclude=etc" %get.workDIR())
    shelltools.chmod(get.workDIR() + "/opt/brave.com/brave-nightly/brave-browser-nightly")


def install():
    pisitools.insinto("/opt/", "./opt/*")
    pisitools.insinto("/usr/", "./usr/*")
    pisitools.dosym("/opt/brave.com/brave-nightly/brave-browser-nightly", "/usr/bin/brave-browser-nightly")
    shelltools.system("chmod -v 4755 %s/opt/brave.com/brave-nightly/chrome-sandbox" %get.installDIR())
    #pisitools.dosym("/opt/brave.com/brave-nightly/brave-browser-nightly.desktop", "/usr/share/applications/brave-browser-nightly.desktop")
    
