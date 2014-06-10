# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

WorkDir = "."
revnr = get.srcVERSION().split(".")[1]

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
    pisitools.dosed("CONTENTS", "^#", deleteLine=True)
    pisitools.insinto("/var/lib/texmf/pisilinux/installedpacks", "CONTENTS", "%s_%s.list" % (get.srcNAME(), revnr))

    for i in shelltools.ls("texmf-dist"):
        shelltools.copytree("texmf-dist/%s/" % i, "%s/usr/share/texmf-dist/" % get.installDIR())
    shelltools.system("find texmf-dist -type f -executable -exec chmod 755 %s/usr/share/{} \;" % get.installDIR())

    for i in shelltools.ls("."):
        if shelltools.isDirectory(i) and not i.startswith("texmf"):
            shelltools.copytree(i, "%s/usr/share/texmf-dist/" % get.installDIR())
    --end--

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