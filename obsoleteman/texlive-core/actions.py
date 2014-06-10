# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

import os
from distutils.dir_util import copy_tree

WorkDir = "."
pkgname="texlive-core"
pkgver="2013.33063"

def setup():
    # Unpack and prepare files
    for tar_file in shelltools.ls(get.workDIR()):
        if tar_file.endswith("xz"):
            shelltools.system("tar Jxfv %s" % tar_file)

def build():
    for folder in ["tlpkg", "doc", "source"]:
        shelltools.unlinkDir(folder)

def install():
    # prepare and install installed packs list
    pisitools.dodir("/var/lib/texmf/pisilinux/installedpacks")
    shelltools.system('sed -i "/^#/d" CONTENTS')
    shelltools.copy("CONTENTS", "%s/var/lib/texmf/pisilinux/installedpacks/" % get.installDIR())
    pisitools.rename("/var/lib/texmf/pisilinux/installedpacks/CONTENTS", "texlive-core-%s.list" % pkgver)
    shelltools.chmod("%s/var/lib/texmf/pisilinux/installedpacks/" % get.installDIR(), 0644)
    pisitools.dodir("/usr/share")

    wanteddirs = []
    for dirs in shelltools.ls(get.workDIR()):
        if shelltools.isDirectory(dirs) and not "texmf" in dirs:
            wanteddirs.append(dirs)

    for folder in wanteddirs:
        pisitools.insinto("/usr/share/texmf-dist", folder)

    if shelltools.can_access_directory("texmf-dist"):
        ## Recursively copy on directory on top of another, overwrite duplicate files too
        copy_tree("texmf-dist", "%s/usr/share/texmf-dist" % get.installDIR())

    ### chmod of script files
    script_dir = get.installDIR() + "/usr/share/texmf-dist/scripts"
    if shelltools.can_access_directory(script_dir):
        for root, dirs, files in os.walk(script_dir):
            for name in files:
                shelltools.chmod(os.path.join(root, name), 0755)

    ### copy config file to texmf-config ??
    pisitools.dodir("/etc/texmf/tex/context/config")
    shelltools.copy("%s/usr/share/texmf-dist/tex/context/config/cont-usr.tex" % get.installDIR(), \
                     "%s/etc/texmf/tex/context/config/cont-usr.tex" % get.installDIR())

 ## ??
    ## old packages, we will not provide them
    #pisitools.remove("/usr/share/texmf-dist/tex/plain/config/omega.ini")
    #pisitools.remove("/usr/share/texmf-dist/tex/plain/config/aleph.ini")
    #pisitools.removeDir("/usr/share/texmf-dist/scripts/context/stubs/mswin/")

    pisitools.removeDir("/usr/share/texmf-dist/doc/man")