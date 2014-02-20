#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools

ARCH = "x64" if get.ARCH() == "x86_64" else "ia32"

def setup():
    # use_system_ssl is disabled -->  https://bugzilla.mozilla.org/show_bug.cgi?id=547312
    # use_system_icu is disabled --> http://crbug.com/103360
    # use_system_hunspell has build problems, upstream changes needed
    # use_system_sqlite is disabled --> http://crbug.com/22208
    # use_system_ffmpeg has build problems, system libraries might be outdated

    options = '\
               -Dwerror= \
               -Dlinux_link_gsettings=1 -Dlinux_link_libpci=1 -Dlinux_link_libspeechd=1 -Dlinux_link_pulseaudio=1 -Dlinux_strip_binary=1 -Dproprietary_codecs=1 -Dlogging_like_official_build=1 \
               -Dlinux_sandbox_path=/usr/lib/chromium-browser/chromium-sandbox \
               -Dlinux_sandbox_chrome_path=/usr/lib/chromium-browser/chromium-browser \
               -Dgoogle_api_key=AIzaSyBINKL31ZYd8W5byPuwTXYK6cEyoceGh6Y \
               -Dgoogle_default_client_id=879512332529.apps.googleusercontent.com \
               -Dgoogle_default_client_secret=RmQPJJeL1cNJ8iETnoVD4X17 \
               -Drelease_extra_cflags=-Wno-unused-local-typedefs \
               -Dlibspeechd_h_prefix=speech-dispatcher \
               -Dffmpeg_branding=Chrome \
               -Duse_system_bzip2=1 -Duse_system_flac=1 -Duse_system_harfbuzz=1 -Duse_system_icu=1 -Duse_system_libevent=1 -Duse_system_libjpeg=1 -Duse_system_libpng=1 -Duse_system_opus=1 -Duse_system_snappy=1 -Duse_system_xdg_utils=1 -Duse_system_yasm=1 -Ddisable_sse2=1 -Ddisable_glibc=1 \
               -Duse_system_ffmpeg=0 -Duse_system_libxml=0 -Duse_system_ssl=0 -Duse_system_zlib=0 -Duse_gconf=0 -Dlinux_use_gold_binary=0 -Dlinux_use_gold_flags=0 \
               -Dtarget_arch="%s"' % ARCH

    # We add -fno-ipa-cp to CFLAGS. See: http://crbug.com/41887
#    shelltools.system("build/gyp_chromium -f make build/all.gyp --depth=. \
#                       %s" % options)

    shelltools.system('build/linux/unbundle/replace_gyp_files.py %s' % options)
    shelltools.system('build/gyp_chromium -f make --depth=. %s' % options)

def build():
    autotools.make("chrome chrome_sandbox BUILDTYPE=Release V=1")

def install():
    shelltools.cd("out/Release")

    shelltools.makedirs("%s/usr/lib/chromium-browser" % get.installDIR())

    pisitools.insinto("/usr/lib/chromium-browser", "chrome.pak")
    pisitools.insinto("/usr/lib/chromium-browser", "resources.pak")
    pisitools.insinto("/usr/lib/chromium-browser", "chrome_100_percent.pak")
    pisitools.insinto("/usr/lib/chromium-browser", "content_resources.pak")
    pisitools.insinto("/usr/lib/chromium-browser", "chrome", "chromium-browser")
    pisitools.insinto("/usr/lib/chromium-browser", "chrome_sandbox", "chrome-sandbox")

    # We need to set SUID otherwise it will not run
    shelltools.chmod("%s/usr/lib/chromium-browser/chrome-sandbox" % get.installDIR(), 04755)

    pisitools.insinto("/usr/lib/chromium-browser", "locales")
    pisitools.insinto("/usr/lib/chromium-browser", "resources")

    # Internal ffmpeg libraries
    pisitools.insinto("/usr/lib/chromium-browser", "libffmpegsumo.so")

    # Nacl plugin
    #pisitools.insinto("/usr/lib/chromium-browser", "libppGoogleNaClPluginChrome.so")

    pisitools.newman("chrome.1", "chromium-browser.1")

    shelltools.cd("../..")
    for size in ["22", "24", "48", "64", "128", "256"]:
        pisitools.insinto("/usr/share/icons/hicolor/%sx%s/apps" %(size, size), "chrome/app/theme/chromium/product_logo_%s.png" % size, "chromium-browser.png")

    pisitools.dosym("/usr/share/icons/hicolor/256x256/apps/chromium-browser.png", "/usr/share/pixmaps/chromium-browser.png")
