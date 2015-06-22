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

version = get.srcVERSION()
driver_dir_name = "nvidia-current"
datadir = "/usr/share/%s" % driver_dir_name

if get.buildTYPE() == 'emul32':
    arch = "x86"
    nvlibdir = "/usr/lib32/%s" % driver_dir_name
    libdir = "/usr/lib32"
    xlibdir= "/usr/lib32/xorg"
else:
    arch = get.ARCH().replace("i686", "x86")
    nvlibdir = "/usr/lib/%s" % driver_dir_name
    libdir = "/usr/lib"
    xlibdir= "/usr/lib/xorg"

def setup():
    shelltools.system("sh NVIDIA-Linux-%s-%s.run -x --target tmp"
                      % (arch, get.srcVERSION()))
    
    shelltools.move("tmp/*", ".")
    
    # Our libc is TLS enabled so use TLS library
    shelltools.unlink("*-tls.so*")
    shelltools.move("tls/*", ".")

    # xorg-server provides libwfb.so
    shelltools.unlink("libnvidia-wfb.so.*")

    shelltools.echo("ld.so.conf", nvlibdir)
    shelltools.echo("XvMCConfig", "%s/libXvMCNVIDIA.so" % nvlibdir)

def build():
    # We don't need kernel module for emul32 build
    if get.buildTYPE() == 'emul32':
        return

    shelltools.export("SYSSRC", "/lib/modules/%s/build" % KDIR)
    shelltools.cd("kernel")

    autotools.make("module")
    
    shelltools.cd("uvm")
    
    autotools.make("module")
    
def install():

    if not get.buildTYPE() == 'emul32':
    # Kernel driver
        pisitools.insinto("/lib/modules/%s/extra/nvidia" % KDIR,
                          "kernel/nvidia.ko")
	
	pisitools.insinto("/lib/modules/%s/extra/nvidia" % KDIR,
                          "kernel/uvm/nvidia-uvm.ko")
	
	# Command line tools and their man pages
        pisitools.dobin("nvidia-smi")
        pisitools.doman("nvidia-smi.1.gz")
        
        for binary in ("nvidia-cuda-mps-control", "nvidia-cuda-mps-server", "nvidia-debugdump", "nvidia-persistenced", "nvidia-smi"):
            pisitools.dobin("%s" %binary)
            
        for man in ("nvidia-smi.1.gz", "nvidia-cuda-mps-control.1.gz", "nvidia-persistenced.1.gz"):
            pisitools.doman("%s" %man)


    ###  Libraries
    # OpenGl library
    pisitools.dolib("libGL.so.%s" % version, nvlibdir)
    pisitools.dosym("libGL.so.%s" % version, "%s/libGL.so.1.2.0" % nvlibdir)
    
    pisitools.dolib("libEGL.so.%s" % version, nvlibdir)
    pisitools.dosym("libEGL.so.%s" % version, "%s/libEGL.so.1.0.0" % nvlibdir)
    
    pisitools.dolib("libGLESv1_CM.so.%s" % version, nvlibdir)
    pisitools.dosym("libGLESv1_CM.so.%s" % version, "%s/libGLESv1_CM.so.1.1.0" % nvlibdir)
    
    pisitools.dolib("libGLESv2.so.%s" % version, nvlibdir)
    pisitools.dosym("libGLESv2.so.%s" % version, "%s/libGLESv2.so.2.0.0" % nvlibdir)

    # OpenCL
    pisitools.dolib("libOpenCL.so.1.0.0", libdir)
    pisitools.dosym("libOpenCL.so.1.0.0", "%s/libOpenCL.so.1.0" % libdir)
    pisitools.dosym("libOpenCL.so.1.0", "%s/libOpenCL.so.1" % libdir)

    # CUDA
    pisitools.dolib("libcuda.so.%s" % version, libdir)
    pisitools.dosym("libcuda.so.%s" % version, "%s/libcuda.so.1" % libdir)
    pisitools.dosym("libcuda.so.1", "%s/libcuda.so" % libdir)

    pisitools.dolib("libnvcuvid.so.%s" % version, libdir)
    pisitools.dosym("libnvcuvid.so.%s" % version, "%s/libnvcuvid.so.1" % libdir)
    pisitools.dosym("libnvcuvid.so.1", "%s/libnvcuvid.so" % libdir)

    # NVML
    # Provides programmatic access to static information and monitoring
    # data for NVIDIA GPUs, as well as limited managment capabilities
    pisitools.dolib("libnvidia-ml.so.%s" % version, libdir)
    pisitools.dosym("libnvidia-ml.so.%s" % version, "%s/libnvidia-ml.so.1" % libdir)

    pisitools.dolib("libnvidia-cfg.so.%s" % version, libdir)
    pisitools.dosym("libnvidia-cfg.so.%s" % version, "%s/libnvidia-cfg.so.1" % libdir)

    pisitools.dolib("libnvidia-compiler.so.%s" % version, libdir)
    pisitools.dosym("libnvidia-compiler.so.%s" % version, "%s/libnvidia-compiler.so.1" % libdir)

    # OpenGL core library and others
    for lib in ("glcore", "tls", "encode", "fbc", "glsi", "ifr", "eglcore", "opencl"):
        pisitools.dolib("libnvidia-%s.so.%s" % (lib, version), libdir)
        pisitools.dosym("libnvidia-%s.so.%s" % (lib, version), "%s/libnvidia-%s.so.1" %(libdir, lib))

    # VDPAU driver
    pisitools.dolib("libvdpau_nvidia.so.%s" % version, "%s/vdpau" % nvlibdir)
    pisitools.dosym("../nvidia-current/vdpau/libvdpau_nvidia.so.%s" % version, "%s/vdpau/libvdpau_nvidia.so.1" % nvlibdir.strip(driver_dir_name))
    
    
    # X modules
    pisitools.dolib("nvidia_drv.so", "%s/modules/drivers" % nvlibdir)
    pisitools.dosym("%s/modules/drivers/nvidia_drv.so" % nvlibdir, "%s/modules/drivers/nvidia_drv.so" % xlibdir)
    pisitools.dolib("libglx.so.%s" % version, "%s/modules/extensions" % nvlibdir)
    pisitools.dosym("libglx.so.%s" % version, "%s/modules/extensions/libglx.so" % nvlibdir)

    # Exit time for emul32 build
    if get.buildTYPE() == 'emul32':
        pisitools.insinto(datadir, "ld.so.conf", "32bit-ld.so.conf")
        return

    pisitools.insinto("/etc/OpenCL/vendors", "nvidia.icd")

    pisitools.insinto(datadir, "ld.so.conf")
    pisitools.insinto(datadir, "XvMCConfig")

    # Documentation
    docdir = "xorg-video-%s" % driver_dir_name
    pisitools.dodoc("LICENSE", "NVIDIA_Changelog", "README.txt", destDir=docdir)
    pisitools.dohtml("html/*", destDir=docdir)

    ### Note
    # This package includes nvidia-setting and nvidia-xconfig binaries. However
    # we have seperate packages for each of them. Nvidia provides tarballs for
    # these binaries. Don't forget to update these package with each NVIDIA
    # driver update.

    # Nvidia-bug-report
    # Comes with our own nvidia-xcfonig package
    # pisitools.dobin("nvidia-bug-report.sh")
