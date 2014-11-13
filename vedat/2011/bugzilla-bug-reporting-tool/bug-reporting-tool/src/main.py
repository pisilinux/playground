#!/usr/bin/python
# -*- coding: utf-8 -*-

import gettext
__trans = gettext.translation('bug-reporting-tool', fallback=True)
i18n = __trans.ugettext
import xmlrpclib
from BugReporterUI import Ui_BugReporter
from BugReporter import Bugs
import sys,os,subprocess
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox
import tempfile

class Main:
    def __init__(self):
        # Bug Data
        self.productList = []
        self.ui = None
        self.app = None
        self.bugs = Bugs()
        self.bugid= -1
        self.buginfo = []
        self.selectedindex = -1
        self.sysInfo = None
        self.userInfo = None



	    #create temporary directory for generic and specific command outpus
        self.tmpDir = tempfile.mkdtemp()

        self.genericCmdList = list()

        self.genericCmdList.append(['dmesg','dmesg.txt'])
        self.genericCmdList.append(['lspci -nnvv','lspci-nnvv.txt'])
        self.genericCmdList.append(['lsusb','lsusb.txt'])
        self.genericCmdList.append(['lsmod','lsmod.txt'])
        self.genericCmdList.append(['uname -a','uname-a.txt'])
        self.genericCmdList.append(['free -m','free-m.txt'])
        self.genericCmdList.append(['pisi lr','pisi-lr.txt'])

        self.genericLogList = list()

        self.genericLogList.append(['/proc/cmdline','proc-cmdline'])

        self.buginfo = list()
        self.buginfo.append({'productname':'Display','commandlist':self.genericCmdList[:],'loglist':self.genericLogList[:]})
        self.buginfo.append({'productname':'Storage','commandlist':self.genericCmdList[:],'loglist':self.genericLogList[:]})
        self.buginfo.append({'productname':'Sound/Audio','commandlist':self.genericCmdList[:],'loglist':self.genericLogList[:]})
        self.buginfo.append({'productname':'Other','commandlist':self.genericCmdList[:],'loglist':self.genericLogList[:]})

        #Display specific log and commands
        if os.path.exists('/var/log/Xorg.0.log'):
            self.buginfo[0]['loglist'].append(['/var/log/Xorg.0.log','var-log-xorg-0-log.txt'])

        if os.path.exists('/var/log/Xorg.0.log.old'):
            self.buginfo[0]['loglist'].append(['/var/log/Xorg.0.log.old','var-log-xorg-0-log-old.txt'])

        if os.path.exists('/var/log/Xorg.1.log'):
            self.buginfo[0]['loglist'].append(['/var/log/Xorg.1.log','var-log-xorg-1-log.txt'])

        if os.path.exists('/var/log/Xorg.1.log.old'):
            self.buginfo[0]['loglist'].append(['/var/log/Xorg.1.log.old','var-log-xorg-1-log-old.txt'])

        if os.path.exists(os.getenv('HOME')+'/.xsession-errors'):
            self.buginfo[0]['loglist'].append([os.getenv('HOME')+'/.xsession-errors','xsession-errors.txt'])


        #Storage specific log and commands
        self.buginfo[1]['commandlist'].append(['blkid','blkid.txt'])
        self.buginfo[1]['commandlist'].append(['fdisk -l','fdisk-l.txt'])

        if os.path.exists('/boot/grub/grub.conf'):
            self.buginfo[1]['loglist'].append(['/boot/grub/grub.conf','boot-grub-grub-conf.txt'])
        if os.path.exists('/proc/mounts'):
            self.buginfo[1]['loglist'].append(['/proc/mounts','proc-mounts.txt'])

        print 'tempdir = ' + self.tmpDir

    def getLogsIntoTempDir(self,bugtype):
        for log in self.buginfo[bugtype]['loglist']:
            print log
            subprocess.call('cp '+log[0]+' '+self.tmpDir+'/'+log[1],shell=True)

        for cmd in self.buginfo[bugtype]['commandlist']:
            print cmd
            subprocess.call(cmd[0]+' > '+self.tmpDir+'/'+cmd[1],shell=True)

    def showMessage(self,title,message):
        msgBox = QMessageBox(self.ui.stackedWidget)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.show()

    def goto_next_page(self):
        index = self.ui.stackedWidget.currentIndex()
        if index == 2:
            if len(str(self.ui.txtSummary.toPlainText())) < 8:
                self.showMessage(i18n("Warning"),i18n("Summary can not be less than 8 characters !"))
                return

            # TODO Text may contain only space character. Check if the text is acceptable
            if len(str(self.ui.txtDetails.toPlainText()).split(' ')) < 10:
                self.showMessage(i18n("Warning"),i18n("Detail can not be less than 10 words !"))
                return
        index = index + 1
        if index == 3:
            self.previewBug()
        self.ui.stackedWidget.setCurrentIndex(index)

    def goto_prev_page(self):
        index = self.ui.stackedWidget.currentIndex()
        if index==5:
            index = index-2
        else:
            index = index - 1
        self.ui.stackedWidget.setCurrentIndex(index)

    def create_actions(self):
        self.ui.btnNextPage1.clicked.connect(self.goto_next_page)
        self.ui.btnNextPage2.clicked.connect(self.goto_next_page)
        self.ui.btnNextPage3.clicked.connect(self.goto_next_page)
        self.ui.btnBackPage2.clicked.connect(self.goto_prev_page)
        self.ui.btnBackPage3.clicked.connect(self.goto_prev_page)
        self.ui.btnBackPage4.clicked.connect(self.goto_prev_page)
        self.ui.btnBackPage6.clicked.connect(self.goto_prev_page)
        self.ui.btnLogin.clicked.connect(self.login)
        self.ui.btnQuitPage5.clicked.connect(self.quit_window)
        self.ui.btnQuitPage6.clicked.connect(self.quit_window)
        self.ui.btnCancelPage1.clicked.connect(self.quit_window)
        self.ui.btnSendPage4.clicked.connect(self.sendBug)
    def quit_window(self):
        sys.exit()
    def login(self):
        user = str(self.ui.txtMail.toPlainText())
        password = str(self.ui.txtPassword.toPlainText())
        if not self.bugs.login(user,password):
            self.showMessage(i18n("Error"),i18n("Authentication failed. Check your e-mail and password and try again..."))
        else:
            self.goto_prev_page()
    def show(self):
        # Creates actions by assigning signals to slots
        self.app = QtGui.QApplication(sys.argv)
        BugReporter = QtGui.QMainWindow()
        self.ui = Ui_BugReporter()
        self.ui.setupUi(BugReporter)
        self.create_actions()
        self.createProducts()
        BugReporter.show()
        sys.exit(self.app.exec_())

    def createProducts(self):
        # Produce info about bugs
        self.productList.append(self.ui.rbDisplay)
        self.productList.append(self.ui.rbStorage)
        self.productList.append(self.ui.rbSoundAudio)
        self.productList.append(self.ui.rbOthers)

    def setProduct(self):
        '''
        sets selected product
        '''
        for but in self.productList:
            if but.isChecked():
               self.selectedindex = self.productList.index(but)
    def getProduct(self):
        '''
        returns selected product name
        '''
        product = self.buginfo[self.selectedindex]['productname']
        return product
    
    def get_sys_info(self):
        '''
        returns a data type of dict containing system information to be sent to the bug
        platform 
        '''
        import platform
        data = {}
        #find component
        component = "unspecified"
        data['component'] = component

        # find version
        version = platform.dist()[1]
        if "Kurumsal" in version or "Corporate" in version:
            substr = version.split(" ")
            version = "Corporate"+substr[1]
        else :
            substr = version.split(".")
            version = substr[0]
        data['version'] = version

        #find platform
        plat = platform.uname()[4]
        data['platform'] = plat

        return data

    def previewBug(self):
        '''
        Preview the bug information
        '''
        # set User Info
        self.setProduct()
        self.userInfo= {}
        self.userInfo['product'] = self.getProduct()
        self.userInfo['summary'] = str(self.ui.txtSummary.toPlainText())
        self.userInfo['description'] = str(self.ui.txtDetails.toPlainText()) +  "\n" + str(self.ui.txtSteps.toPlainText())
        # set system Info
        self.sysInfo = {} 
        self.sysInfo = self.get_sys_info()
	
	# run commands and copy outputs to temp directory
	self.getLogsIntoTempDir(self.selectedindex)



        self.ui.treeWidget.headerItem().setText(0, i18n("Fields"))
        self.ui.treeWidget.headerItem().setText(1, i18n("Data"))
        __sortingEnabled = self.ui.treeWidget.isSortingEnabled()
        self.ui.treeWidget.setSortingEnabled(False)
        self.ui.treeWidget.topLevelItem(0).setText(0, i18n("Architecture"))


        self.ui.treeWidget.topLevelItem(0).child(0).setText(0, i18n("OS"))

        self.ui.treeWidget.topLevelItem(0).child(0).setText(1, i18n("Pardus " + self.sysInfo['version']))
       
       
       
        self.ui.treeWidget.topLevelItem(0).child(1).setText(0, i18n("Platform"))
        
        self.ui.treeWidget.topLevelItem(0).child(1).setText(1, i18n(self.sysInfo['platform']))



        self.ui.treeWidget.topLevelItem(1).setText(0, i18n("User Data"))


        self.ui.treeWidget.topLevelItem(1).child(0).setText(0, i18n("Problem Type"))

        self.ui.treeWidget.topLevelItem(1).child(0).setText(1, i18n(self.userInfo['product']))


        self.ui.treeWidget.topLevelItem(1).child(1).setText(0, i18n("Summary")) 

        self.ui.treeWidget.topLevelItem(1).child(1).setText(1, i18n(self.userInfo['summary']))

        
        self.ui.treeWidget.topLevelItem(1).child(2).setText(0, i18n("Description"))

        self.ui.treeWidget.topLevelItem(1).child(2).setText(1, i18n(self.userInfo['description']))
       
        self.ui.treeWidget.topLevelItem(2).setText(0, i18n("System Data"))
	self.ui.treeWidget.topLevelItem(2).child(0).setText(0, i18n("Command Outputs"))    
	
	i=0
	for elem in self.buginfo[self.selectedindex]['commandlist']:
	    item_0 = QtGui.QTreeWidgetItem(self.ui.treeWidget.topLevelItem(2).child(0))
	    item_0.setText(0, i18n(elem[0]))
	    item_0.setText(1, i18n(self.tmpDir + '/' + elem[1]))
        i += 1


	self.ui.treeWidget.topLevelItem(2).child(1).setText(0, i18n("Log Files"))    
	i=0
	for elem in self.buginfo[self.selectedindex]['loglist']:
	    item_1 = QtGui.QTreeWidgetItem(self.ui.treeWidget.topLevelItem(2).child(1))
	    item_1.setText(0, i18n(elem[0] ))    
	    item_1.setText(1, i18n(self.tmpDir + '/' + elem[1]))
        i += 1
       
       
        self.ui.treeWidget.setSortingEnabled(__sortingEnabled)
    def getFault(self,fault):
        return int(str(fault).split(' ')[1].split(':')[0])
    def sendBug(self):

        try:
            r = self.bugs.createbug(self.userInfo,self.sysInfo)
            self.bugid = str(r).split(' ')[0].split('#')[1]
        except xmlrpclib.Fault,e:
            fault = self.getFault(e) 
            if fault == 410:
                self.goto_next_page()
                self.goto_next_page()
            self.bugid=-1
        if self.bugid > 0:
            try:
                self.attachbug()
            except xmlrpclib.Fault,e:
                self.showMessage(i18n("Error"),str(e))
                return
            self.ui.lblBugID.setText(str(self.bugid))
            url = self.bugs.getBuzillaURL().rstrip('xmlrpc.cgi')
            self.ui.lblLinkToBug.setText("<a href='"+ url +"show_bug.cgi?id=" + self.bugid + "'>" +url+"show_bug.cgi?id="+self.bugid+"</a>")
            self.goto_next_page()
    def run(self, cmd, logfile):
        '''
        Execute given commands and redirect them to a file named as 'commandname' + '.txt'
        File name is given as a parameter to the function 
        '''
        import os
        cmd = cmd + " > " + logfile
        os.system(cmd)
    def attachbug(self):
        '''
        '''
        import dircache
        if self.bugid and self.bugid < 0:
            return
        for fname in dircache.listdir(self.tmpDir):
            fdesc = fname
            self.bugs.attach_file(self.bugid,self.tmpDir + "/" + fname,fdesc)
if __name__ == "__main__":
    m=Main()
    m.show()
 
