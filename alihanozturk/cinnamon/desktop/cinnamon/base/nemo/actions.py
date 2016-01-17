#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    pisitools.dosed("data/merge_action_strings", "#!/usr/bin/python2", "#!/usr/bin/python")
    pisitools.dosed("data/extract_action_strings", "#!/usr/bin/python2", "#!/usr/bin/python")
    shelltools.export("PYTHON", "/usr/bin/python2.7")
    shelltools.system("./autogen.sh")
    autotools.configure("--libexecdir=/usr/lib/nemo \
                         --prefix=/usr \
                         --sysconfdir=/etc \
                         --disable-update-mimedb \
                         --disable-tracker \
                         --disable-schemas-compile \
                         --disable-gtk-doc-html \
                         --enable-gtk-doc")
    
    pisitools.dosed("libtool"," -shared ", " -Wl,--as-needed -shared ")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("README", "AUTHORS")