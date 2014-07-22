# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
#    shelltools.chmod("hw/vnc/symlink-vnc.sh")

    #autotools.autoreconf("-fiv")
    autotools.configure("--prefix=/usr \
                         --localstatedir=/var \
                         --enable-install-libxf86config \
                         --enable-aiglx \
                         --enable-glx-tls \
                         --enable-composite \
                         --enable-xcsecurity \
                         --enable-record \
                         --enable-dri \
                         --enable-dri2 \
                         --enable-config-udev \
                         --disable-config-hal \
                         --enable-xfree86-utils \
                         --enable-xorg \
                         --enable-dmx \
                         --enable-xvfb \
                         --disable-xnest \
                         --enable-kdrive \
                         --enable-kdrive-evdev \
                         --enable-kdrive-kbd \
                         --enable-kdrive-mouse \
                         --enable-xephyr \
                         --disable-xfake \
                         --disable-xfbdev \
                         --disable-devel-docs \
                         --disable-static \
                         --without-doxygen \
                         --with-pic \
                         --without-dtrace \
                         --with-int10=x86emu \
                         --with-os-name=\"PisiLinux\" \
                         --with-os-vendor=\"Pisi GNU/Linux Community\" \
                         --with-builderstring=\"Package: %s\" \
                         --with-fontrootdir=/usr/share/fonts \
                         --with-default-font-path=catalogue:/etc/X11/fontpath.d,built-ins \
                         --with-xkb-output=/var/lib/xkb \
                         --with-dri-driver-path=/usr/lib/xorg/modules/dri \
                         --without-xmlto \
                         --without-fop \      
                         --enable-install-setuid  \
                         --enable-suid-wrapper  \          
                         PCI_TXT_IDS_DIR=/usr/share/X11/pci \
                         XSERVERCFLAGS_LIBS=-L/usr/lib \
                         XSERVERCFLAGS_CFLAGS=-I/usr/include  \
                         PKG_CONFIG_PATH=/usr/lib/pkgconfig \
                         " % get.srcTAG())
    
    pisitools.dosed("libtool", " -shared ", " -Wl,-O1,--as-needed -shared ")
    pisitools.dosed("hw/xfree86/dri/dri.h", "xf86dri.h", "X11/dri/xf86dri.h")
    #pisitools.dosed("include/inputstr.h", "pixman.h", "pixman-1/pixman.h")
    #pisitools.dosed("dix/devices.c", "pixman.h", "pixman-1/pixman.h")
    #pisitools.dosed("dix/main.c", "pixman.h", "pixman-1/pixman.h")
    #pisitools.dosed("dix/getevents.c", "pixman.h", "pixman-1/pixman.h")
    #pisitools.dosed("dix/region.c", "pixman.h", "pixman-1/pixman.h")
    
def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodir("/etc/X11/fontpath.d")
    pisitools.dodir("/etc/X11/xorg.conf.d")
    pisitools.dodir("/usr/share/X11/pci")
    pisitools.dodir("/usr/share/X11/xorg.conf.d")

    # Remove empty dir
    pisitools.removeDir("/var/log")

    pisitools.dodoc("COPYING", "README")
