#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import pisitools
from pisi.actionsapi import autotools
from pisi.actionsapi import shelltools

shelltools.export("LC_ALL", "C")

pixmaps = "/usr/share/pixmaps/"
LoVersion = "%s" % get.srcVERSION()
OurWorkDir = "%s/libreoffice-%s" % (get.workDIR(), LoVersion)
OurWorkDir = "%s/libreoffice-6.4.0.0.alpha1" % (get.workDIR())

#for support all languages.
langall="en-US af am ar as ast be bg bn bn-IN bo br brx bs ca ca-valencia cs cy da de dgo dsb dz el en-GB en-ZA eo es et eu fa fi fr fy ga gd gl gu gug he hsb hi hr hu id is it ja ka kab kk km kmr-Latn kn ko kok ks lb lo lt lv mai mk ml mn mni mr my nb ne nl nn nr nso oc om or pa-IN pl pt pt-BR ro ru rw sa-IN sat sd sr-Latn si sid sk sl sq sr ss st sv sw-TZ ta te tg th tn tr ts tt ug uk uz ve vec vi xh zh-CN zh-TW zu"

#only Turkish and English.
lang="tr"

def setup():
    shelltools.chmod("%s/bin/unpack-sources" % OurWorkDir)
    shelltools.export("LO_PREFIX", "/usr")    
    shelltools.export("PYTHON", "python3.6")
    
    # http://site.icu-project.org/download/61#TOC-Migration-Issues
    shelltools.export("CPPFLAGS", "-DU_USING_ICU_NAMESPACE=1")
    shelltools.cd(OurWorkDir)   
  
    shelltools.touch("autogen.lastrun")
    shelltools.system('sed -e "/distro-install-file-lists/d" -i Makefile.in')
    shelltools.system('./autogen.sh                        \
                        --prefix=/opt/libreofficedev                      \
                        --sysconfdir=/etc                  \
                        --with-vendor="Pisi Linux"         \
                        --with-lang="%s"                   \
                        --enable-qt5                       \
                        --enable-gtk3                      \
                        --enable-kde5                      \
                        --with-help                        \
                        --with-myspell-dicts               \
                        --with-java                        \
                        --without-system-dicts             \
                        --without-fonts                    \
                        --disable-postgresql-sdbc          \
                        --without-system-hsqldb            \
                        --enable-release-build=yes         \
                        --enable-python=system             \
                        --with-system-apr                  \
                        --without-system-boost             \
                        --without-system-libcmis           \
                        --without-system-libetonyek        \
                        --without-system-libmspub          \
                        --without-system-libodfgen         \
                        --without-system-libpagemaker      \
                        --without-system-libcdr            \
                        --without-system-mdds              \
                        --without-system-liblangtag        \
                        --without-system-librevenge        \
                        --without-system-libvisio          \
                        --without-system-libstaroffice     \
                        --without-system-libzmf            \
                        --without-system-coinmp            \
                        --without-system-firebird          \
                        --without-system-orcus             \
                        --without-system-ucpp              \
                        --without-system-libwpd            \
                        --without-system-libwpg            \
                        --without-system-libwps            \
                        --without-system-poppler           \
                        --without-system-harfbuzz          \
                        --without-system-graphite          \
                        --with-system-icu                  \
                        --with-system-openssl              \
                        --with-system-cairo                \
                        --with-system-clucene              \
                        --with-system-cppunit              \
                        --with-system-curl                 \
                        --with-system-expat                \
                        --with-system-glm                  \
                        --with-system-hunspell             \
                        --with-system-jpeg                 \
                        --with-system-lcms2                \
                        --with-system-libpng               \
                        --with-system-libxml               \
                        --with-system-neon                 \
                        --with-system-nss                  \
                        --with-system-odbc                 \
                        --with-system-openldap             \
                        --with-system-postgresql           \
                        --with-system-redland              \
                        --with-system-serf                 \
                        --with-system-zlib                 \
                        --enable-scripting-beanshell       \
                        --enable-scripting-javascript      \
                        --disable-odk                      \
                        --enable-ext-wiki-publisher        \
                        --enable-ext-nlpsolver             \
                        --with-jdk-home=/usr/lib/jvm/java-8-openjdk \
                        --with-external-tar=external/tarballs \
                        --with-gdrive-client-id=457862564325.apps.googleusercontent.com \
                        --with-gdrive-client-secret=GYWrDtzyZQZ0_g5YoBCC6F0I \
                        --with-parallelism=%s' % (langall, get.makeJOBS().replace("-j","")))
