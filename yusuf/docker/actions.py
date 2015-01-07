#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

shelltools.export("AUTO_GOPATH", "1")
shelltools.export("DOCKER_GITCOMMIT", "5bc2ff8") #DOCKER_GITCOMMIT="5bc2ff8"
shelltools.export("GOPATH", "%s" % get.workDIR())

shelltools.export("CGO_CFLAGS", "-I/usr/include")
shelltools.export("CGO_LDFLAGS", "-L/usr/lib")
shelltools.export("DOCKER_BUILDTAGS","exclude_graphdriver_aufs exclude_graphdriver_btrfs exclude_graphdriver_devicemapper")
  
NoStrip=["/"]

def build():
    shelltools.system("./hack/make.sh dynbinary")

def install():  
    pisitools.dobin("bundles/1.4.1/dynbinary/docker")
    pisitools.dobin("bundles/1.4.1/dynbinary/docker-1.4.1")
    pisitools.dobin("bundles/1.4.1/dynbinary/dockerinit")
    pisitools.dobin("bundles/1.4.1/dynbinary/dockerinit-1.4.1")
    
    # insert udev rules
    pisitools.insinto("/etc/udev/rules.d", "contrib/udev/*.rules")
           
    pisitools.dodoc("VERSION", "LICENSE", "README.md", "AUTHORS", "CONTRIBUTING.md", "CHANGELOG.md", "NOTICE")
       
