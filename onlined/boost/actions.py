# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools

def build():
    shelltools.system("./bootstrap.sh --with-toolset=gcc --with-icu --with-python=/usr/bin/python2")
    shelltools.echo("%s/boost_1_57_0/project-config.jam" % get.workDIR(),"using python : 2.7 : /usr/bin/python ; ")
    shelltools.echo("%s/boost_1_57_0/project-config.jam" % get.workDIR(),"using python : 3.4 : /usr/bin/python3 : /usr/include/python3.4mu : /usr/lib ;")
    shelltools.echo("%s/boost_1_57_0/project-config.jam" % get.workDIR(),"using mpi ;")

def install():
    #pisitools.dodir("/usr")
    #shelltools.system("./b2 install --prefix=%s/usr" % get.installDIR());
    pisitools.dohtml("doc/html/*")