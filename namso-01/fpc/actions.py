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

fpcdir = "/usr/lib/fpc/2.64"
docdir = "/usr/share/doc/fpc-2.64"

builddocdir = "%s/usr/share/doc/fpc-2.64" % get.workDIR()
buildlibdir = "%s/usr/lib" % get.workDIR()
buildmandir = "%s/usr/share" % get.workDIR()
buildbindir = "%s/usr/bin" % get.workDIR()
buildexamplesdir = "%s/usr/share/doc/fpc-2.64/examples" % get.workDIR()

version = get.srcVERSION().split("_")[0]
sourceDir = "%s/%s" % (get.workDIR(), get.srcDIR())
ppc = "ppcx64" if get.ARCH() == "x86_64" else "ppc386"

shelltools.export("GDBLIBDIR", "%s/gdb-7.5.1/gdb/" % get.workDIR())
shelltools.export("LIBGDBFILE", "%s/gdb-7.5.1/gdb/libgdb.a" % get.workDIR())

INSTALLOPS = ""

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
    shelltools.cd("fpcbuild-2.6.4/fpcsrc")
    shelltools.cd("compiler")
    shelltools.system("fpcmake -Tall")
    shelltools.cd("..")
    shelltools.cd("ide")
    shelltools.system("fpcmake -Tall")
    shelltools.cd("..")
    shelltools.cd("packages")
    shelltools.system("fpcmake -Tall")
    shelltools.cd("..")
    shelltools.cd("rtl")
    shelltools.system("fpcmake -Tall")
    shelltools.cd("..")
    shelltools.cd("utils")
    shelltools.system("fpcmake -Tall")
    shelltools.cd("..")
    shelltools.cd("..")
    shelltools.cd("fpcdocs")
    shelltools.system("fpcmake -Tall")
    shelltools.cd("..")
    autotools.make("build NOGDB=1")

def install():    
    shelltools.cd("fpcbuild-2.6.4")
    
    pisitools.insinto("/etc/", "install/amiga/fpc.cfg")
    pisitools.insinto("/etc/", "fpcsrc/utils/fpcmkcfg/fppkg.cfg")
        
    pisitools.insinto("/usr/lib/fpc/2.6.4/msg/", "fpcsrc/compiler/msg/*.msg")
    pisitools.doman("install/man/man1/*")
    pisitools.doman("install/man/man5/*")
    
    #for files in ["fpcsrc/utils/bin2obj", "fpcsrc/utils/data2inc", "fpcsrc/utils/delp", "fpcsrc/utils/grab_vcsa", "fpcsrc/utils/postw32", "fpcsrc/utils/ppdep", "fpcsrc/utils/ptop", "fpcsrc/utils/rmcvsdir", "fpcsrc/utils/rstconv" \
                 #"fpcsrc/compiler/ppcx64", "", "", "", "", "", "", "", ""]
        #pisitools.dobin("files")
    
    #autotools.rawInstall("PREFIX=%s/usr -C install -j1", get.installDIR())
    
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
