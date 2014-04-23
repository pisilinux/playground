#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def install():
    shelltools.makedirs("%s/usr/bin" % get.installDIR())
    shelltools.makedirs("%s/usr/share/java/maven" % get.installDIR())
    shelltools.makedirs("%s/etc/maven" % get.installDIR())
    shelltools.system(". /etc/profile.d/jre.sh")
    shelltools.system(". /etc/profile.d/jdk.sh")
    shelltools.system("sed '42i\   <property name=\"maven.home\" value=\"%s/usr/share/maven-%s\"/>' build.xml > build2.xml" % (get.installDIR(), get.srcVERSION()))
    shelltools.system("mv build2.xml build.xml")
    shelltools.system("export PATH=$PATH:$maven.home/bin")
    shelltools.system("export MAVEN_OPTS=-Xmx512m")
    shelltools.system("ant -Dmaven.repo.local=%s/usr/share/maven-%s/repo" % (get.installDIR(), get.srcVERSION()))
    shelltools.system("mv %s/usr/share/maven-%s/bin/mvn %s/usr/bin" % (get.installDIR(), get.srcVERSION(), get.installDIR()))
    shelltools.system("mv %s/usr/share/maven-%s/bin/mvnDebug %s/usr/bin" % (get.installDIR(), get.srcVERSION(), get.installDIR()))
    shelltools.system("mv %s/usr/share/maven-%s/lib/* %s/usr/share/java/maven" % (get.installDIR(), get.srcVERSION(), get.installDIR()))
    shelltools.system("mv %s/usr/share/maven-%s/boot/* %s/usr/share/java/maven" % (get.installDIR(), get.srcVERSION(), get.installDIR()))
    shelltools.system("mv %s/usr/share/maven-%s/conf/* %s/etc/maven" % (get.installDIR(), get.srcVERSION(), get.installDIR()))
    shelltools.system("mv %s/usr/share/maven-%s/bin/m2.conf %s/etc/maven" % (get.installDIR(), get.srcVERSION(), get.installDIR()))
    shelltools.system("rm -rf %s/usr/share/maven-%s" % (get.installDIR(), get.srcVERSION()))

