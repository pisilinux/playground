#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

#ARCH = "x64" if get.ARCH() == "x86_64" else "ia32"

def setup():
    shelltools.system("export LC_ALL=C")
    # use_system_ssl is disabled -->  https://bugzilla.mozilla.org/show_bug.cgi?id=547312
    # use_system_icu is disabled --> http://crbug.com/103360
    # use_system_hunspell has build problems, upstream changes needed
    # use_system_sqlite is disabled --> http://crbug.com/22208
    # use_system_ffmpeg has build problems, system libraries might be outdated
#    shelltools.system("export -n CFLAGS CXXFLAGS")
    
    options = '\
                -Dwerror= \
                -Dclang=1 \
                -Dclang_use_chrome_plugins=0 \
                -Dpython_ver=2.7 \
                -Dgoogle_api_key=AIzaSyBINKL31ZYd8W5byPuwTXYK6cEyoceGh6Y \
                -Dgoogle_default_client_id=879512332529.apps.googleusercontent.com \
                -Dgoogle_default_client_secret=RmQPJJeL1cNJ8iETnoVD4X17 \
                -Dlinux_link_gsettings=1 \
                -Dlinux_link_libpci=1 \
                -Dlinux_link_libspeechd=1 \
                -Dlinux_link_pulseaudio=1 \
                -Dlinux_strip_binary=1 \
                -Dlinux_use_gold_binary=0 \
                -Dlinux_use_gold_flags=0 \
                -Dlogging_like_official_build=1 \
                -Drelease_extra_cflags=" -Wno-unused-local-typedefs" \
                -Dlibspeechd_h_prefix=speech-dispatcher/ \
                -Dffmpeg_branding=Chrome \
                -Dbuild_ffmpegsumo=1 \
                -Dproprietary_codecs=1 \
                -Duse_system_bzip2=1 \
                -Duse_system_re2=0 \
                -Duse_system_flac=1 \
                -Duse_system_libwebp=1 \
                -Duse_system_ffmpeg=0 \
                -Duse_system_harfbuzz=0 \
                -Duse_system_sqlite=0 \
                -Duse_system_icu=0 \
                -Duse_system_libevent=1 \
                -Duse_system_libjpeg=1 \
                -Duse_system_libpng=0 \
                -Duse_system_libxml=0 \
                -Duse_system_opus=0 \
                -Duse_system_protobuf=0 \
                -Duse_system_snappy=1 \
                -Duse_system_ssl=0 \
                -Duse_system_xdg_utils=1 \
                -Duse_system_yasm=1 \
                -Duse_system_zlib=0 \
                -Duse_gconf=0 \
                -Dcomponent=shared_library \
                -Dproprietary_codecs=1 \
                -Ddisable_pnacl=1 \
                -Ddisable_nacl=1 \
                -Ddisable_glibc=1 \
                -Ddisable_sse2=1 \
                -Duse_allocator=0 \
                -Dtoolkit_uses_gtk=0 \
                -Dusb_ids_path=/usr/share/misc/usb.ids \
                -Dlinux_sandbox_path=/usr/lib/chromium-browser/chromium-sandbox \
                -Dlinux_sandbox_chrome_path=/usr/lib/chromium-browser/chromium-browser \
                -Dno_strict_aliasing=1 \
                -Dtarget_arch=x64'
               

#We add -fno-ipa-cp to CFLAGS. See: http://crbug.com/41887
#shelltools.system("build/gyp_chromium -f make build/all.gyp --depth=. \ %s" % options)

    shelltools.system('build/linux/unbundle/replace_gyp_files.py %s' % options)
    shelltools.system('build/gyp_chromium --depth=. %s' % options)

def build():
#    shelltools.system("export -n CFLAGS CXXFLAGS")
    shelltools.export("GYP_GENERATORS", "ninja")
    
    shelltools.export("CFLAGS", "%s fno-stack-protector" %get.CFLAGS())
    shelltools.export("CXXFLAGS", "%s -fno-stack-protector" %get.CXXFLAGS())
    shelltools.export("LDFLAGS", "%s -fno-stack-protector -lssp" %get.LDFLAGS())
   
    pisitools.dosed("out/Release/build.ninja", "cc = x86_64-pc-linux-gnu-gcc", "cc = clang")    
    pisitools.dosed("out/Release/build.ninja", "cxx = x86_64-pc-linux-gnu-g\+\+", "cxx = clang\+\+")

    shelltools.system("ninja -v -C out/Release chrome chrome_sandbox chromedriver")

def install():
    shelltools.cd("out/Release")

    shelltools.makedirs("%s/usr/lib/chromium-browser" % get.installDIR())
    
    binaries_for_inst=["chrome", "chrome_sandbox", "chromedriver", "mksnapshot", "protoc", "libvpx_obj_int_extract"]
    libraries_for_inst=["libffmpegsumo.so", "icudtl.dat", "libpdf.so", "libyuv.a"]
    
    # install and strip binaries
    for mybin in binaries_for_inst:
        pisitools.insinto("/usr/lib/chromium-browser", mybin)
        #use it if pisi skips stripping
        #shelltools.system("strip --strip-all %s/usr/lib/chromium-browser/%s" % ( get.installDIR(), mybin))
    
    # install and strip shared libs  
    for mylib in libraries_for_inst:
        pisitools.insinto("/usr/lib/chromium-browser", mylib)
        #use it if pisi skips stripping
        #shelltools.system("strip --strip-unneeded %s/usr/lib/chromium-browser/%s" % ( get.installDIR(), mylib))                                    
        
    pisitools.dosym("/usr/lib/chromium-browser/chrome", "/usr/lib/chromium-browser/chromium-browser")
    pisitools.rename("/usr/lib/chromium-browser/chrome_sandbox", "chrome-sandbox")
    shelltools.chmod("%s/usr/lib/chromium-browser/chrome-sandbox" % get.installDIR(), 04755)
    
    # install rest of needed files
    pisitools.insinto("/usr/lib/chromium-browser", "*.pak")
    pisitools.insinto("/usr/lib/chromium-browser", "locales")
    pisitools.insinto("/usr/lib/chromium-browser", "resources")
    pisitools.insinto("/usr/lib/chromium-browser", "pseudo_locales")
    pisitools.insinto("/usr/lib/chromium-browser", "remoting_locales")
    pisitools.insinto("/usr/lib/chromium-browser", "pyproto")
    pisitools.insinto("/usr/lib/chromium-browser", "java_mojo")
    pisitools.insinto("/usr/lib/chromium-browser/lib", "lib/*.so")
    
    pisitools.newman("chrome.1", "chromium-browser.1")

    shelltools.cd("../..")
    for size in ["22", "24", "48", "64", "128", "256"]:
        pisitools.insinto("/usr/share/icons/hicolor/%sx%s/apps" %(size, size), "chrome/app/theme/chromium/product_logo_%s.png" % size, "chromium-browser.png")

    pisitools.dosym("/usr/share/icons/hicolor/256x256/apps/chromium-browser.png", "/usr/share/pixmaps/chromium-browser.png")
    
    pisitools.dodoc("LICENSE")



