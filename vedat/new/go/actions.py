#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def build():
    shelltools.export("GOROOT", "%s"  % get.workDIR())
    shelltools.export("GOROOT_FINAL", "/usr/lib/go")
    shelltools.export("GOBIN", "%s/bin"  % get.curDIR())
    shelltools.export("GOOS", "linux")
    shelltools.cd("src")
    shelltools.system("./make.bash")
    # Install race detection version of std libraries (amd64 only)
    if get.ARCH() == "x86_64":
        shelltools.cd("../")
        shelltools.cd("bin")
        shelltools.system("./go install -race std")

def install():
    pisitools.dobin("bin/*")
    pisitools.dodoc("AUTHORS", "CONTRIBUTORS", "PATENTS", "README")
    #There is a known issue which requires the source tree to be installed [1].
    #Once this is fixed, we can consider using the doc use flag to control 
    #installing the doc and src directories.
    # [1] http://code.google.com/p/go/issues/detail?id=2775
    pisitools.dodir("/usr/lib/go")
    pisitools.insinto("/usr/lib/go", "doc")
    pisitools.insinto("/usr/lib/go", "include")
    pisitools.insinto("/usr/lib/go", "lib")
    pisitools.insinto("/usr/lib/go", "pkg")
    pisitools.insinto("/usr/lib/go", "src")
    #vim
    pisitools.insinto("/usr/share/vim/vimfiles", "misc/vim/ftdetect")
    pisitools.insinto("/usr/share/vim/vimfiles", "misc/vim/ftplugin")
    pisitools.insinto("/usr/share/vim/vimfiles", "misc/vim/syntax")
    pisitools.insinto("/usr/share/vim/vimfiles", "misc/vim/indent")
    pisitools.insinto("/usr/share/vim/vimfiles", "misc/vim/plugin")
    #zsh
    pisitools.insinto("/usr/share/zsh/site-functions", "misc/zsh/go")

