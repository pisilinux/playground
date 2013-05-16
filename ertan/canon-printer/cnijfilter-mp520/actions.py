#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

libs = (
    "libcnbpcnclui328.so.3.3.0",
    "libcnbpess328.so.3.0.9",
    "libcnbpo328.so.1.0.1",
    "libcnbpcnclapi328.so.3.3.0",
    "libcnbpcmcm328.so.6.61.1",
    "libcnbpcnclbjcmd328.so.3.3.0",
)

def setup():
    shelltools.system("tar xvf 28477.tgz")
    shelltools.system("rpm2targz cnijfilter-mp520series-2.80-1.i386.rpm")
    shelltools.system("tar xvf cnijfilter-mp520series-2.80-1.i386.tar.gz")
    shelltools.system("tar xvf guidemp520series-pd-2.80-1.tar.tar")

def build():
    pass

def install():
    pisitools.dobin("usr/local/bin/cifmp520")
    for lib in libs:
        pisitools.insinto("/usr/lib", "usr/lib/%s" % lib, "%s.so" % lib.split(".so")[0])
    pisitools.insinto("/%s/share/cups/model" % get.defaultprefixDIR(), "usr/share/cups/model/*.ppd")
    pisitools.insinto("/usr/lib/bjlib", "usr/lib/bjlib/*")

    pisitools.dohtml("guidemp520series-pd-2.80-1/MP520series/*")