#--disable-fetch-external \

def build():
    autotools.make("build-nocheck")

def install():
    autotools.rawInstall("DESTDIR=%s distro-pack-install" % get.installDIR())
    
    # cleanup gid_Module
    pisitools.remove("gid_Module*")
    
    # add application descriptions    
    pisitools.insinto("/usr/share/appdata/", "sysui/desktop/appstream-appdata/libreoffice-base.appdata.xml", "libreofficedev-base.appdata.xml")
    pisitools.insinto("/usr/share/appdata/", "sysui/desktop/appstream-appdata/libreoffice-calc.appdata.xml", "libreofficedev-calc.appdata.xml")
    pisitools.insinto("/usr/share/appdata/", "sysui/desktop/appstream-appdata/libreoffice-draw.appdata.xml", "libreofficedev-draw.appdata.xml")
    pisitools.insinto("/usr/share/appdata/", "sysui/desktop/appstream-appdata/libreoffice-impress.appdata.xml", "libreofficedev-impress.appdata.xml")
    pisitools.insinto("/usr/share/appdata/", "sysui/desktop/appstream-appdata/libreoffice-writer.appdata.xml", "libreofficedev-writer.appdata.xml")
    pisitools.insinto("/usr/share/appdata/", "sysui/desktop/appstream-appdata/org.libreoffice.kde.metainfo.xml")
    
    # put configuration files into place
    pisitools.dosym("/opt/libreofficedev/lib/libreoffice/program/bootstraprc", "/etc/libreofficedev/bootstraprc")
    pisitools.dosym("/opt/libreofficedev/lib/libreoffice/program/sofficerc", "/etc/libreofficedev/sofficerc")
    pisitools.dosym("/opt/libreofficedev/lib/libreoffice/share/psprint/psprint.conf", "/etc/libreofficedev/psprint.conf")
    
    # make pyuno find its modules
    pisitools.dosym("/opt/libreofficedev/libreoffice/program/uno.py", "/usr/lib/python3.6/site-packages/uno.py")
    pisitools.dosym("/opt/libreofficedev/libreoffice/program/unohelper.py", "/usr/lib/python3.6/site-packages/unohelper.py")
    
    for pix in ["libreoffice-base", "libreoffice-calc", "libreoffice-draw", "libreoffice-impress", "libreoffice-main", "libreoffice-math", "libreoffice-startcenter", "libreoffice-writer"]:
        pisitools.dosym("/opt/libreofficedev/share/icons/hicolor/32x32/apps/%s.png" % pix, "/usr/share/pixmaps/%s-dev.png" %pix)
        
	
	#Change names with libreofficedev and do symlinks
    pisitools.rename("/usr/share/bash-completion/completions/libreoffice.sh", "libreofficedev.sh")
    pisitools.dosym("/opt/libreofficedev/share/application-registry/libreoffice.applications", "/usr/share/application-registry/libreofficedev.applications")
    shelltools.system("sed -i 's/libreoffice/libreofficedev/g' %s/opt/libreofficedev/share/application-registry/libreoffice.applications" %get.installDIR())
    
    pisitools.dosym("/opt/libreofficedev/share/applications/libreoffice-base.desktop", "/usr/share/applications/libreofficedev-base.desktop")
    pisitools.dosym("/opt/libreofficedev/share/applications/libreoffice-calc.desktop", "/usr/share/applications/libreofficedev-calc.desktop")
    pisitools.dosym("/opt/libreofficedev/share/applications/libreoffice-draw.desktop", "/usr/share/applications/libreofficedev-draw.desktop")
    pisitools.dosym("/opt/libreofficedev/share/applications/libreoffice-impress.desktop", "/usr/share/applications/libreofficedev-impress.desktop")
    pisitools.dosym("/opt/libreofficedev/share/applications/libreoffice-math.desktop", "/usr/share/applications/libreofficedev-math.desktop")
    pisitools.dosym("/opt/libreofficedev/share/applications/libreoffice-startcenter.desktop", "/usr/share/applications/libreofficedev-startcenter.desktop")
    pisitools.dosym("/opt/libreofficedev/share/applications/libreoffice-writer.desktop", "/usr/share/applications/libreofficedev-writer.desktop")
    #pisitools.dosym("/opt/libreofficedev/share/applications/libreoffice-xslfilter.desktop", "/usr/share/applications/libreofficedev-xslfilter.desktop")
    
    shelltools.system("sed -i 's/Icon=libreoffice-base/Icon=libreoffice-base-dev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/base.desktop" %get.installDIR())
    shelltools.system("sed -i 's/Icon=libreoffice-calc/Icon=libreoffice-calc-dev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/calc.desktop" %get.installDIR())
    shelltools.system("sed -i 's/Icon=libreoffice-draw/Icon=libreoffice-draw-dev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/draw.desktop" %get.installDIR())
    shelltools.system("sed -i 's/Icon=libreoffice-impress/Icon=libreoffice-impress-dev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/impress.desktop" %get.installDIR())
    shelltools.system("sed -i 's/Icon=libreoffice-math/Icon=libreoffice-math-dev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/math.desktop" %get.installDIR())
    shelltools.system("sed -i 's/Icon=libreoffice-startcenter/Icon=libreoffice-startcenter-dev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/startcenter.desktop" %get.installDIR())
    shelltools.system("sed -i 's/Icon=libreoffice-writer/Icon=libreoffice-writer-dev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/writer.desktop" %get.installDIR())
    #shelltools.system("sed -i 's/Icon=libreoffice-xslfilter/Icon=libreoffice-xslfilter-dev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/xslfilter.desktop" %get.installDIR())
    
    shelltools.system("sed -i 's/Exec=libreoffice/Exec=libreofficedev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/base.desktop" %get.installDIR())
    shelltools.system("sed -i 's/Exec=libreoffice/Exec=libreofficedev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/calc.desktop" %get.installDIR())
    shelltools.system("sed -i 's/Exec=libreoffice/Exec=libreofficedev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/draw.desktop" %get.installDIR())
    shelltools.system("sed -i 's/Exec=libreoffice/Exec=libreofficedev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/impress.desktop" %get.installDIR())
    shelltools.system("sed -i 's/Exec=libreoffice/Exec=libreofficedev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/math.desktop" %get.installDIR())
    shelltools.system("sed -i 's/Exec=libreoffice/Exec=libreofficedev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/startcenter.desktop" %get.installDIR())
    shelltools.system("sed -i 's/Exec=libreoffice/Exec=libreofficedev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/writer.desktop" %get.installDIR())
    #shelltools.system("sed -i 's/Exec=libreoffice %U/Exec=libreofficedev %U/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/xslfilter.desktop" %get.installDIR())
    
    shelltools.system("sed -i 's/LibreOffice/LibreOfficeDev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/base.desktop" %get.installDIR())
    shelltools.system("sed -i 's/LibreOffice/LibreOfficeDev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/calc.desktop" %get.installDIR())
    shelltools.system("sed -i 's/LibreOffice/LibreOfficeDev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/draw.desktop" %get.installDIR())
    shelltools.system("sed -i 's/LibreOffice/LibreOfficeDev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/impress.desktop" %get.installDIR())
    shelltools.system("sed -i 's/LibreOffice/LibreOfficeDev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/math.desktop" %get.installDIR())
    shelltools.system("sed -i 's/LibreOffice/LibreOfficeDev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/startcenter.desktop" %get.installDIR())
    shelltools.system("sed -i 's/LibreOffice/LibreOfficeDev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/writer.desktop" %get.installDIR())
   # shelltools.system("sed -i 's/Libreoffice/LibreOfficeDev/g' %s/opt/libreofficedev/lib/libreoffice/share/xdg/xslfilter.desktop" %get.installDIR())
    
    for binary in ["libreoffice", "lobase", "localc", "lodraw", "loffice", "lofromtemplate", "loimpress", "lomath", "loweb", "lowriter", "soffice", "unopkg"]:
		pisitools.dosym("/opt/libreofficedev/bin/%s" %binary, "/usr/bin/%sdev" %binary)
	
    pisitools.dosym("/opt/libreofficedev/share/mime/packages/libreoffice.xml", "usr/share/mime/packages/libreofficedev.xml")
    pisitools.dosym("/opt/libreofficedev/share/mime-info/libreoffice.keys", "/usr/share/mime-info/libreofficedev.keys")
    pisitools.dosym("/opt/libreofficedev/share/mime-info/libreoffice.mime", "/usr/share/mime-info/libreofficedev.mime")
