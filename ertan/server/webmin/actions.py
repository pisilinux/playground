#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

KeepSpecial = ["perl"]

def install():
    shelltools.export("HOME",get.workDIR())
    work_dir = get.workDIR()+"/"+get.srcDIR()
  # shelltools.system("find %s -name '*.cgi' ;find %s -name '*.pl' | perl %s/perlpath.pl /usr/bin/perl -" % (work_dir, work_dir, work_dir))
    shelltools.system("sed -i -e 's/\/usr\/local\/bin\/perl/\/usr\/bin\/perl/g' **/*.cgi")
    shelltools.system("sed -i -e 's/\/usr\/local\/bin\/perl/\/usr\/bin\/perl/g' *.cgi")
    shelltools.system("sed -i -e 's/\/usr\/local\/bin\/perl/\/usr\/bin\/perl/g' **/*.pl")
    shelltools.system("sed -i -e 's/\/usr\/local\/bin\/perl/\/usr\/bin\/perl/g' *.pl")
    pisitools.dodir("/usr/share/webmin-1.550")
    pisitools.dodir("/etc/webmin")
    pisitools.dodir("/var/log/webmin")
    pisitools.dodir("/tmp/.webmin")
    shelltools.export("config_dir", "%s/etc/webmin" % get.installDIR())
    shelltools.export("var_dir", "%s/var/log/webmin" % get.installDIR())
    shelltools.export("perl", "/usr/bin/perl")
    shelltools.export("autoos", "1")
    shelltools.export("port", "10000")
    shelltools.export("login", "root")
    shelltools.export("crypt", "XXX")
    shelltools.export("host", "$HOSTNAME")
    shelltools.export("ssl", "1")
    shelltools.export("atboot", "1")
    shelltools.export("nostart", "1")
    shelltools.export("nochown", "1")
    shelltools.export("autothird","1")
    shelltools.export("nouninstall", "1")
    shelltools.export("noperlpath","1")
    shelltools.export("nopostinstall","")
    shelltools.export("tempdir", "%s/tmp/.webmin" % get.installDIR())
    shelltools.system("./setup.sh %s/usr/share/webmin-1.620"  % get.installDIR())
    
    pisitools.dosed("%s/etc/webmin/install-dir" % get.installDIR(),get.installDIR()+"/", "/")
    pisitools.dosed("%s/etc/webmin/miniserv.conf" % get.installDIR(),get.installDIR()+"/", "/")
    pisitools.dosed("%s/etc/webmin/reload" % get.installDIR(),get.installDIR()+"/", "/")
    pisitools.dosed("%s/etc/webmin/restart" % get.installDIR(),get.installDIR()+"/", "/")
    pisitools.dosed("%s/etc/webmin/start" % get.installDIR(),get.installDIR()+"/", "/")
    pisitools.dosed("%s/etc/webmin/stop" % get.installDIR(),get.installDIR()+"/", "/")
    pisitools.dosed("%s/etc/webmin/var-path" % get.installDIR(),get.installDIR()+"/", "/")
    file=open("/etc/shadow", "r")
    shadow=file.readline()
    file.close()
    shadow=shadow.split(":")
    pisitools.dosed("%s/etc/webmin/miniserv.users" % get.installDIR(), "root:XXX","root:%s" % shadow[1])
#   shelltools.system("sed -i -e 's/root:XXX/root:%s/' '%s/etc/webmin/miniserv.users'" % (shadow[1], get.installDIR()))
