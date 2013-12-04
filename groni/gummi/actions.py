# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.util import run_batch

def setup():
    cat = run_batch("cat data/misc/gummi.desktop.in | grep Categories=")[1].split('=')[1].strip()
    for it in ['GTK', 'GNOME']:
        if not it in cat:
            cat = "%s;%s" % (it, cat)
            pisitools.dosed('data/misc/gummi.desktop.in', '^(Categories=).*', r'\1%s' % cat)
    autotools.configure()

def build():
    autotools.make()

def install():
    autotools.install()
    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING", "README")
