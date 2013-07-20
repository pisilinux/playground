#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

WorkDir = "."
WorkDir_PicasaInstallDir = ""+ get.workDIR() +"/opt/google/picasa/3.0/wine/drive_c/Program Files/Google/Picasa3/"

def setup():
    shelltools.system("rpm2targz -v %s/picasa-3.9-2pclos2012.src.rpm" %get.workDIR())
    #shelltools.system("tar xfvz %s/picasa-3.9-2pclos2012.src.tar.gz --exclude=usr --exclude=opt/kde3 --exclude=opt/google/picasa/3.0/wine/drive_c/Program\ Files/Google/Picasa3" %get.workDIR())
    shelltools.system("tar xfvz %s/picasa-3.9-2pclos2012.src.tar.gz" %get.workDIR())
    shelltools.system("tar xJvf %s/picasa.tar.xz" %get.workDIR())

    shelltools.chmod("%s/picasa/3.0/bin/*" %get.workDIR())
    shelltools.chmod("%s/picasa/3.0/bin/*" %get.workDIR())

def install():
#    pisitools.dosed("opt/google/picasa/3.0/bin/repackage32.sh","if [ \"`uname -m`\" != \"x86_64\" ] ; then","if [ \"`uname -m`\" = \"x86_64\" ] ; then" %get.installDIR())
    pisitools.dosed("picasa/3.0/bin/repackage32.sh"," != "," = ")
    pisitools.insinto("opt/google/picasa", "picasa/*")

    pisitools.dosym("/opt/google/picasa/3.0/bin/picasa", "/usr/bin/picasa")
    pisitools.dosym("/opt/google/picasa/3.0/lib/npPicasa3.so", "/usr/lib/browser-plugins/npPicasa3.so")

    pisitools.dodoc("picasa/3.0/README", "picasa/3.0/LICENSE.FOSS")