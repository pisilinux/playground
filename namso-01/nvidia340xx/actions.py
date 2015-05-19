#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import kerneltools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir = "."

KDIR = kerneltools.getKernelVersion()
version = get.srcVERSION()
driver_dir_name = "nvidia"
libdir = "/usr/lib32" if get.buildTYPE() == 'emul32' else "/usr/lib"
arch = "x86"  if get.buildTYPE() == 'emul32' else get.ARCH().replace("i6", "x")

def setup():
    shelltools.system("sh NVIDIA-Linux-%s-%s-no-compat32.run --extract-only"
                      % (arch, get.srcVERSION()))
    
def build():    
    shelltools.cd("NVIDIA-Linux-%s-%s-no-compat32" %(arch, get.srcVERSION()))
    
    shelltools.system("tar -xf nvidia-persistenced-init.tar.bz2")
    
    shelltools.touch("nvidia.conf")
    shelltools.system('echo "blacklist nouveau" >> "nvidia.conf"')
        
    shelltools.touch("nvidia-tls.conf")
    shelltools.system('echo "blacklist nouveau" >> "nvidi-tls.conf"')
    pisitools.dosed("nvidi-tls.conf", "blacklist nouveau", "blacklist nouveau\nblacklist nvidiafb")
    
    shelltools.cd("kernel")
    autotools.make("SYSSRC=/lib/modules/%s/build module" % KDIR)
    
    shelltools.cd("uvm")
    autotools.make("SYSSRC=/lib/modules/%s/build module" % KDIR)
    

