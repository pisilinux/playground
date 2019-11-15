#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir = "chromium-%s" % get.srcVERSION()

shelltools.export("HOME", get.workDIR())

ARCH = "x64"

def setup():
    shelltools.export("LC_ALL", "C")
    shelltools.system("mkdir -p third_party/node/linux/node-linux-x64/bin")
    shelltools.system("ln -s /usr/bin/node third_party/node/linux/node-linux-x64/bin/")
    
    
    
    #Change name to Chromium-dev
    shelltools.system("sed -e 's|=Chromium|&-dev|g' -i chrome/app/theme/chromium/BRANDING")
    shelltools.system(""" sed -e '0,/output_name = "chrome"/s/= "chrome"/= "chromium-dev"/' \
					      -e 's|root_out_dir/chrome"|root_out_dir/chromium-dev"|g' \
					      -i chrome/BUILD.gn """)
    shelltools.system(""" sed -e 's|"chromium-browser"|"chromium-dev"|g' -i media/audio/pulse/pulse_util.cc """)
    shelltools.system(""" sed -e 's|"Chromium|&-dev|g' -i chrome/common/chrome_constants.cc """)
    shelltools.system(""" sed -e 's|chromium-browser|chromium-dev|g' \
						 -i chrome/browser/shell_integration_linux.cc \
						 -i chrome/browser/ui/libgtkui/gtk_util.cc """)
    shelltools.system(""" sed -e 's|config_dir.Append("chromium|&-dev|' -i chrome/common/chrome_paths_linux.cc """)
    shelltools.system(""" sed -e 's|/etc/chromium|&-dev|' \
						  -e 's|/usr/share/chromium|&-dev|' \
						  -i chrome/common/chrome_paths.cc """)
    shelltools.system(""" sed -e 's|/etc/chromium|&-dev|' \
						  -e "s|'app_name': 'Chromium|&-dev|g" \
						  -i components/policy/tools/template_writers/writer_configuration.py """)

	#Change name of chrome-sandbox
    shelltools.system("sed -e 's|chrome-sandbox|chrome_sandbox|g' -i sandbox/linux/suid/client/setuid_sandbox_host.cc")    
    
    #Enable VAAPI
    shelltools.system("sed 's|/dri/|/|g' -i media/gpu/vaapi/vaapi_wrapper.cc")
    
    #Unbundle zlib
    #shelltools.system("sed 's|zlib:zlib_config|zlib:system_zlib|g' -i third_party/perfetto/gn/BUILD.gn")
    
    
    

    #for LIB in ["freetype", "flac", "ffmpeg", "fontconfig", "harfbuzz-ng", "libdrm", "libjpeg", "libxml" ,"libxslt", "libwebp", "opus", "re2", "snappy", "yasm"]:
        #shelltools.system('find -type f -path "*third_party/$LIB/*" \! -path "*third_party/$LIB/chromium/*" \! -path "*third_party/$LIB/google/*" \! -regex ".*\.\(gn\|gni\|isolate\|py\)" -delete')
	
	
    #shelltools.system("build/linux/unbundle/replace_gn_files.py --system-libraries flac ffmpeg fontconfig freetype harfbuzz-ng libdrm libjpeg libxml libxslt libwebp opus re2 snappy yasm")
    
    shelltools.system("sed -i -e 's/\<xmlMalloc\>/malloc/' -e 's/\<xmlFree\>/free/' \
                       third_party/blink/renderer/core/xml/*.cc \
                       third_party/blink/renderer/core/xml/parser/xml_document_parser.cc \
					   third_party/libxml/chromium/libxml_utils.cc")

    opt = 'use_sysroot=false \
           enable_nacl=true \
           enable_nacl_nonsfi=true \
           use_custom_libcxx=true \
           clang_use_chrome_plugins=false \
           is_official_build=true \
           fieldtrial_testing_like_official_build=true \
           clang_use_chrome_plugins=false \
           fatal_linker_warnings=false \
           treat_warnings_as_errors=false \
           use_gnome_keyring=false\
           use_gold=false \
           use_aura=true \
           use_dbus=true \
           ffmpeg_branding="ChromeOS" \
           enable_hangout_services_extension=true \
           enable_widevine=true \
           linux_use_bundled_binutils=false \
           is_debug=false \
           google_default_client_secret="0ZChLK6AxeA3Isu96MkwqDR4" \
           google_api_key="AIzaSyDwr302FpOSkGRpLlUpPThNTDPbXcIn_FM" \
           google_default_client_id="413772536636.apps.googleusercontent.com" \
           remove_webcore_debug_symbols=true \
           proprietary_codecs=true \
           link_pulseaudio=true \
           enable_swiftshader=false \
           use_vaapi=true \
           closure_compile=false'
           
        
    shelltools.system("build/download_nacl_toolchains.py --packages nacl_x86_newlib,pnacl_newlib,pnacl_translator sync --extract")
    shelltools.system("tools/clang/scripts/update.py")
    
    clangpath = "%s/chromium-%s/third_party/llvm-build/Release+Asserts/bin/" %(get.workDIR(), get.srcVERSION())

    shelltools.export("CC", "%s/clang" %clangpath )
    shelltools.export("CXX", "%s/clang++" %clangpath)
    shelltools.export("AR", "%s/llvm-ar" %clangpath)
    
    shelltools.export("CFLAGS", "-Wno-builtin-macro-redefined")
    shelltools.export("CXXFLAGS", "-Wno-builtin-macro-redefined")
    #shelltools.export("LDFLAGS", "-static-libgcc -static-libstdc++")
    shelltools.export("CPPFLAGS", "-D__DATE__=  -D__TIME__=  -D__TIMESTAMP__=")
    
    shelltools.system(""" sed "s|fuse-ld=lld|fuse-ld=%s/ld.lld|g" -i build/config/compiler/BUILD.gn """ %clangpath)
    
    #Build FFmpeg
    #shelltools.system("third_party/ffmpeg/chromium/scripts/build_ffmpeg.py linux x64 --branding ChromeOS -- \
		               #--disable-lto \
		               #--cc=%s/clang \
		               #--cxx=%s/clang++ \
		               #--ld=%s/clang \
		               #--ar=%s/llvm-ar \
		               #--extra-ldflags='-fuse-ld=%s/ld.lld' \
		               #" %(clangpath, clangpath, clangpath, clangpath, clangpath) )
	
    #shelltools.system("third_party/ffmpeg/chromium/scripts/copy_config.sh")
    #shelltools.system("third_party/ffmpeg/chromium/scripts/generate_gn.py")
    
    
    shelltools.system("tools/gn/bootstrap/bootstrap.py --gn-gen-args '%s'"% opt)
    shelltools.system("out/Release/gn gen out/Release --args='%s'"% opt)


