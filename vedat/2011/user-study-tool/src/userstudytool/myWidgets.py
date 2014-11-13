#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtCore import *

from pds.gui import *

from ui_surveyItem import Ui_SurveyItemWidget

import sys

class SurveyItem(QtGui.QListWidgetItem):

    def __init__(self, titleItem, parent):
        QtGui.QListWidgetItem.__init__(self, parent)

        self.titleItem = titleItem

class SurveyItemWidget(QtGui.QWidget):

    def __init__(self, titleItem, parent, item, surveyList):
        QtGui.QWidget.__init__(self, None)

        self.ui = Ui_SurveyItemWidget()
        self.ui.setupUi(self)
        
        self.root = parent
        self.item = item
        self.titleItem = titleItem
        self.surveyList = surveyList
        self.ui.label.setText(titleItem)
        
    def showDescription(self):
	self.surveyList.setCurrentItem(self.item)
	self.root.showDescription(self.item.url)
    
        