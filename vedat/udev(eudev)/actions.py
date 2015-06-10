#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import libtools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

suffix = "32" if get.buildTYPE() == "emul32" else ""

def setup():
    autotools.autoreconf("-fi")
    libtools.libtoolize("--force")

  
    options = " ac_cv_header_sys_capability_h=yes \
                --bindir=/sbin%s \
                --sbindir=/sbin%s \
                --docdir=/usr/share/doc/udev \
                --libdir=/usr/lib%s \
                --libexecdir=/lib%s/udev \
                --with-firmware-path=/lib%s/firmware/updates:/lib%s/firmware \
                --with-html-dir=/usr/share/doc/udev/html \
                --with-rootlibdir=/lib%s \
                --with-rootprefix= \
                --disable-selinux \
                --enable-gudev \
                --enable-shared \
                --disable-static \
                --enable-split-usr \
                --disable-gtk-doc-html \
                --enable-rule_generator \
                --with-modprobe=/sbin/modprobe \
                --enable-keymap \
                --enable-blkid \
                --enable-split-usr \
                --disable-manpages \
               " % ((suffix, )*7)

    options += "\
                --disable-static \
                --disable-gtk-doc \
                --enable-introspection=no \ \
               " if get.buildTYPE() == "emul32" else \
               "\
                --enable-static \
                --enable-libkmod \
                --enable-introspection=yes \
               "
   
    autotools.configure(options)

def build():
    pisitools.dosed("libtool", " -shared ", " -Wl,-O1,--as-needed -shared ")
    
    autotools.make()

def install():

    autotools.rawInstall("-j1 DESTDIR=%s%s" % (get.installDIR(), suffix))
    if get.buildTYPE() == "emul32":
        shelltools.move("%s%s/lib%s" % (get.installDIR(), suffix, suffix), "%s/lib%s" % (get.installDIR(), suffix))
        shelltools.move("%s%s/usr/lib%s" % (get.installDIR(), suffix, suffix), "%s/usr/lib%s" % (get.installDIR(), suffix))
        for f in shelltools.ls("%s/usr/lib32/pkgconfig" % get.installDIR()):
             pisitools.dosed("%s/usr/lib32/pkgconfig/%s" % (get.installDIR(), f), "emul32", "usr")
        return
      
    # Create vol_id and scsi_id symlinks in /sbin probably needed by multipath-tools
    pisitools.dosym("/lib/udev/scsi_id", "/sbin/scsi_id")

    # Create /etc/udev/rules.d for backward compatibility
    pisitools.dodir("/etc/udev/rules.d")

    pisitools.dodir("/run/udev")
    pisitools.dodoc("README")

    # Add man files
    #pisitools.doman("man/systemd.link.5", "man/udev.7", "man/udevadm.8", "man/systemd-udevd.service.8")