def build():
    #Sandbox for error must remain separate
    shelltools.system("ninja -C out/Release chrome")
    shelltools.system("ninja -C out/Release chrome_sandbox")
    shelltools.system("ninja -C out/Release chromedriver")

def install():
    shelltools.cd("out/Release")

    #should be checked should for the missing folder "out/Release"
    for vla in ["*.pak", "*.json", "chrome", "locales", "resources", "icudtl.dat", "mksnapshot", "chromedriver", "natives_blob.bin", "snapshot_blob.bin", "character_data_generator", \
			    "libEGL.so", "libGLESv2.so", "libVk*.so", "v8_context_snapshot.bin", "MEIPreload", "nacl_helper", "nacl_helper_bootstrap", "nacl_helper_nonsfi", "nacl_irt_x86_64.nexe"]:
        pisitools.insinto("/usr/lib/chromium-dev", "%s" % vla)

    pisitools.insinto("/usr/lib/chromium-dev", "chrome_sandbox", "chrome-sandbox")
    pisitools.rename("/usr/lib/chromium-dev/chrome", "chrome-dev")
    pisitools.dosym("/usr/lib/chromium-dev/chrome-dev", "/usr/bin/chromium-dev")
    pisitools.dosym("/usr/lib/chromium-browser/PepperFlash", "/usr/lib/chromium-dev/PepperFlash")
 
    shelltools.system("chmod -v 4755 %s/usr/lib/chromium-dev/chrome-sandbox" %get.installDIR())

    #pisitools.newman("chrome.1", "chromium-browser.1")

    shelltools.cd("../..")
    for size in ["24", "48", "64", "128", "256"]:
        pisitools.insinto("/usr/share/icons/hicolor/%sx%s/apps" %(size, size), "chrome/app/theme/chromium/product_logo_%s.png" % size, "chromium-dev.png")

    pisitools.dosym("/usr/share/icons/hicolor/256x256/apps/chromium-browser.png", "/usr/share/pixmaps/chromium-dev.png")

    pisitools.dodoc("LICENSE")
