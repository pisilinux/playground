#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

#anthome = "/usr/bin/ant"
#javadir = "/usr/lib/jvm/java-7-openjdk"

def build():
   # shelltools.system('find . -name "*.jar" -exec rm -f {} \;')
    shelltools.export("JAVA_HOME","/usr/lib/jvm/java-7-openjdk")
    #shelltools.system("ant")
    shelltools.system("ant -buildfile.xml")

def install():
    pisitools.insinto("/opt/SweetHome3D", "install/SweetHome3D-%s.jar" % get.srcVERSION())
