#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

NoStrip = ["/usr/share/fpcsrc"]

WorkDir = "."

version = get.srcVERSION().split("_")[0]
sourceDir = "%s/%s" % (get.workDIR(), get.srcDIR())
ppc = "ppcx64" if get.ARCH() == "x86_64" else "ppc386"

shelltools.export("GDBLIBDIR", "/var/pisi/fpc-2.6.4-4/work/gdb-7.5.1/gdb/")
shelltools.export("LIBGDBFILE", "/var/pisi/fpc-2.6.4-4/work/gdb-7.5.1/gdb/libgdb.a")

def setup():
    shelltools.cd("gdb-7.5.1")
    autotools.configure("--prefix=/usr \
                         --disable-nls \
                         --without-python \
                         --disable-werror \
                         --disable-tui")
    
    
def build():
    shelltools.cd("gdb-7.5.1")
    autotools.make()
    autotools.make("-C gdb libgdb.a")
    shelltools.system("cp libdecnumber/libdecnumber.a gdb/")
    shelltools.cd("..")
    shelltools.cd("fpcbuild-2.6.4")
    shelltools.cd("fpcsrc/compiler")
    shelltools.system("fpcmake -Tall")
    shelltools.cd("..")
    shelltools.cd("..")
    autotools.make("NOGDB=1")

def install():    
    shelltools.cd("fpcbuild-2.6.4")
    
    pisitools.insinto("/etc/", "install/amiga/fpc.cfg")
    pisitools.insinto("/etc/", "fpcsrc/utils/fpcmkcfg/fppkg.cfg")
    
    autotools.rawInstall("PREFIX=%s/usr -C install -j1", get.installDIR())
    
    #pisitools.dosym("../lib/fpc/%s/%s" % (version, ppc), "/usr/bin/%s" % ppc)
    
    #pisitools.removeDir("/usr/lib/fpc/lexyacc")

    #shelltools.system("%(root)s/usr/lib/fpc/%(ver)s/samplecfg"
                      #" %(root)s/usr/lib/fpc/%(ver)s %(root)s/etc" \
                        #% {"root": get.installDIR(), "ver": version})

    #autotools.make("PP=%s/ppc_new clean" % sourceDir)
    #shelltools.copytree(".", "%s/usr/share/fpcsrc/" % get.installDIR())
    #pisitools.remove("/usr/share/fpcsrc/ppc*")

    #pisitools.rename("/usr/share/doc/fpc-%s" % version, get.srcNAME())
    pisitools.dodoc("fpcsrc/rtl/COPYING.FPC")
