#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import *

from mainWin import *
import urllib2

class Tray(QtGui.QWidget):
    def __init__(self, parent):
	QtGui.QWidget.__init__(self)
	self.tray = QtGui.QSystemTrayIcon(self)
	self.trayMenu = QtGui.QMenu()
	self.optionsMenu = QtGui.QMenu()
	self.optionsGroup = QtGui.QActionGroup(self)
	self.appWindow = parent 
	
	
	self.action_quit = QtGui.QAction(QtGui.QIcon("../../data/gtk-quit.png"),u'Çık', self)
	self.action_options = QtGui.QAction(QtGui.QIcon("../../data/options.png"),u'Seçenekler', self)
	self.action_alwaysJoin = QtGui.QAction(u'Her Zaman', self)
	self.action_alwaysJoin.setCheckable(True)
	self.action_askToJoin = QtGui.QAction(u'Katılmadan Sor', self)
	self.action_askToJoin.setCheckable(True)
	self.action_rejectJoin = QtGui.QAction(u'Katılma', self)
	self.action_rejectJoin.setCheckable(True)
	
	
	self.trayMenu.addAction(self.action_options)
	self.trayMenu.addAction(self.action_quit)
	
        self.action_options.setMenu(self.optionsMenu)
        self.optionsGroup.addAction(self.action_alwaysJoin)
        self.optionsGroup.addAction(self.action_askToJoin)
        self.optionsGroup.addAction(self.action_rejectJoin)
        self.optionsMenu.addAction(self.action_alwaysJoin)
        self.optionsMenu.addAction(self.action_askToJoin)
        self.optionsMenu.addAction(self.action_rejectJoin)
        
	self.connect(self.action_quit, QtCore.SIGNAL("triggered()"),self.quit)
	self.connect(self.action_options,QtCore.SIGNAL("triggered()"), self.setActions)

	self.setDefaultOptions()
	
	self.connect(self.action_alwaysJoin, SIGNAL("triggered()"), self.setGlobalParticipation)
        self.connect(self.action_askToJoin, SIGNAL("triggered()"), self.setGlobalParticipation)
	self.connect(self.action_rejectJoin, SIGNAL("triggered()"), self.setGlobalParticipation)
  

	self.defaultIcon = QtGui.QIcon("../data/user_study.png")
	self.countIcon = QtGui.QIcon("")
	self.lastIcon = self.defaultIcon
	self.tray.setIcon(self.defaultIcon)
	self.tray.setContextMenu(self.trayMenu)
	self.tray.show()
	
	self.unread = 0    #number of updates
	
	self.tray.showMessage(u"User Study", u"There's a problem that I could not solve", QtGui.QSystemTrayIcon.Information, 8000)
	
	self.checkUpdates()
	
	self.tray.activated.connect(self.__activated)
    
    def __activated(self, reason):
	if not reason == QtGui.QSystemTrayIcon.Context:
	    if self.appWindow.isVisible():
		self.appWindow.hide()
	    else:
		self.appWindow.show()
		
    def quit(self):
	sys.exit()
    
    def setActions(self):
	pass
    
    def setDefaultOptions(self):
	json_data =  open('../../data/user_participation_info.json','r')
	self.data = json.load(json_data)
	json_data.close()
	
	if self.data["userParticipation"] == "Always Join":
	    self.action_alwaysJoin.setChecked(True)
	elif self.data["userParticipation"] == "Ask Before Join":
	    self.action_askToJoin.setChecked(True)
	else:
	    self.action_rejectJoin.setChecked(True)

    
    def checkUpdates(self):
	json_data =  open('../../data/user_studies.json','r')
	self.data = json.load(json_data)
	json_data.close()
	
	try:
	    json_local_data = urllib2.urlopen('http://cekirdek.pardus.org.tr/~bertan/user_studies.json')
	    self.local_data = json.load(json_local_data)
	except:
	    sys.exit()

	for survey in self.data["pardusUserStudyList"]:
	    surveyNum = survey["id"]

	for local_survey in self.local_data["pardusUserStudyList"]:
	    localSurveyNum = local_survey["id"]
	  
	if localSurveyNum > surveyNum:
	    diff = localSurveyNum - surveyNum
	    if diff > 1:
		self.tray.showMessage(u"New User Studies", u"There are %s new user studies" %(diff), QtGui.QSystemTrayIcon.Information, 8000)
	    else:
		self.tray.showMessage(u"New User Study", u"There is a new user study", QtGui.QSystemTrayIcon.Information, 8000)
	    f = open('../../data/user_studies.json','w')
	    string = json.dump(self.local_data,f, indent = 2)
	    f.close()
	
    def setGlobalParticipation(self):
	json_data =  open('../../data/user_participation_info.json','r')
	self.data = json.load(json_data)
	json_data.close()
	
	if self.action_alwaysJoin.isChecked() == True:
	    self.data["userParticipation"] = "Always Join"
	    self.appWindow.ui.alwaysHelp.setChecked(True)
	elif self.action_askToJoin.isChecked() == True:
	    self.data["userParticipation"] = "Ask Before Join" 
	    self.appWindow.ui.askToHelp.setChecked(True)
	else :
	    self.data["userParticipation"] = "Do not Join"
	    self.appWindow.ui.rejectHelp.setChecked(True)
	
	f = open('../../data/user_participation_info.json','w')
	string = json.dump(self.data,f, indent = 2)
	f.close()
 
