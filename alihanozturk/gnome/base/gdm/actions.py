#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.autoreconf("-fi")
    shelltools.system("intltoolize -f")
    autotools.configure("--enable-split-authentication \
                         --enable-profiling \
                         --enable-console-helper \
                         --disable-scrollkeeper \
                         --with-default-pam-config=pisilinux
                         --with-console-kit \
                         --without-systemd \
                         --with-plymouth \
                         --with-at-spi-registryd-directory=/usr/libexec \
                         --with-dbus-services=/usr/share/dbus-1/services \
                         --with-gnome-settings-daemon-directory=/usr/libexec \
                         --with-check-accelerated-directory=/usr/libexec \
                         --with-authentication-agent-directory=/usr/libexec \
                         --with-run-dir=/run/gdm ")

    pisitools.dosed("libtool", "( -shared )", " -Wl,-O1,--as-needed\\1")
    pisitools.dosed("libtool", '(    if test "\$export_dynamic" = yes && test -n "\$export_dynamic_flag_spec"; then)', '      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\\1')

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING*", "NEWS", "README")