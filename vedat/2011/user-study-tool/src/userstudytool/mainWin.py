#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json

from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4 import QtWebKit

from pds.gui import *
from pds.qprogressindicator import QProgressIndicator
from tray import Tray

from myWidgets import SurveyItem,SurveyItemWidget
from ui_mainMenu import Ui_mainManager
from ui_detailWidget import Ui_InfoWidget 

class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True):
        QtGui.QWidget.__init__(self, parent)

	self.ui = Ui_mainManager()

	if standAlone:
            self.ui.setupUi(self)
        else:
            self.ui.setupUi(parent)
	
	self.setDefaultOptions()
	
	self.initializeTray()

        self.widgets = {}
	
	json_object =  open('../../data/user_studies.json','r')
	self.data = json.load(json_object)
	json_object.close()
	
	self.info = UserStudyItemInfo(self.ui.surveyList)
		
        for survey in self.data["pardusUserStudyList"]:
            item = SurveyItem(survey["title"], self.ui.surveyList)
            item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
            item.setSizeHint(QSize(38,48))
            item.url = QUrl(survey["url"])
	    w = SurveyItemWidget(survey["title"], self, item, self.ui.surveyList)
	   
	    self.widgets[survey["id"]] = w
            self.ui.surveyList.setItemWidget(item, self.widgets[survey["id"]])
            self.connect(w.ui.infoButton, SIGNAL("clicked()"), w.showDescription)
         
        self.connect(self.ui.alwaysHelp, SIGNAL("clicked()"), self.setGlobalParticipation)
        self.connect(self.ui.askToHelp, SIGNAL("clicked()"), self.setGlobalParticipation)
	self.connect(self.ui.rejectHelp, SIGNAL("clicked()"), self.setGlobalParticipation)
	
	self.connect(self.info.ui.hideButton, SIGNAL("clicked()"), self.hideDescription)

	
	 
    def setGlobalParticipation(self):
	json_data =  open('../../data/user_participation_info.json','r')
	self.data = json.load(json_data)
	json_data.close()
	
	if self.ui.alwaysHelp.isChecked() == True:
	    self.data["userParticipation"] = "Always Join" 
	    self.tray.action_alwaysJoin.setChecked(True)
	elif self.ui.askToHelp.isChecked() == True:
	    self.data["userParticipation"] = "Ask Before Join" 
	    self.tray.action_askToJoin.setChecked(True)
	else :
	    self.data["userParticipation"] = "Do not Join"
	    self.tray.action_rejectJoin.setChecked(True)
	
	f = open('../../data/user_participation_info.json','w')
	string = json.dump(self.data,f, indent = 2)
	f.close()
    
    def setDefaultOptions(self):
	json_data =  open('../../data/user_participation_info.json','r')
	self.data = json.load(json_data)
	json_data.close()
	
	if self.data["userParticipation"] == "Always Join":
	    self.ui.alwaysHelp.setChecked(True)
	elif self.data["userParticipation"] == "Ask Before Join":
	    self.ui.askToHelp.setChecked(True)
	else:
	    self.ui.rejectHelp.setChecked(True)
	    
    def showDescription(self, url):
	
	self.info.ui.webView.load(url)
	
	self.info.resize(self.ui.surveyList.size())
	self.info.animate(start = MIDLEFT, stop = MIDCENTER)
	QtGui.qApp.processEvents()
	self.ui.alwaysHelp.setEnabled(False)
	self.ui.askToHelp.setEnabled(False)
	self.ui.rejectHelp.setEnabled(FalsQWidgete)
	
	#self.busy =QProgressIndicator(self)
	#self.addWidget(self.busy)
	#self.busy.startAnimation()
	#self.setAnimationDelay(100)
	#self.stopAnimation()
    def hideDescription(self):
	if self.info.isVisible():
	    self.info.animate(start = MIDCENTER,
			stop  = MIDRIGHT,
			direction = OUT)
	self.ui.alwaysHelp.setEnabled(True)
	self.ui.askToHelp.setEnabled(True)
	self.ui.rejectHelp.setEnabled(True)
	
    def initializeTray(self):
	self.tray = Tray(self)
	
class UserStudyItemInfo(PAbstractBox):

    def __init__(self, parent):
	PAbstractBox.__init__(self, parent)
	
	self.ui = Ui_InfoWidget()
	self.ui.setupUi(self)
	
	self.ui.hideButton = QtGui.QPushButton(self.ui.webView)
	
	self._animation = 2
	self._duration = 500
	
	self.enableOverlay()
	self.hide()
	
    def resizeEvent(self, event):
	PAbstractBox.resizeEvent(self, event)
	print event.size().width()
	self.ui.hideButton.move(event.size().width()-self.ui.hideButton.width(),0)

	
    
	
	
	
	  
	