def install():
    pisitools.insinto("/lib/modules/extra/%s/" % driver_dir_name, "NVIDIA-Linux-%s-%s-no-compat32/kernel/nvidia.ko" % (arch, get.srcVERSION()))
    pisitools.insinto("/lib/modules/extra/%s/" % driver_dir_name, "NVIDIA-Linux-%s-%s-no-compat32/kernel/uvm/nvidia-uvm.ko" % (arch, get.srcVERSION()))
    
    pisitools.insinto("/lib/modprobe.d/", "NVIDIA-Linux-%s-%s-no-compat32/nvidia.conf" % (arch, get.srcVERSION()))
    pisitools.insinto("/lib/modprobe.d/", "NVIDIA-Linux-%s-%s-no-compat32/nvidia-tls.conf" % (arch, get.srcVERSION()))
    
    shelltools.cd("NVIDIA-Linux-%s-%s-no-compat32/"% (arch, get.srcVERSION()))
    # OpenCL
    pisitools.insinto("/etc/OpenCL/vendors/", "nvidia.icd")
    pisitools.insinto("/usr/lib/", "libnvidia-opencl.so.%s" % get.srcVERSION())
    pisitools.dosym("libnvidia-opencl.so.%s" % get.srcVERSION(), "%s/libnvidia-opencl.so" % libdir)
    pisitools.dosym("libnvidia-opencl.so.%s" % get.srcVERSION(), "%s/libnvidia-opencl.so.1" % libdir)
    pisitools.insinto("/usr/lib/", "libnvidia-compiler.so.%s" % get.srcVERSION())
    pisitools.dosym("libnvidia-compiler.so.%s" % get.srcVERSION(), "%s/libnvidia-compiler.so" % libdir)
    pisitools.insinto("/usr/lib/", "libOpenCL.so.1.0.0")
    pisitools.dosym("libOpenCL.so.1.0.0", "%s/libOpenCL.so" % libdir)
    pisitools.dosym("libOpenCL.so.1.0.0", "%s/libOpenCL.so.1.0" % libdir)
    
    # nvidia libgl 
    pisitools.insinto("/usr/lib/", "libEGL.so.%s" % get.srcVERSION())
    pisitools.dosym("libEGL.so.%s" % get.srcVERSION(), "%s/libEGL.so" % libdir)
    pisitools.dosym("libEGL.so.%s" % get.srcVERSION(), "%s/libEGL.so.1" % libdir)
    pisitools.insinto("/usr/lib/", "libGL.so.%s" % get.srcVERSION())
    pisitools.dosym("libGL.so.%s" % get.srcVERSION(), "%s/libGL.so" % libdir)
    pisitools.dosym("libGL.so.%s" % get.srcVERSION(), "%s/libGL.so.1" % libdir)
    pisitools.insinto("/usr/lib/", "libGLESv1_CM.so.%s" % get.srcVERSION())
    pisitools.dosym("libGLESv1_CM.so.%s" % get.srcVERSION(), "%s/libGLESv1_CM.so" % libdir)
    pisitools.dosym("libGLESv1_CM.so.%s" % get.srcVERSION(), "%s/libGLESv1_CM.so.1" % libdir)
    pisitools.insinto("/usr/lib/xorg/modules/extensions/", "libglx.so.%s" % get.srcVERSION())
    #pisitools.dosym("libglx.so.%s" % get.srcVERSION(), "%s/xorg/modules/extensions/libglx.so" % libdir)
    pisitools.dosym("libglx.so.%s" % get.srcVERSION(), "%s/xorg/modules/extensions/libglx.so.1" % libdir)    
    pisitools.insinto("/usr/lib/", "libGLESv2.so.%s" % get.srcVERSION())
    pisitools.dosym("libGLESv2.so.%s" % get.srcVERSION(), "%s/libGLESv2.so" % libdir)
    pisitools.dosym("libGLESv2.so.%s" % get.srcVERSION(), "%s/libGLESv2.so.2" % libdir)
    
    #nvidia-utils
    # X driver
    
    pisitools.insinto("/usr/lib/xorg/modules/drivers/", "nvidia_drv.so")
    
    # GLX extension module for X
    
    pisitools.insinto("/usr/lib/nvidia/xorg/modules/extensions/", "libglx.so.%s" % get.srcVERSION())
    pisitools.dosym("libglx.so.%s" % get.srcVERSION(), "%s/nvidia/xorg/modules/extensions/libglx.so" % libdir)
    
    # OpenGL libraries
    pisitools.insinto("/usr/lib/nvidia/", "libGL.so.%s" % get.srcVERSION())
    pisitools.insinto("/usr/lib/nvidia/", "libEGL.so.%s" % get.srcVERSION())
    pisitools.insinto("/usr/lib/nvidia/", "libGLESv1_CM.so.%s" % get.srcVERSION())
    pisitools.insinto("/usr/lib/nvidia/", "libGLESv2.so.%s" % get.srcVERSION())
    
    # OpenGL core library
    
    pisitools.insinto("/usr/lib/", "libnvidia-glsi.so.%s" % get.srcVERSION())
    pisitools.insinto("/usr/lib/", "libnvidia-glcore.so.%s" % get.srcVERSION())
    pisitools.insinto("/usr/lib/", "libnvidia-eglcore.so.%s" % get.srcVERSION())
    
    #misc
    
    pisitools.insinto("/usr/lib/", "libnvidia-ml.so.%s" % get.srcVERSION())
    pisitools.insinto("/usr/lib/", "libnvidia-cfg.so.%s" % get.srcVERSION())
    pisitools.insinto("/usr/lib/", "libnvidia-fbc.so.%s" % get.srcVERSION())
    pisitools.insinto("/usr/lib/", "libnvidia-ifr.so.%s" % get.srcVERSION())
    pisitools.insinto("/usr/lib/", "libnvidia-encode.so.%s" % get.srcVERSION())
    
    # VDPAU
    
    pisitools.insinto("/usr/lib/vdpau/", "libvdpau_nvidia.so.%s" % get.srcVERSION())
    
    
    # nvidia-tls library
    
    pisitools.insinto("/usr/lib/", "tls/libnvidia-tls.so.%s" % get.srcVERSION())
    
    # CUDA   
    
    pisitools.insinto("/usr/lib/", "libcuda.so.%s" % get.srcVERSION())
    pisitools.insinto("/usr/lib/", "libnvcuvid.so.%s" % get.srcVERSION())
    
    # DEBUG
    
    pisitools.dobin("nvidia-debugdump")
    
    # nvidia-xconfig
        # nvidia-bug-report
    pisitools.dobin("nvidia-bug-report.sh")
    pisitools.dobin("nvidia-xconfig")
    pisitools.doman("nvidia-xconfig.1.gz")
    
    # nvidia-settings
    
    pisitools.dobin("nvidia-settings")
    pisitools.doman("nvidia-settings.1.gz")
    pisitools.insinto("/usr/share/applications/", "nvidia-settings.desktop")
    pisitools.dosed("%s/usr/share/applications/nvidia-settings.desktop" % get.installDIR(), "__UTILS_PATH__/", "/usr/bin/")
    pisitools.dosed("%s/usr/share/applications/nvidia-settings.desktop" % get.installDIR(), "__PIXMAP_PATH__/", "/usr/share/applications")
    pisitools.dopixmaps("nvidia-settings.png")
    pisitools.insinto("/usr/lib/", "libnvidia-gtk2.so.%s" % get.srcVERSION())
    pisitools.insinto("/usr/lib/", "libnvidia-gtk3.so.%s" % get.srcVERSION())
    
    # nvidia-smi
    
    pisitools.dobin("nvidia-smi")
    pisitools.doman("nvidia-smi.1.gz")
    
    # nvidia-cuda-mps
    
    pisitools.dobin("nvidia-cuda-mps-server")
    pisitools.dobin("nvidia-cuda-mps-control")
    pisitools.doman("nvidia-cuda-mps-control.1.gz")
    
    # nvidia-modprobe
    # This should be removed if nvidia fixed their uvm module!
    
    pisitools.dobin("nvidia-modprobe")
    pisitools.doman("nvidia-modprobe.1.gz")
    
    # nvidia-persistenced
    
    pisitools.dobin("nvidia-persistenced")
    pisitools.doman("nvidia-persistenced.1.gz")
    pisitools.insinto("/usr/lib/systemd/system/", "nvidia-persistenced-init/systemd/nvidia-persistenced.service.template", "nvidia-persistenced.service")
    pisitools.dosed("%s/usr/lib/systemd/system/nvidia-persistenced.service" % get.installDIR(), "__USER__", "nvidia-persistenced")
        
    # application profiles
    
    pisitools.insinto("/usr/share/nvidia/", "nvidia-application-profiles-%s-rc" % get.srcVERSION())
    pisitools.insinto("/usr/share/nvidia/", "nvidia-application-profiles-%s-key-documentation" % get.srcVERSION())
    
    pisitools.dodoc("LICENSE", "README*", "NVIDIA_Changelog")
    pisitools.dohtml("html/*")