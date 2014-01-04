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

def setup():
    # Unpack and prepare files
    for tar_file in shelltools.ls(get.workDIR()):
        if tar_file.endswith("xz"):
            shelltools.system("tar Jxfv %s" % tar_file)

def build():
    for folder in ["tlpkg", "doc", "source", "omega"]:
        shelltools.unlinkDir("%s/%s" %(get.workDIR() , folder))

def install():
    #install
    pisitools.dodir("/usr/share")

    wanteddirs = []
    for file_ in shelltools.ls(get.workDIR()):
        if shelltools.isDirectory(file_) and not "texmf" in file_:
            wanteddirs.append(file_)

    for folder in wanteddirs:
        pisitools.insinto("/usr/share/texmf-dist", folder)

    if shelltools.can_access_directory("texmf-dist"):
        # Recursively copy on directory on top of another, overwrite duplicate files too
        copy_tree("texmf-dist", "%s/usr/share/texmf-dist" % get.installDIR())

    ## chmod of script files
    script_dir = get.installDIR() + "/usr/share/texmf-dist/scripts"
    if shelltools.can_access_directory(script_dir):
        for root, dirs, files in os.walk(script_dir):
            for name in files:
                shelltools.chmod(os.path.join(root, name), 0755)

#    # copy config file to texmf-config
#    pisitools.dodir("/etc/texmf/tex/context/config")
#    shelltools.copy("%s/usr/share/texmf-dist/tex/context/config/cont-usr.tex" % get.installDIR(), \
#                    "%s/etc/texmf/tex/context/config/cont-usr.tex" % get.installDIR())

    # old packages, we will not provide them
    pisitools.remove("/usr/share/texmf-dist/tex/plain/config/omega.ini")
    pisitools.remove("/usr/share/texmf-dist/tex/plain/config/aleph.ini")
    pisitools.removeDir("/usr/share/texmf-dist/scripts/context/stubs/mswin/")
    
    # install texmf tree
    folders = ["/usr/share",
               "/etc/texmf/web2c",
               "/etc/texmf/chktex",
               "/etc/texmf/dvips/config",
               "/etc/texmf/dvipdfm/config",
               "/etc/texmf/dvipdfmx",
               "/etc/texmf/tex/generic/config",
               "/etc/texmf/ttf2pk",
               "/etc/texmf/xdvi",
               "/etc/fonts/conf.avail"]

    for dirs in folders:
        pisitools.dodir(dirs)

    #pisitools.insinto("/usr/share", "texmf")
    pisitools.insinto("/etc/fonts/conf.avail/", "09-texlive-fonts.conf")

    # replace upstream texmf.cnf with ours
    pisitools.remove("/usr/share/texmf-dist/web2c/texmf.cnf")
    pisitools.insinto("/etc/texmf/web2c/", "texmf.cnf")

    # the location of texmf.cnf is hard-wired to be under /usr/share/texmf/web2c
    # we make a symlink from /etc/texmf/web2c/texmf.cnf to the latter
    pisitools.dosym("/etc/texmf/web2c/texmf.cnf", "/usr/share/texmf-dist/web2c/texmf.cnf")
    
    # copy config files to $TEXMFSYSCONFIG tree (defined in texmf.cnf)
    config_files = [ "/usr/share/texmf-dist/chktex/chktexrc",
                     "/usr/share/texmf-dist/web2c/mktex.cnf",
                     "/usr/share/texmf-dist/web2c/updmap.cfg",
                     "/usr/share/texmf-dist/web2c/fmtutil.cnf",
                     "/usr/share/texmf-dist/dvips/config/config.ps",
                     "/usr/share/texmf-dist/dvipdfmx/dvipdfmx.cfg",
                     "/usr/share/texmf-dist/tex/generic/config/pdftexconfig.tex",
                     "/usr/share/texmf-dist/tex/generic/config/language.dat",
                     "/usr/share/texmf-dist/tex/generic/config/language.def",
                     "/usr/share/texmf-dist/ttf2pk/ttf2pk.cfg",
                     "/usr/share/texmf-dist/xdvi/XDvi"]

    for share_file in config_files:
        etc_file = share_file.replace("/usr/share/texmf-dist", "/etc/texmf")
        shelltools.copy("%s/%s" % (get.installDIR(), share_file) , "%s/%s" % (get.installDIR(), etc_file))

    # clean updmap.cfg
    pisitools.dosed("%s/etc/texmf/web2c/updmap.cfg" % get.installDIR(), "^(Map|MixedMap).*$")
    pisitools.dosed("%s/etc/texmf/web2c/updmap.cfg" % get.installDIR(), "^#! (Map|MixedMap).*$")
    
    # remove aleph from fmtutil.cnf
    pisitools.dosed("%s/usr/share/texmf-dist/web2c/fmtutil.cnf" % get.installDIR(), "^.*aleph.*$")
