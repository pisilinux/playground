#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    shelltools.system("./autogen.sh")
    shelltools.system("sed -i -e 's:getgroups:lightdm_&:' tests/src/libsystem.c")

    autotools.configure("--disable-static \
                         --disable-gtk-doc \
                         --enable-liblightdm-qt \
                         --disable-liblightdm-qt5 \
                         --enable-introspection \
                         --disable-tests \
                         --disable-systemd \
                         --with-greeter-user=lightdm \
                         --with-greeter-session=lightdm-gtk-greeter")

def build():
    autotools.make()

def install():
    pisitools.dodir("/var/cache/lightdm")
    shelltools.chmod("%s/var/cache/lightdm" % get.installDIR(),0755)

    pisitools.dodir("/var/lib/lightdm")
    shelltools.chmod("%s/var/lib/lightdm" % get.installDIR(), 0770)

    pisitools.dodir("/var/log/lightdm")
    shelltools.chmod("%s/var/log/lightdm"  % get.installDIR(),0711)

    shelltools.echo("%s/var/lib/lightdm/.pam_environment" % get.installDIR(), "GDK_CORE_DEVICE_EVENTS=true")
    shelltools.chmod("%s/var/lib/lightdm/.pam_environment" % get.installDIR(), 0644)

    shelltools.chmod("%s/var/lib/lightdm" % get.installDIR(), 0770)

    pisitools.dodir("/usr/share/polkit-1/rules.d")

    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    shelltools.chmod("%s/usr/share/polkit-1/rules.d"  % get.installDIR(), 0700)
    pisitools.removeDir("/etc/apparmor.d")

