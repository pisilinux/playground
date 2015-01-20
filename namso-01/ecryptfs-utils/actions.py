#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.
#
# nut is done with checkouts from
# svn://svn.mplayerhq.hu/nut/src/trunk

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    shelltools.touch("ecryptfs.conf")
    shelltools.echo("ecryptfs.conf", "# ecryptfs module is needed before ecryptfs mount, so mount helper can \n# check for file name encryption support\necryptfs")
    autotools.autoreconf("-fiv")
    autotools.configure("--prefix=/usr --sbindir=/usr/bin --enable-nss --enable-pkcs11-helper --enable-tests PYTHON=python2.7")
    
    pisitools.dosed("src/desktop/ecryptfs-mount-private.desktop.in", "Type=Application", "Type=Application\nEncoding=UTF-8\nIcon=/usr/share/pixmaps/ecryptfs-mount-private.png")
    pisitools.dosed("src/desktop/ecryptfs-setup-private.desktop.in", "Type=Application", "Type=Application\nEncoding=UTF-8\nIcon=/usr/share/pixmaps/ecryptfs-mount-private.png")
    
    #disable rpath
    shelltools.system("sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool")
    shelltools.system("sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool")

def build():
    autotools.make()
    
def install():
    autotools.rawInstall("DESTDIR=%s INSTALL_ROOT=%s" %(get.installDIR(), get.installDIR()))
    
    pisitools.dopixmaps("ecryptfs-mount-private.png")
    
    pisitools.insinto("/usr/lib/modules-load.d/", "ecryptfs.conf")
    
    pisitools.dodoc("COPYING", "README*")