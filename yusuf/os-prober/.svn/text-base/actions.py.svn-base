#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import autotools
from pisi.actionsapi import get

WorkDir = "os-prober"

def build():
    autotools.make("CFLAGS='%s'" % get.CFLAGS())

def install():
    pisitools.dobin("os-prober")
    pisitools.dobin("linux-boot-prober")
    pisitools.dobin("newns", "/usr/libexec")

    pisitools.dodir("/var/lib/os-prober")

    pisitools.insinto("/usr/share/os-prober", "common.sh")

    for probes in ("os-probes", "os-probes/mounted", "os-probes/init",
                   "linux-boot-probes", "linux-boot-probes/mounted"):
        pisitools.insinto("/usr/libexec/%s" % probes, "%s/common/*" % probes)
        if shelltools.isDirectory("%s/x86" % probes):
            pisitools.insinto("/usr/libexec/%s" % probes, "%s/x86/*" % probes)

    pisitools.insinto("/usr/libexec/os-probes/mounted", "os-probes/mounted/powerpc/20macosx")

    pisitools.dodoc("README", "TODO")
