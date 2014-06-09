#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import get
from pisi.actionsapi import libtools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import texlivemodules

import os

WorkDir = "."

def setup():
    pisitools.dosed("source/texk/tex4htk/t4ht.c", "SELFAUTOPARENT", "TEXMFROOT")
    #pisitools.dosed("source/texk/xdvik/configure","-lXp", " ")
    shelltools.makedirs("source/build")
    shelltools.cd("source/build")
    shelltools.sym("../configure", "configure")
    autotools.configure('--datarootdir=/usr/share \
                         --datadir=/usr/share \
                         --disable-native-texlive-build \
                         --with-banner-add="/Pisi Linux" \
                         --disable-multiplatform \
                         --disable-dialog \
                         --disable-psutils \
                         --disable-t1utils \
                         --disable-bibtexu \
                         --disable-xz \
                         --enable-shared \
                         --disable-static \
                         --with-system-zlib \
                         --with-system-zziplib \
                         --with-system-pnglib \
                         --with-system-ncurses \
                         --with-system-t1lib \
                         --with-system-gd \
                         --with-system-poppler \
                         --with-system-freetype2 \
                         --with-system-pixman \
                         --with-system-cairo \
                         --with-system-harfbuzz \
                         --with-system-graphite \
                         --with-system-icu \
                         --with-freetype2-libdir=/usr/lib \
                         --with-freetype2-include=/usr/include/freetype2 \
                         --with-xdvi-x-toolkit=xaw \
                         --disable-dump-share \
                         --disable-aleph \
                         --enable-luatex \
                         --with-clisp-runtime=default \
                         --enable-xindy --disable-xindy-rules --disable-xindy-docs')

def build():
    shelltools.cd("source/build")
    autotools.make()

def install():
    pisitools.dobin("biber", "/usr/bin")

    pisitools.dodir("/usr/share/tlpkg/TeXLive")
    shelltools.copy("source/utils/biber/TeXLive/*.pm", "%s/usr/share/tlpkg/TeXLive" % get.installDIR())

    shelltools.cd("source/build")
    autotools.rawInstall('DESTDIR=%s texmf="%s/usr/share/texmf"' % ((get.installDIR(), ) * 2))


    bibtexextra_scripts=["bibexport", "listbib" ,"multibibliography", "urlbst"]

    core_scripts=["a2ping","a5toa4", "adhocfilelist", "afm2afm", "allcm", "allec", "allneeded", "arara","arlatex"
    ,"autoinst", "bundledoc", "checkcites", "chkweb", "context", "ctanify", "ctanupload", "ctxtools", "de-macro", "deweb"
    ,"dosepsbin", "dtxgen", "dvi2fax", "dviasm", "dvired", "e2pall", "epstopdf", "findhyph", "fmtutil", "fmtutil-sys"
    ,"fontinst", "fragmaster", "installfont-tl", "kpsepath", "kpsetool", "kpsewhere", "kpsexpand", "latex2man", "latexdiff"
    ,"latexdiff-vc", "latexfileversion", "latexmk", "latexpand", "latexrevise", "listings-ext.sh", "ltxfileinfo", "lua2dox_filter"
    ,"luaotfload-tool", "luatools", "match_parens", "mf2pt1", "mkjobtexmf", "mkluatexfontdb", "mkt1font", "mktexfmt", "mptopdf"
    ,"mtxrun", "ot2kpx", "pdf180", "pdf270", "pdf90", "pdfatfi", "pdfbook", "pdfcrop", "pdfflip", "pdfjam", "pdfjam-pocketmod"
    ,"pdfjam-slides3up", "pdfjam-slides6up", "pdfjoin", "pdfnup", "pdfpun", "pfarrei", "pkfix", "pkfix-helper", "ps2eps", "ps2frag"
    ,"pslatex", "pstopdf", "purifyeps", "repstopdf", "rpdfcrop", "rungs", "simpdftex", "sty2dtx", "texconfig", "texconfig-dialog"
    ,"texconfig-sys", "texcount", "texdef", "texdiff", "texdirflatten", "texdoc", "texdoctk", "texexec", "texindy", "texlinks"
    ,"texliveonfly", "texloganalyser", "texmfstart", "thumbpdf", "typeoutfileinfo", "updmap", "updmap-sys", "vpl2ovp", "vpl2vpl", "xindy"]

    htmlxml_scripts=["ht", "htcontext", "htlatex", "htmex", "httex", "httexi", "htxelatex", "htxetex", "mk4ht"]

    langcyrillic_scripts=["rubibtex", "rumakeindex"]

    langcjk_scripts=["convbkmk", "ptex2pdf", "kanji-fontmap-creator", "kanji-config-updmap", "kanji-config-updmap-sys"]

    langextra_scripts=["ebong"]

    langgreek_scripts=["mkgrkindex"]

    latexextra_scripts=["authorindex", "exceltex", "makeglossaries", "pdfannotextractor", "perltex", "ps4pdf", "splitindex" ,"svn-multi", "vpe"]

    music_scripts=["m-tx", "musixtex", "musixflx", "pmx2pdf"]

    pictures_scripts=["cachepic", "epspdf", "epspdftk", "fig4latex", "mathspic"]

    pstricks_scripts=["pedigree", "pst2pdf"]

    science_scripts=["ulqda"]

    # remove unneeded files and symlinks
    dirs = []
    for g in [bibtexextra_scripts, core_scripts, htmlxml_scripts, \
              langcjk_scripts, langcyrillic_scripts, langextra_scripts, \
              langgreek_scripts, latexextra_scripts, music_scripts, \
              pictures_scripts, pstricks_scripts, science_scripts, \
              ["tlmgr"]]:
        for s in g:
            if shelltools.isLink("%s/usr/bin/%s" % (get.installDIR(), s)):
                realpath = shelltools.realPath("%s/usr/bin/%s" % (get.installDIR(), s))
                dirname = shelltools.dirName(realpath)
                if not dirname in dirs: dirs.append(dirname)
                if not dirname == "%s/usr/bin" % get.installDIR():
                    if shelltools.isFile(realpath): shelltools.unlink(realpath)
                pisitools.remove("/usr/bin/%s" % s)

    # remove empty dirs
    while dirs:
        tmpdirs = dirs[:]
        for d in tmpdirs:
            if not shelltools.ls(d):
                shelltools.unlinkDir(d)
                dirname = shelltools.dirName(d)
                if not dirname in dirs: dirs.append(dirname)
            dirs.remove(d)
