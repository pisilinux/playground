#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

import os
from pisi.actionsapi import get
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

shelltools.export("ALT_PARALLEL_COMPILE_JOBS", get.makeJOBS())
shelltools.export("HOTSPOT_BUILD_JOBS", get.makeJOBS())
shelltools.export("LC_ALL", "C")

bindir = "/usr/bin"
jre7lib = "/usr/lib/jvm/java-7-openjdk/jre/lib/amd64/"
jvmbindir = "/usr/lib/jvm/java-7-openjdk/bin/"
jreheadless = "/etc/java-7-openjdk/"

def setup():
    autotools.rawConfigure("\
                            --disable-tests \
                            --disable-Werror \
                            --disable-downloading \
                            --with-parallel-jobs=%s \
                            --with-jdk-home=/opt/sun-jdk \
                            --enable-pulse-java \
                            --enable-nss \
                            --with-rhino \
                            --disable-bootstrap \
                            --with-jdk-src-zip=7958751eb9ef.tar.gz \
                            --with-jaxp-src-zip=8f220f7b51c7.tar.gz \
                            --with-corba-src-zip=8ed5df839fbc.tar.gz \
                            --with-jaxws-src-zip=652eb396f959.tar.gz  \
                            --with-openjdk-src-zip=e2f5917da3c1.tar.gz \
                            --with-hotspot-src-zip=b59e02d9e72b.tar.gz  \
                            --with-langtools-src-zip=3c8eb52a32ea.tar.gz \
                            --with-abs-install-dir=/usr/lib/jvm/java-7-openjdk \
                            --with-pkgversion='PisiLinux build 7.u45_2.4.3-1' \
                           " % get.makeJOBS().replace("-j", ""))

def build():
    autotools.make()

def check():
    autotools.make("check -k")

