# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

import os
from distutils.dir_util import copy_tree

def setup():
    # Unpack and prepare files
    for tar_file in shelltools.ls("%s/texlive-core" % get.workDIR()):
        if tar_file.endswith("xz"):
            shelltools.system("tar Jxfv %s" % tar_file)

def build():
    shelltools.cd("%s/texlive-core/" % get.workDIR())
    for folder in ["tlpkg", "doc", "source"]:
        shelltools.unlinkDir(folder)

def install():
    shelltools.cd("%s/texlive-core/" % get.workDIR())
    pisitools.dodir("/usr/share")

    wanteddirs = []
    for file_ in shelltools.ls(get.workDIR()):
        if shelltools.isDirectory(file_) and not "texmf" in file_:
            wanteddirs.append(file_)

    for folder in wanteddirs:
        pisitools.insinto("/usr/share/texmf-dist", folder)

    # fix sandbox violations
    #pisitools.dosed("texmf-dist/scripts/texlive/texlinks.sh", '"\$symlinkdir', r'"%s/$symlinkdir' % get.installDIR())

    # Recursively copy on directory on top of another, overwrite duplicate files too
    if shelltools.can_access_directory("texmf-dist"):
        copy_tree("texmf-dist", "%s/usr/share/texmf-dist" % get.installDIR())

    ## chmod of script files
    script_dir = get.installDIR() + "/usr/share/texmf-dist/scripts"
    if shelltools.can_access_directory(script_dir):
        for root, dirs, files in os.walk(script_dir):
            for name in files:
                shelltools.chmod(os.path.join(root, name), 0755)

    # copy TEXMFCONFIG tree
    pisitools.insinto("/etc/texmf/chktex/", "texmf-dist/chktex/chktexrc")
    pisitools.insinto("/etc/texmf/web2c/", "texmf-dist/web2c/mktex.cnf")
    pisitools.insinto("/etc/texmf/web2c/", "texmf-dist/web2c/updmap.cfg")
    pisitools.insinto("/etc/texmf/web2c/", "texmf-dist/web2c/fmtutil.cnf")
    pisitools.insinto("/etc/texmf/dvips/config/", "texmf-dist/dvips/config/config.ps")
    pisitools.insinto("/etc/texmf/dvipdfmx", "texmf-dist/dvipdfmx/dvipdfmx.cfg")
    pisitools.insinto("/etc/texmf/tex/generic/config/", "texmf-dist/tex/generic/config/pdftexconfig.tex")
    #pisitools.insinto("/etc/texmf/tex/generic/config/", "texmf-dist/tex/generic/config/language.dat")
    #pisitools.insinto("/etc/texmf/tex/generic/config/", "texmf-dist/tex/generic/config/language.def")
    pisitools.insinto("/etc/texmf/ttf2pk", "texmf-dist/ttf2pk/ttf2pk.cfg")
    pisitools.insinto("/etc/texmf/xdvi", "texmf-dist/xdvi/XDvi")
    
    # link programs from /usr/share/texmf-dist/scripts
    linked_scripts="""
a2ping/a2ping.pl
accfonts/mkt1font
accfonts/vpl2ovp
accfonts/vpl2vpl
adhocfilelist/adhocfilelist.sh
arara/arara.sh
bundledoc/arlatex
bundledoc/bundledoc
checkcites/checkcites.lua
chktex/chkweb.sh
chktex/deweb.pl
context/perl/mptopdf.pl
context/stubs/unix/context
context/stubs/unix/ctxtools
context/stubs/unix/luatools
context/stubs/unix/mtxrun
context/stubs/unix/pstopdf
context/stubs/unix/texexec
context/stubs/unix/texmfstart
ctanify/ctanify
ctanupload/ctanupload.pl
de-macro/de-macro
dosepsbin/dosepsbin.pl
dtxgen/dtxgen
dviasm/dviasm.py
epstopdf/epstopdf.pl
findhyph/findhyph
fontools/afm2afm
fontools/autoinst
fontools/ot2kpx
fragmaster/fragmaster.pl
installfont/installfont-tl
latex2man/latex2man
latexdiff/latexdiff-vc.pl
latexdiff/latexdiff.pl
latexdiff/latexrevise.pl
latexfileversion/latexfileversion
latexmk/latexmk.pl
latexpand/latexpand
ltxfileinfo/ltxfileinfo
lua2dox/lua2dox_filter
luaotfload/luaotfload-tool.lua
match_parens/match_parens
mf2pt1/mf2pt1.pl
mkjobtexmf/mkjobtexmf.pl
oberdiek/pdfatfi.pl
pdfcrop/pdfcrop.pl
pdfjam/pdf180
pdfjam/pdf270
pdfjam/pdf90
pdfjam/pdfbook
pdfjam/pdfflip
pdfjam/pdfjam
pdfjam/pdfjam-pocketmod
pdfjam/pdfjam-slides3up
pdfjam/pdfjam-slides6up
pdfjam/pdfjoin
pdfjam/pdfnup
pdfjam/pdfpun
pfarrei/a5toa4.tlu
pfarrei/pfarrei.tlu
pkfix-helper/pkfix-helper
pkfix/pkfix.pl
ps2eps/ps2eps.pl
purifyeps/purifyeps
simpdftex/simpdftex
sty2dtx/sty2dtx.pl
texcount/texcount.pl
texdef/texdef.pl
texdiff/texdiff
texdirflatten/texdirflatten
texdoc/texdoc.tlu
texdoctk/texdoctk.pl
texlive/allcm.sh
texlive/allneeded.sh
texlive/dvi2fax.sh
texlive/dvired.sh
texlive/e2pall.sh
texlive/fmtutil-sys.sh
texlive/fmtutil.sh
texlive/fontinst.sh
texlive/kpsetool.sh
texlive/kpsewhere.sh
texlive/ps2frag.sh
texlive/pslatex.sh
texlive/rungs.tlu
texlive/texconfig-dialog.sh
texlive/texconfig-sys.sh
texlive/texconfig.sh
texlive/texlinks.sh
texlive/updmap-sys.sh
texlive/updmap.pl
texliveonfly/texliveonfly.py
texloganalyser/texloganalyser
thumbpdf/thumbpdf.pl
typeoutfileinfo/typeoutfileinfo.sh
xindy/texindy.pl
xindy/xindy.pl
"""
    for p in linked_scripts.split():
        bn = shelltools.baseName(p).split(".")[0]
        if shelltools.isFile("%s/usr/share/texmf-dist/scripts/%s" % (get.installDIR(), p)):
            pisitools.dosym("/usr/share/texmf-dist/scripts/%s" % p, "/usr/bin/%s" % bn)

    #? pisitools.dosym("/usr/share/texmf-dist/scripts/listings-ext/listings-ext.sh", "/usr/bin/listings-ext.sh")
    pisitools.dosym("allcm", "/usr/bin/allec")
    pisitools.dosym("fmtutil", "/usr/bin/mktexfmt")
    pisitools.dosym("kpsetool", "/usr/bin/kpsexpand")
    pisitools.dosym("kpsetool", "/usr/bin/kpsepath")
    pisitools.dosym("epstopdf", "/usr/bin/repstopdf")
    pisitools.dosym("pdfcrop", "/usr/bin/rpdfcrop")
    pisitools.dosym("luaotfload-tool", "/usr/bin/mkluatexfontdb")

    #remove unneded
    pisitools.removeDir("/usr/share/texmf-dist/scripts/context/stubs/mswin")
    pisitools.removeDir("/usr/share/texmf-dist/scripts/context/stubs/win64")

    #remove conflicts files with texlive-bin
    pisitools.remove("/usr/share/texmf-dist/dvipdfmx/dvipdfmx.cfg")
    pisitools.remove("/usr/share/texmf-dist/dvips/base/*.pro")
    pisitools.remove("/usr/share/texmf-dist/dvips/gsftopk/render.ps")
    pisitools.remove("/usr/share/texmf-dist/fonts/cmap/dvipdfmx/EUC-UCS2")
    pisitools.remove("/usr/share/texmf-dist/fonts/enc/dvips/base/7t.enc")
    pisitools.remove("/usr/share/texmf-dist/fonts/enc/ttf2pk/base/T1-WGL4.enc")
    pisitools.remove("/usr/share/texmf-dist/fonts/map/dvipdfmx/cid-x.map")
    pisitools.removeDir("/usr/share/texmf-dist/fonts/sfd/ttf2pk")
    pisitools.remove("/usr/share/texmf-dist/scripts/context/stubs/unix/*jit")
    pisitools.removeDir("/usr/share/texmf-dist/scripts/crossrefware")
    pisitools.remove("/usr/share/texmf-dist/ttf2pk/ttf2pk.cfg")
    pisitools.remove("/usr/share/texmf-dist/ttf2pk/VPS.rpl")
    
    pisitools.remove("/usr/share/texmf-dist/web2c/mktex*")
    pisitools.removeDir("/usr/share/texmf-dist/xdvi")
    pisitools.removeDir("/usr/share/texmf-dist/bibtex/csf/base")
    pisitools.remove("/usr/share/texmf-dist/chktex/chktexrc")
    
    
