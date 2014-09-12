#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

import os

WorkDir = "glibc-2.20"

arch = "x86-64" if get.ARCH() == "x86_64" and not get.buildTYPE() == "emul32" else "i686"
defaultflags = "-O3 -g -fasynchronous-unwind-tables -mtune=generic -march=%s" % arch
if get.buildTYPE() == "emul32": defaultflags += " -m32"
# this is getting ridiculous, also gdb3 breaks resulting binary
#sysflags = get.CFLAGS().replace("-fstack-protector", "").replace("-D_FORTIFY_SOURCE=2", "").replace("-funwind-tables", "").replace("-fasynchronous-unwind-tables", "")
#sysflags = "-mtune=generic -march=x86-64" if get.ARCH() == "x86_64" else "-mtune=generic -march=i686"

### helper functions ###
def removePisiLinuxSection(_dir):
    for root, dirs, files in os.walk(_dir):
        for name in files:
            # FIXME: should we do this only on nonshared or all ?
            # if ("crt" in name and name.endswith(".o")) or name.endswith("nonshared.a"):
            if ("crt" in name and name.endswith(".o")) or name.endswith(".a"):
                i = os.path.join(root, name)
                shelltools.system('objcopy -R ".comment.PISILINUX.OPTs" -R ".note.gnu.build-id" %s' % i)


def setup():
    shelltools.export("LANGUAGE","C")
    shelltools.export("LANG","C")
    shelltools.export("LC_ALL","C")

    shelltools.export("CC", "gcc %s " % defaultflags)
    shelltools.export("CXX", "g++ %s " % defaultflags)

    shelltools.export("CFLAGS", defaultflags)
    shelltools.export("CXXFLAGS", defaultflags)

    shelltools.makedirs("build")
    shelltools.cd("build")
    options = "--prefix=/usr \
               --mandir=/usr/share/man \
               --infodir=/usr/share/info \
               --libexecdir=/usr/lib/misc \
               --with-bugurl=https://bugs.pisilinux.org \
               --enable-add-ons \
               --enable-bind-now \
               --enable-kernel=2.6.32 \
               --enable-stackguard-randomization \
               --without-selinux \
               --without-gd \
               --disable-profile \
               --enable-obsolete-rpc \
               --enable-lock-elision \
               --enable-multi-arch \
               --with-tls"
    if get.buildTYPE() == "emul32":
        options += "\
                    --enable-multi-arch i686-pc-linux-gnu \
                   "

    shelltools.system("../configure %s" % options)

def build():
    shelltools.cd("build")
    if get.buildTYPE() == "emul32":
        shelltools.echo("configparms","build-programs=no")
        shelltools.echo("configparms", "slibdir=/lib32")
        shelltools.echo("configparms", "rtlddir=/lib32")
        shelltools.echo("configparms", "bindir=/tmp32")
        shelltools.echo("configparms", "sbindir=/tmp32")
        shelltools.echo("configparms", "rootsbindir=/tmp32")
        shelltools.echo("configparms", "datarootdir=/tmp32")

        autotools.make()

        pisitools.dosed("configparms", "=no", "=yes")
        shelltools.echo("configparms", "CC += -fstack-protector-strong -D_FORTIFY_SOURCE=2")
        shelltools.echo("configparms", "CXX += -fstack-protector-strong -D_FORTIFY_SOURCE=2")

    else:
        shelltools.echo("configparms", "slibdir=/lib")
        shelltools.echo("configparms", "rtlddir=/lib")

    autotools.make()

def install():
    shelltools.cd("build")

    autotools.rawInstall("install_root=%s" % get.installDIR())
    if get.buildTYPE() == "emul32":
        pisitools.removeDir("/tmp32")

    # Remove our options section from crt stuff
    #removePisiLinuxSection("%s/usr/%s/" % (get.installDIR(), cfg["libdir"]))


### real actions start here ###
#def setup():
    #if multibuild:
        #libcSetup(config["multiarch"])

    #libcSetup(config["system"])


#def build():
    #if multibuild:
        #libcBuild(config["multiarch"])

    #libcBuild(config["system"])


# FIXME: yes fix me
#def check():
#    set_variables(cfg)
#    shelltools.chmod("scripts/begin-end-check.pl")
#
#    shelltools.cd("build")
#
#    shelltools.export("TIMEOUTFACTOR", "16")
#    autotools.make("-k check 2>error.log")


#def install():
    ## we do second arch first, to allow first arch to overwrite headers, etc.
    ## stubs-32.h, elf.h, vm86.h comes only with 32bit
    #if multibuild:
        #libcInstall(config["multiarch"])
        ##pisitools.dosym("../lib32/ld-linux.so.2", "/lib/ld-linux.so.2")
        ## FIXME: these should be added as additional file, when we can define pkg per arch
        #pisitools.dodir("/etc/ld.so.conf.d")
        #shelltools.echo("%s/etc/ld.so.conf.d/60-glibc-32bit.conf" % get.installDIR(), ldconf32bit)

    #libcInstall(config["system"])

    ## localedata can be shared between archs
    #shelltools.cd(config["system"]["builddir"])
    #autotools.rawInstall("install_root=%s localedata/install-locales" % get.installDIR())

    ## now we do generic stuff
    #shelltools.cd(pkgworkdir)

    # We'll take care of the cache ourselves
    if shelltools.isFile("%s/etc/ld.so.cache" % get.installDIR()):
        pisitools.remove("/etc/ld.so.cache")

    # It previously has 0755 perms which was killing things
    #shelltools.chmod("%s/usr/%s/misc/pt_chown" % (get.installDIR(), config["system"]["libdir"]), 04711)

    # Prevent overwriting of the /etc/localtime symlink
    if shelltools.isFile("%s/etc/localtime" % get.installDIR()):
        pisitools.remove("/etc/localtime")

    # Nscd needs this to work
    pisitools.dodir("/var/run/nscd")
    pisitools.dodir("/var/db/nscd")

    # remove zoneinfo files since they are coming from timezone packages
    # we disable timezone build with a patch, keeping these lines for easier maintenance
    if shelltools.isDirectory("%s/usr/share/zoneinfo" % get.installDIR()):
        pisitools.removeDir("/usr/share/zoneinfo")

    #while bootstrapping whole system zic should not be removed. timezone package does not build without it. # 2013
    #for i in ["zdump","zic"]:
        #if shelltools.isFile("%s/usr/sbin/%s" % (get.installDIR(), i)):
            #pisitools.remove("/usr/sbin/%s" % i)

    #pisitools.dodoc("BUGS", "ChangeLog*", "CONFORMANCE", "NAMESPACE", "NEWS", "PROJECTS", "README*", "LICENSES")

