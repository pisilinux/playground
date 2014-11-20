#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

WorkDir = "."
NoStrip = ["/"]

def setup():
    shelltools.system("rpm2targz -v %s/birdfont-1.9-5.1.x86_64.rpm" %get.workDIR())
    shelltools.system("tar xfvz %s/birdfont-1.9-5.1.x86_64.tar.gz" %get.workDIR())
    #shelltools.chmod(get.workDIR() + "/opt/google/chrome/*", 0755)

def install():
    #pisitools.insinto("/opt/", "./opt/*")
    pisitools.insinto("/usr/", "./usr/*")
    pisitools.dosym("/usr/lib64/libbirdfont.so", "/usr/lib/libbirdfont.so")
    pisitools.dosym("/usr/lib64/libbirdfont.so.31", "/usr/lib/libbirdfont.so.31")
    pisitools.dosym("/usr/lib64/libbirdfont.so.31.0", "/usr/lib/libbirdfont.so.31.0")
    pisitools.dosym("/usr/lib64/libbirdxml.so", "/usr/lib/libbirdxml.so")
    pisitools.dosym("/usr/lib64/libbirdxml.so.0", "/usr/lib/libbirdxml.so.0")
    pisitools.dosym("/usr/lib64/libbirdxml.so.0.0", "/usr/lib/libbirdxml.so.0.0")

# By PiSiDo 2.0.0