def install():
    #files for jdk7-openjdk
    for files in ["bootstrap/jdk1.6.0/bin/jar", "bootstrap/jdk1.6.0/bin/xjc", "bootstrap/jdk1.6.0/bin/apt", "bootstrap/jdk1.6.0/bin/jdb", "bootstrap/jdk1.6.0/bin/jps", "bootstrap/jdk1.6.0/bin/jmap", "bootstrap/jdk1.6.0/bin/idlj", "bootstrap/jdk1.6.0/bin/jcmd", "bootstrap/jdk1.6.0/bin/jhat", "bootstrap/jdk1.6.0/bin/rmic", "bootstrap/jdk1.6.0/bin/jstat", "bootstrap/jdk1.6.0/bin/javac", "bootstrap/jdk1.6.0/bin/javah", "bootstrap/jdk1.6.0/bin/javap", "bootstrap/jdk1.6.0/bin/jinfo", "bootstrap/jdk1.6.0/bin/wsgen", "bootstrap/jdk1.6.0/bin/jstat", "bootstrap/jdk1.6.0/bin/jstack", "bootstrap/jdk1.6.0/bin/jstatd", "bootstrap/jdk1.6.0/bin/javadoc", "bootstrap/jdk1.6.0/bin/extcheck", "bootstrap/jdk1.6.0/bin/jconsole", "bootstrap/jdk1.6.0/bin/wsimport", "bootstrap/jdk1.6.0/bin/jarsigner", "bootstrap/jdk1.6.0/bin/jsadebugd", "bootstrap/jdk1.6.0/bin/schemagen", "bootstrap/jdk1.6.0/bin/serialver", "bootstrap/jdk1.6.0/bin/jrunscript", "bootstrap/jdk1.6.0/bin/appletviewer", "bootstrap/jdk1.6.0/bin/native2ascii"]:
        pisitools.insinto(bindir, files)
    
    for files in ["openjdk.build/j2sdk-image/bin/appletviewer", "openjdk.build/j2sdk-image/bin/jarsigner", "openjdk.build/j2sdk-image/bin/javap", "openjdk.build/j2sdk-image/bin/jhat", "openjdk.build/j2sdk-image/bin/jsadebugd", "openjdk.build/j2sdk-image/bin/native2ascii", "openjdk.build/j2sdk-image/bin/rmid", "openjdk.build/j2sdk-image/bin/tnameserv", "openjdk.build/j2sdk-image/bin/apt", "openjdk.build/j2sdk-image/bin/java", "openjdk.build/j2sdk-image/bin/java-rmi.cgi", "openjdk.build/j2sdk-image/bin/jinfo", "openjdk.build/j2sdk-image/bin/jstack", "openjdk.build/j2sdk-image/bin/orbd", "openjdk.build/j2sdk-image/bin/rmiregistry", "openjdk.build/j2sdk-image/bin/unpack200", "openjdk.build/j2sdk-image/bin/extcheck", "openjdk.build/j2sdk-image/bin/javac", "openjdk.build/j2sdk-image/bin/jcmd", "openjdk.build/j2sdk-image/bin/jmap", "openjdk.build/j2sdk-image/bin/jstat", "openjdk.build/j2sdk-image/bin/pack200", "openjdk.build/j2sdk-image/bin/schemagen", "openjdk.build/j2sdk-image/bin/wsgen", "openjdk.build/j2sdk-image/bin/idlj", "openjdk.build/j2sdk-image/bin/javadoc", "openjdk.build/j2sdk-image/bin/jconsole", "openjdk.build/j2sdk-image/bin/jps", "openjdk.build/j2sdk-image/bin/jstatd", "openjdk.build/j2sdk-image/bin/policytool", "openjdk.build/j2sdk-image/bin/serialver", "openjdk.build/j2sdk-image/bin/wsimport", "openjdk.build/j2sdk-image/bin/jar", "openjdk.build/j2sdk-image/bin/javah", "openjdk.build/j2sdk-image/bin/jdb", "openjdk.build/j2sdk-image/bin/jrunscript", "openjdk.build/j2sdk-image/bin/keytool", "openjdk.build/j2sdk-image/bin/rmic", "openjdk.build/j2sdk-image/bin/servertool", "openjdk.build/j2sdk-image/bin/xjc"]:
        pisitools.insinto(jvmbindir, files)
    
    pisitools.insinto("/usr/lib/jvm/java-7-openjdk/lib/", "openjdk.build/j2sdk-image/lib/*")
    
    pisitools.insinto("/usr/lib/jvm/java-7-openjdk/include/", "openjdk.build/include/*")
    pisitools.insinto("/usr/share/applications/", "jconsole.desktop")
    pisitools.insinto("/usr/share/man/ja/", "openjdk.build/j2sdk-image/man/ja_JP.UTF-8/*")
    pisitools.insinto("/usr/share/man/man1/", "openjdk.build/j2sdk-image/man/man1/*")
    
    #files for openjdk7-src
    pisitools.insinto("/usr/lib/jvm/java-7-openjdk/", "openjdk.build/j2sdk-image/src.zip")
    
    #files for openjdk7-doc
    pisitools.insinto("/usr/share/doc/openjdk7-doc/", "openjdk.build/docs/*")
    
    #for files jre7-openjdk
    pisitools.dobin("openjdk.build/j2re-image/bin/policytool")
    pisitools.insinto("/usr/share/applications/", "policytool.desktop")
    pisitools.insinto("usr/lib/jvm/java-7-openjdk/jre/bin/", "openjdk.build/j2re-image/bin/policytool")
    for files in ["openjdk.build/j2re-image/lib/amd64/libjsoundalsa.so", "openjdk.build/j2re-image/lib/amd64/libpulse-java.so", "openjdk.build/j2re-image/lib/amd64/libsplashscreen.so", "openjdk.build/j2re-image/lib/amd64/xawt/libmawt.so"]:
        pisitools.insinto(jre7lib, files)
        
    pisitools.dodoc("openjdk.build/j2re-image/THIRD_PARTY_README", "openjdk.build/j2re-image/LICENSE")
    pisitools.doman("openjdk.build/j2re-image/man/man1/policytool.1")
    pisitools.insinto("/usr/share/man/ja/man1/", "openjdk.build/j2re-image/man/ja_JP.UTF-8/man1/policytool.1")
    pisitools.insinto("/usr/share/icons/hicolor/16x16/apps/", "openjdk/jdk/src/solaris/classes/sun/awt/X11/java-icon16.png", "java.png")
    pisitools.insinto("/usr/share/icons/hicolor/24x24/apps/", "openjdk/jdk/src/solaris/classes/sun/awt/X11/java-icon24.png", "java.png")
    pisitools.insinto("/usr/share/icons/hicolor/32x32/apps/", "openjdk/jdk/src/solaris/classes/sun/awt/X11/java-icon32.png", "java.png")
    pisitools.insinto("/usr/share/icons/hicolor/48x48/apps/", "openjdk/jdk/src/solaris/classes/sun/awt/X11/java-icon48.png", "java.png")
    
    #for files jre7-openjdk-headless
    for files in ["openjdk.build/j2sdk-image/jre/lib/calendars.properties", "openjdk.build/j2sdk-image/jre/lib/content-types.properties", "openjdk.build/j2sdk-image/jre/lib/flavormap.properties", "openjdk.build/j2sdk-image/jre/lib/amd64/jvm.cfg", "openjdk.build/j2sdk-image/jre/lib/logging.properties", "openjdk.build/j2sdk-image/jre/lib/net.properties", "openjdk.build/j2sdk-image/jre/lib/psfont.properties.ja", "openjdk.build/j2sdk-image/jre/lib/psfontj2d.properties", "openjdk.build/j2sdk-image/jre/lib/tz.properties", "openjdk.build/j2sdk-image/jre/lib/sound.properties"]:
        pisitools.insinto(jreheadless, files)
    
    pisitools.insinto("/etc/java-7-openjdk/cursors/", "openjdk.build/j2sdk-image/jre/lib/images/cursors/cursors.properties")
    pisitools.insinto("/etc/java-7-openjdk/management/", "openjdk.build/j2sdk-image/jre/lib/management/jmxremote.access")
    pisitools.insinto("/etc/java-7-openjdk/management/", "openjdk.build/j2sdk-image/jre/lib/management/management.properties")
    pisitools.insinto("/etc/java-7-openjdk/management/", "openjdk.build/j2sdk-image/jre/lib/management/jmxremote.password.template", "jmxremote.password")
    pisitools.insinto("/etc/java-7-openjdk/management/", "openjdk.build/j2sdk-image/jre/lib/management/snmp.acl.template", "snmp.acl")
    
    pisitools.insinto("/etc/java-7-openjdk/security/", "openjdk.build/j2sdk-image/jre/lib/security/java.policy")
    pisitools.insinto("/etc/java-7-openjdk/security/", "openjdk.build/j2sdk-image/jre/lib/security/java.security")
    pisitools.insinto("/etc/java-7-openjdk/security/", "openjdk.build/j2sdk-image/jre/lib/security/nss.cfg")
    
    pisitools.insinto("/usr/share/doc/jre7-openjdk-headless", "openjdk.build/j2sdk-image/jre/LICENSE")
    pisitools.insinto("/usr/share/doc/jre7-openjdk-headless", "openjdk.build/j2sdk-image/jre/THIRD_PARTY_README")
    pisitools.insinto("/usr/share/doc/jre7-openjdk-headless", "openjdk.build/j2sdk-image/jre/ASSEMBLY_EXCEPTION")
    
    pisitools.insinto("/usr/lib/jvm/java-7-openjdk/jre/bin/", "openjdk.build/j2sdk-image/jre/bin/*")
    pisitools.insinto("/usr/bin/", "openjdk.build/j2sdk-image/jre/bin/*")
    
    pisitools.insinto("/usr/lib/jvm/java-7-openjdk/jre/lib/", "openjdk.build/j2re-image/lib/*")
        
    pisitools.insinto("/etc/java-7-openjdk/", "openjdk.build/j2sdk-image/jre/lib/fontconfig.Ubuntu.properties.src", "fontconfig.properties")    
    pisitools.insinto("/etc/java-7-openjdk/", "openjdk.build/j2sdk-image/jre/lib/fontconfig.Ubuntu.bfc", "fontconfig.bfc")
    
    pisitools.doman("openjdk.build/j2re-image/man/man1/*")
    pisitools.insinto("/usr/share/man/ja/man1", "openjdk.build/j2re-image/man/ja_JP.UTF-8/man1/*.1")
    
    
    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING", "HACKING", "README", "NEWS")