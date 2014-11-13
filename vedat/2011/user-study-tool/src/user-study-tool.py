#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import *

import pds
from pds import Pds

_pds = Pds('user-study-tool', debug = False)
_ = _pds.i18n

if __name__ == '__main__':
 
    PACKAGE     = "Pardus Kullanım Araştırmaları"
    appName     = "user-study-tool"
    modName     = "userstudytool"
    version     = "1.0.0"
    homePage    = "http://svn.pardus.org.tr/uludag/trunk/playground/intern/user-study-tool"
    bugEmail    = "bugs@pardus.org.tr"
    catalog     = appName


    if _pds.session == pds.Kde4:
      
	from PyKDE4.kdeui import *
        from PyKDE4.kdecore import KAboutData, ki18n, ki18nc, KCmdLineArgs
   
	programName = ki18n(PACKAGE)
	description = ki18n(PACKAGE)
	license     = KAboutData.License_GPL
	copyright   = ki18n("(c) TUBITAK/UEKAE")
	text        = ki18n(None)
	aboutData   = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

	#Authors
	aboutData.addAuthor(ki18n("Bertan Gündoğdu"), ki18n("Current Maintainer"))
	aboutData.addAuthor(ki18n("Sinem Oğuz"), ki18n(""))
	aboutData.setTranslator(ki18nc("NAME OF TRANSLATORS", "Your names"), ki18nc("EMAIL OF TRANSLATORS", "Your emails"))
	from userstudytool.myStandalone import SurveyManager
	KCmdLineArgs.init(sys.argv, aboutData)

	#Create a Kapplitcation instance
	app = KApplication()

	#Create Main Widget
	mainWindow = SurveyManager(None, appName)
	mainWindow.show()
	
    else:
	from userstudytool.mainWin import MainManager

	#Pds Stuff
	from pds.quniqueapp import QUniqueApplication
	
	app = QUniqueApplication(sys.argv, catalog = appName)
	
	#Create Main Widget and make some settings
	mainWindow = MainManager(None)
	mainWindow.show()
	mainWindow.resize(640, 480)
	mainWindow.setWindowTitle(_(PACKAGE))
	


    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

    # Run the applications
    app.exec_()
