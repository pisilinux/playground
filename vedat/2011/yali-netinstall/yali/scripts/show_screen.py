#!/usr/bin/python

import sys
sys.path.append("./yali/gui")
sys.path.append("../yali/gui")
from PyQt4 import QtGui
from PyQt4.QtCore import *

app = QtGui.QApplication(sys.argv)
win = QtGui.QMainWindow()

avaliable_modules = [
    "ScrKahyaCheck",          # 00
    "ScrWelcome",             # 01
    "ScrCheckCD",             # 02
    "ScrKeyboard",            # 03
    "ScrDateTime",            # 04
    "ScrUsers",               # 05
    "ScrAdmin",               # 06
    "ScrPartitionAuto",       # 07
    "ScrPartitionManual",     # 08
    "ScrBootloader",          # 09
    "ScrSummary",             # 10
    "ScrInstall",             # 11
    "ScrGoodbye"              # 12
]

module_name = sys.argv[1]
if module_name not in avaliable_modules:
    print " There is no module named with '%s' " % module_name
    print " Avaliable modules are listed below: "
    for module in avaliable_modules:
        print "\t - %s" % module
else:
    print " Loading module %s ..." % module_name
    m = __import__("%s" % module_name)
    w = m.Widget(win)

    win.setCentralWidget(w)
    win.resize(800,600)
    win.show()

    app.connect(app, SIGNAL("lastWindowClosed()"),
                app, SLOT("quit()"))

    app.exec_()
