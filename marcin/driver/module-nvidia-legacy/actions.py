# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import kerneltools
from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "."
KDIR = kerneltools.getKernelVersion()
NoStrip = ["/lib/modules"]

arch = get.ARCH().replace("i686", "x86")
version = get.srcVERSION()
driver = "nvidia-legacy"
libdir = "/usr/lib/%s" % driver
datadir = "/usr/share/%s" % driver

def setup():
    shelltools.system("sh NVIDIA-Linux-%s-%s.run -x --target tmp" % (arch, version))
    shelltools.move("tmp/*", ".")

    # Our libc is TLS enabled so use TLS library
    shelltools.unlink("*-tls.so*")
    shelltools.move("tls/*", "./")
    shelltools.unlinkDir("tls")

    # xorg-server provides libwfb.so
    shelltools.unlink("libnvidia-wfb.so.*")

    shelltools.echo("ld.so.conf", libdir)
    shelltools.echo("XvMCConfig", "%s/libXvMCNVIDIA.so" % libdir)

def build():
    shelltools.export("SYSSRC", "/lib/modules/%s/build" % KDIR)
    shelltools.cd("kernel")
    autotools.make("module")

def install():
    # Kernel driver
    pisitools.insinto("/lib/modules/%s/extra/nvidia" % KDIR, "kernel/nvidia.ko", "%s.ko" % driver)

    # Libraries and X modules
    pisitools.insinto(libdir, "*so.%s" % version)
    pisitools.insinto(libdir, "*so.1.0.0")

    # Symlinks
    pisitools.dosym("libGL.so.%s" % version, "%s/libGL.so.1.2.0" % libdir)
    pisitools.dosym("libGLcore.so.%s" % version, "%s/libGLcore.so.1" % libdir)

    pisitools.dosym("libXvMCNVIDIA.so.%s" % version, "%s/libXvMCNVIDIA.so.1" % libdir)
    pisitools.dosym("libXvMCNVIDIA.so.1", "%s/libXvMCNVIDIA.so" % libdir)

    pisitools.dosym("libcuda.so.%s" % version, "%s/libcuda.so.1" % libdir)
    pisitools.dosym("libcuda.so.1", "%s/libcuda.so" % libdir)

    pisitools.dosym("libnvidia-cfg.so.%s" % version, "%s/libnvidia-cfg.so.1" % libdir)
    pisitools.dosym("libnvidia-tls.so.%s" % version, "%s/libnvidia-tls.so.1" % libdir)

    pisitools.dosym("libglx.so.%s" % version, "%s/modules/extensions/libglx.so" % libdir)

    pisitools.insinto(datadir, "ld.so.conf")
    pisitools.insinto(datadir, "XvMCConfig")

    # Documentation
    docdir = "xorg-video-%s" % driver
    pisitools.dodoc("LICENSE", "README.txt", destDir=docdir)
    pisitools.dohtml("html/*", destDir=docdir)
