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
    autotools.make()
    
def install():

    if not get.buildTYPE() == 'emul32':
    # Kernel driver
        pisitools.insinto("/lib/modules/%s/extra" % KDIR,
                          "kernel/nvidia.ko")
	
	pisitools.insinto("/lib/modules/%s/extra" % KDIR,
                          "kernel/nvidia-uvm.ko")
	
	pisitools.insinto("/lib/modules/%s/extra" % KDIR,
                          "kernel/nvidia-modeset.ko")
	
	pisitools.insinto("/lib/modules/%s/extra" % KDIR,
                          "kernel/nvidia-drm.ko")	
	
	# Command line tools and their man pages
        pisitools.dobin("nvidia-smi")
        pisitools.doman("nvidia-smi.1.gz")
        
        for binary in ("nvidia-cuda-mps-control", "nvidia-cuda-mps-server", "nvidia-debugdump", "nvidia-persistenced", "nvidia-smi", "nvidia-modprobe"):
            pisitools.dobin("%s" %binary)
            
        for man in ("nvidia-smi.1.gz", "nvidia-cuda-mps-control.1.gz", "nvidia-persistenced.1.gz"):
            pisitools.doman("%s" %man)


    ###  Libraries
    # OpenGl library
    pisitools.dolib("libGL.so.%s" %version, nvlibdir)
    pisitools.dosym("libGL.so.%s" %version, "%s/libGL.so.1.2.0" % nvlibdir)
    pisitools.dosym("libGL.so.%s" %version, "%s/libGL.so.1" % nvlibdir)
    pisitools.dosym("libGL.so.%s" %version, "%s/libGL.so" % nvlibdir)
        
    
    pisitools.dolib("libGLESv1_CM_nvidia.so.%s" %version, nvlibdir)
    pisitools.dosym("libGLESv1_CM_nvidia.so.%s" %version, "%s/libGLESv1_CM.so.1.1.0" % nvlibdir)
    #pisitools.dosym("libGLESv1_CM_nvidia.so.%s" %version, "%s/libGLESv1_CM.so.1" % nvlibdir)
    #pisitools.dosym("libGLESv1_CM_nvidia.so.%s" %version, "%s/libGLESv1_CM.so" % nvlibdir)
    
    pisitools.dolib("libGLESv2_nvidia.so.%s" %version, nvlibdir)
    pisitools.dosym("libGLESv2_nvidia.so.%s" %version, "%s/libGLESv2.so.2.0.0" % nvlibdir)
    #pisitools.dosym("libGLESv2_nvidia.so.%s" %version, "%s/libGLESv2.so.2" % nvlibdir)
    #pisitools.dosym("libGLESv2_nvidia.so.%s" %version, "%s/libGLESv2.so" % nvlibdir)
    
    pisitools.dolib("libEGL_nvidia.so.%s" %version, nvlibdir)
    pisitools.dosym("libEGL_nvidia.so.%s" %version, "%s/libEGL.so.1.0.0" % nvlibdir)
    #pisitools.dosym("libEGL_nvidia.so.%s" %version, "%s/libEGL.so.1" % nvlibdir)
    #pisitools.dosym("libEGL_nvidia.so.%s" %version, "%s/libEGL.so" % nvlibdir)

    # OpenCL
    pisitools.dolib("libOpenCL.so.1.0.0", libdir)
    pisitools.dosym("libOpenCL.so.1.0.0", "%s/libOpenCL.so.1.0" % libdir)
    pisitools.dosym("libOpenCL.so.1.0", "%s/libOpenCL.so.1" % libdir)
    pisitools.dosym("libOpenCL.so.1.0", "%s/libOpenCL.so" % libdir)
    
    pisitools.dolib("libOpenGL.so.0", libdir)
    pisitools.dosym("libOpenGL.so.0", "%s/libOpenGL.so" %libdir)    
    
    pisitools.dolib("libGLX.so.0", libdir)
    pisitools.dosym("libGLX.so.0", "%s/libGLX.so" %libdir)
    
    pisitools.dolib("libGLdispatch.so.0", libdir)
    pisitools.dosym("libGLdispatch.so.0", "%s/libGLdispatch.so" %libdir)
    
    # OpenGL core library and others
    
    for lib in ("cfg", "compiler", "eglcore", "encode", "fatbinaryloader", "fbc", "glcore", "glsi", "ifr", "ml", "opencl", "ptxjitcompiler", "tls"):
        pisitools.dolib("libnvidia-%s.so.%s" % (lib, version), libdir)
        pisitools.dosym("libnvidia-%s.so.%s" % (lib, version), "%s/libnvidia-%s.so.1" %(libdir, lib))
        pisitools.dosym("libnvidia-%s.so.%s" % (lib, version), "%s/libnvidia-%s.so" %(libdir, lib))
        
    for nlib in ("cuda", "nvcuvid", "GLX_nvidia"):
        pisitools.dolib("lib%s.so.%s" % (nlib, version), libdir)
        pisitools.dosym("lib%s.so.%s" % (nlib, version), "%s/lib%s.so.1" %(libdir, nlib))
        pisitools.dosym("lib%s.so.%s" % (nlib, version), "%s/lib%s.so" %(libdir, nlib))
    
    
    pisitools.dosym("libnvidia-ml.so.%s" % version, "%s/libnvidia-ml.so.0" % libdir)
    
    # VDPAU driver
    pisitools.dolib("libvdpau_nvidia.so.%s" % version, "%s/vdpau" % nvlibdir)
    pisitools.dosym("../nvidia-current/vdpau/libvdpau_nvidia.so.%s" % version, "%s/vdpau/libvdpau_nvidia.so.1" % nvlibdir.strip(driver_dir_name))
    pisitools.dosym("../nvidia-current/vdpau/libvdpau_nvidia.so.%s" % version, "%s/vdpau/libvdpau_nvidia.so" % nvlibdir.strip(driver_dir_name))
    pisitools.dosym("../nvidia-current/vdpau/libvdpau_nvidia.so.%s" % version, "%s/vdpau/libvdpau_nvidia.so.1.0.0" % nvlibdir.strip(driver_dir_name))
    
    #pisitools.dolib("libvdpau_trace.so.%s" % version, "%s/vdpau" % nvlibdir)
    
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
    
    pisitools.insinto("/usr/share/nvidia", "nvidia-application-profiles-%s-rc" %version)
    pisitools.insinto("/usr/share/nvidia", "nvidia-application-profiles-%s-key-documentation" %version)

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
