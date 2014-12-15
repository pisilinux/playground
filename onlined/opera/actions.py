#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    shelltools.cd("x86_64")
    shelltools.system("ar x opera-stable_%s_amd64.deb" % get.srcVERSION())
    shelltools.system("tar -xJf data.tar.xz")

def install():
    shelltools.cd("x86_64")
    pisitools.insinto("/usr","usr/*")
    pisitools.domove("/usr/lib/x86_64-linux-gnu/opera","/usr/lib")
    pisitools.removeDir("/usr/lib/x86_64-linux-gnu")
    pisitools.removeDir("/usr/share/lintian")
    pisitools.remove("/usr/bin/opera")
    pisitools.dosym("/usr/lib/opera/opera","/usr/bin/opera")
    if not shelltools.isFile("/usr/lib/libudev.so.0"):
        pisitools.dosym("/usr/lib/libudev.so","/usr/lib/opera/lib/libudev.so.0")
    shelltools.system("chmod 4755 %s/usr/lib/opera/opera_sandbox" % get.installDIR())
