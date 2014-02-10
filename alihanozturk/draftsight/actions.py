#!/usr/bin/python
# -*- coding: utf-8 -*-

# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def install():
    pisitools.insinto("/opt/dassault-systemes/", "/opt/dassault-systemes/*")
    pisitools.insinto("/usr/share/icons/hicolor/128x128/apps/program.png", "dassault-systemes/DraftSight/Resources/pixmaps/128x128/program.png")
    pisitools.insinto("/usr/share/icons/hicolor/128x128/mimetypes/file-dwg.png", "dassault-systemes/DraftSight/Resources/pixmaps/128x128/file-dwg.png")
    pisitools.insinto("/usr/share/icons/hicolor/128x128/mimetypes/file-dxf.png", "dassault-systemes/DraftSight/Resources/pixmaps/128x128/file-dxf.png")
    pisitools.insinto("/usr/share/icons/hicolor/128x128/mimetypes/file-dwt.png", "dassault-systemes/DraftSight/Resources/pixmaps/128x128/file-dwt.png")
    pisitools.insinto("/usr/share/icons/hicolor/64x64/apps/program.png", "dassault-systemes/DraftSight/Resources/pixmaps/64x64/program.png")
    pisitools.insinto("/usr/share/icons/hicolor/64x64/mimetypes/file-dwg.png", "dassault-systemes/DraftSight/Resources/pixmaps/64x64/file-dwg.png")
    pisitools.insinto("/usr/share/icons/hicolor/64x64/mimetypes/file-dxf.png", "dassault-systemes/DraftSight/Resources/pixmaps/64x64/file-dxf.png")
    pisitools.insinto("/usr/share/icons/hicolor/64x64/mimetypes/file-dwt.png", "dassault-systemes/DraftSight/Resources/pixmaps/64x64/file-dwt.png")
    pisitools.insinto("/usr/share/icons/hicolor/32x32/apps/program.png", "dassault-systemes/DraftSight/Resources/pixmaps/32x32/program.png")
    pisitools.insinto("/usr/share/icons/hicolor/32x32/mimetypes/file-dwg.png", "dassault-systemes/DraftSight/Resources/pixmaps/32x32/file-dwg.png")
    pisitools.insinto("/usr/share/icons/hicolor/32x32/mimetypes/file-dxf.png", "dassault-systemes/DraftSight/Resources/pixmaps/32x32/file-dxf.png")
    pisitools.insinto("/usr/share/icons/hicolor/32x32/mimetypes/file-dwt.png", "dassault-systemes/DraftSight/Resources/pixmaps/32x32/file-dwt.png")
    pisitools.insinto("/usr/share/icons/hicolor/16x16/apps/program.png", "dassault-systemes/DraftSight/Resources/pixmaps/16x16/program.png")
    pisitools.insinto("/usr/share/icons/hicolor/16x16/mimetypes/file-dwg.png", "dassault-systemes/DraftSight/Resources/pixmaps/16x16/file-dwg.png")
    pisitools.insinto("/usr/share/icons/hicolor/16x16/mimetypes/file-dxf.png", "dassault-systemes/DraftSight/Resources/pixmaps/16x16/file-dxf.png")
    pisitools.insinto("/usr/share/icons/hicolor/16x16/mimetypes/file-dwt.png", "dassault-systemes/DraftSight/Resources/pixmaps/16x16/file-dwt.png")
    pisitools.insinto("/usr/share/mime/application/dassault-systemes_draftsight-dwg.xml", "dassault-systemes/DraftSight/Resources/dassault-systemes_draftsight-dwg.xml")
    pisitools.insinto("/usr/share/mime/application/dassault-systemes_draftsight-dxf.xml", "dassault-systemes/DraftSight/Resources/dassault-systemes_draftsight-dxf.xml")
    pisitools.insinto("/usr/share/mime/application/dassault-systemes_draftsight-dwt.xml", "dassault-systemes/DraftSight/Resources/dassault-systemes_draftsight-dwt.xml")
    pisitools.insinto("/opt/dassault-systemes/DraftSight/Libraries", "libaudio.so.2")
    pisitools.dohtml("dassault-systemes/DraftSight/Eula/english/*")