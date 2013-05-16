#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

libs = (
    "libcnbpcmcm312.so.6.50.1",
    "libcnbpcnclapi312.so.3.3.0",
    "libcnbpcnclbjcmd312.so.3.3.0",
    "libcnbpcnclui312.so.3.3.0",
    "libcnbpess312.so.3.0.9",
    "libcnbpo312.so.1.0.2",
)

def setup():
    shelltools.system("tar xvf 27213.tgz")
    shelltools.system("rpm2targz cnijfilter-ip1800series-2.70-1.i386.rpm")
    shelltools.system("tar xvf cnijfilter-ip1800series-2.70-1.i386.tar.gz")
    shelltools.system("tar xvf guideip1800series-pd-2.70-1.tar.gz")

def build():
    pass

def install():
    pisitools.dobin("usr/local/bin/cifip1800")
    for lib in libs:
        pisitools.insinto("/usr/lib", "usr/lib/%s" % lib, "%s.so" % lib.split(".so")[0])
    pisitools.dosym("libpng.so", "/usr/lib/libpng.so.3")
    pisitools.insinto("/%s/share/cups/model" % get.defaultprefixDIR(), "usr/share/cups/model/*.ppd")
    pisitools.insinto("/usr/lib/bjlib", "usr/lib/bjlib/*")

    pisitools.dohtml("guideip1800series-pd-2.70-1/iP1800series/*")
