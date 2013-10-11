#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import perlmodules
from pisi.actionsapi import get

def setup():
<<<<<<< HEAD
    autotools.configure('--libexecdir=/usr/lib/xfce4 \
                         --disable-static \
                         --enable-gtk-doc')
=======
    autotools.configure('--prefix=/usr \
                        --libexecdir=/usr/lib/xfce4 \
                        --disable-static \
                        --disable-gtk-doc \
                        --with-perl-options=INSTALLDIRS="vendor" \
                        --disable-debug')

    pisitools.dosed("libtool", "^(hardcode_libdir_flag_spec=).*", '\\1""')
    pisitools.dosed("libtool", "^(runpath_var=)LD_RUN_PATH", "\\1DIE_RPATH_DIE")
    pisitools.dosed("libtool"," -shared ", " -Wl,--as-needed -shared ")
>>>>>>> 9de22661d9cb842ef5d137deafb795148cc692b0

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    
    pisitools.dodoc('AUTHORS', 'ChangeLog', 'NEWS', 'README', 'TODO', 'COPYING')

    # remove unneeded files
    perlmodules.removePodfiles()