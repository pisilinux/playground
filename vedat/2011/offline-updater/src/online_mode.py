#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as tree
import urllib2
import lzma
import cPickle
import os
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox


from ui_online import Ui_Online 

class Online(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        
        self.ui = Ui_Online()
        self.ui.setupUi(self)

        self.ui.pb_action.clicked.connect(self.getUpdatedPackages)
        self.ui.pb_close.clicked.connect(self.close)
        self.ui.pb_path.clicked.connect(self.getDir)
        self.ui.pb_help.clicked.connect(self.showHelp)
        
        self.ui.le_path.setText(os.getenv('USERPROFILE') or os.getenv('HOME'))
        self.ui.lbl_file.setText("0/0")
        self.ui.lbl_progress.setText("%0")
        self.setWindowTitle("Pardus Offline-Updater")
        
        QtGui.QApplication.processEvents()
    
    def getDir(self):
        fd = QtGui.QFileDialog(self)
        self.path = fd.getExistingDirectory(parent=None, caption=u"Klasör seç", directory=self.ui.le_path.text(), options=QtGui.QFileDialog.ShowDirsOnly)
        self.ui.le_path.setText(self.path)
    
    def downloadRepoXML(self, repo):
        repo_ = file_name = repo.split('/')
        #print repo_
        file_name = file_name[4]+"_"+file_name[5]+"_"+file_name[6]+".xz"
        
        message = repo_[5]+ " deposu paket bilgileri indiriliyor."
        self.updateListWidget(message)
        QtGui.QApplication.processEvents()
        
        self.download(file_name, repo)
        try:
            xml_object = open(file_name, 'rb').read()
        except:
            self.errorMessage("Hata", u"Repo XML'i açılamadı. Lütfen tekrar deneyiniz.")
            return
        a = lzma.LZMADecompressor()
        str_object2 = a.decompress(xml_object)
        f = open(file_name+".xml", 'wb')
        f.write(str_object2)
        f.close()
        return file_name+".xml"
    
    def getRepos(self):
        try:
            return cPickle.load(open(self.ui.le_path.text()+"/repoList.ofu"))
        except IOError:                     
            self.errorMessage("Hata", "repoList.ofu bulunamadi !")
    
    def findDependency(self, i):
        dep_list = []
        dep_handler = i.find("RuntimeDependencies")
        if dep_handler:
            deps = dep_handler.findall("Dependency")
            for dep in deps:
                dep_list.append(dep.text)
                
        #print dep_list
        return dep_list
    
    def findReplaces(self, i):
        rep_list = [] #MAYBE: replace packages can be more than one
        rep_handler = i.find("Replaces")
        if rep_handler:
            reps = rep_handler.findall("Package")
            for rep in reps:
                rep_list.append(rep.text)
        #print rep_list
        return rep_list
    
    
    def parsePisiXML(self):
        repo_packages = {}
        QtGui.QApplication.processEvents()
        repos = self.getRepos()
        if not repos:
            return
        item = u"Repo bilgileri okunuyor.\n%s adet repo bilgisi alındı."%len(repos)
        
        self.updateListWidget(item)
        
        for repo in repos:
            QtGui.QApplication.processEvents()
            packages = {}
            obselete_list = []
            
            pisi_xml = self.downloadRepoXML(repos[repo]) #XML dosyalarını indir
            pisi_data = open(pisi_xml) #Aç
            message = repo+u" reposunun bilgileri çözümleniyor."
            self.updateListWidget(message)
            package_tree = tree.fromstring(pisi_data.read()) #XML dosyasını tree değişkenine aç
            packages_tree = package_tree.findall("Package") #tree içerisinden tüm Package taglerini çek
            obseletes = package_tree.find("Distribution").find("Obsoletes").findall("Package")
    
            for obsolete in obseletes:
                obselete_list.append(obsolete.text)
                
            for i in packages_tree:
                QtGui.QApplication.processEvents()
                dep_list = []
                history_handler = i.find("History") 
                name = i.find("Name").text
                release = history_handler.find("Update").get("release")
                version = history_handler.find("Update").find("Version").text
                #url
                url = repos[repo].strip("pisi-index.xml.xz") + i.find("PackageURI").text
                #/url
                #Replaces
                rep_list = self.findReplaces(i)
                #/Replaces
                #Dependencies
                dep_list = self.findDependency(i)
                #/Dependencies
                packages[name] = (release, repo, dep_list, version, rep_list, url)
            print "\n"    
            repo_packages[repo] = (packages, obselete_list) 
        return repo_packages
    
    
    def getInstalledPackages(self):
        try:
            return cPickle.load(open(self.ui.le_path.text()+"/packageList.ofu"))
        except IOError:
            self.errorMessage("Hata", u"packageList.ofu bulunamadı !")
    
    
    def getUpdatedPackages(self):
        
        
        installed_packages = self.getInstalledPackages()
        if not installed_packages:
            return
        repo_packages = self.parsePisiXML()
        self.updateListWidget("Kurulu paketlerin listesi okunuyor")
        
        QtGui.QApplication.processEvents()
        
        
        self.ui.pb_action.setEnabled(False)
        deplist = {}
        package_list = {}
        self.download_list = {}
        print "\n"
        self.updateListWidget(u"Paket güncellemeleri belirleniyor.")
        for ins_package in installed_packages:
            QtGui.QApplication.processEvents()
            
            for repo in repo_packages:
                for package in repo_packages[repo][0]:
                    if ins_package == package and repo_packages[repo][0][package][1] == installed_packages[ins_package][1]:
                        if int(repo_packages[repo][0][package][0]) > int(installed_packages[ins_package][0] or 
                             repo_packages[repo][0][package][3] > installed_packages[ins_package][3]):
                            if self.checkObsoletes(repo_packages[repo][1], package): 
                                isReplace = self.checkReplaces(repo_packages[repo][0][package][4], package, package_list)
                                if isReplace ==  None:
                                    #print "%d.Paket adi:%s\t repo:%s\t guncelV:%s\t simdikiV:%s"%(cnt, package, repo, repo_packages[repo][0][package][0],installed_packages[ins_package][0])
                                    self.download_list[package] = repo_packages[repo][0][package][5]
                                    for dep in repo_packages[repo][0][package][2]:
                                        deplist[dep] = repo_packages[repo][0][package][1]
                                else:
                                    self.download_list[package] = repo_packages[repo][0][isReplace][5]
            package_list[ins_package] = installed_packages[ins_package][1]
        deplist = self.checkDependencyUpdate(package_list, deplist, repo_packages)
        #print deplist
        for dep in deplist:
            self.download_list[dep] = repo_packages[deplist[dep]][0][dep][5]
       
        message = u"%s paket ve %s bagimlılık bulundu" %(int(len(self.download_list)-len(deplist)), len(deplist)) 
        self.updateListWidget(message)
        
        if len(self.download_list) == 0:
            message = u"Güncellenecek Paket Bulunamadı!"
            self.ui.updateListWidget(message)
            self.cleaningJobs()
            return
        
            
        
        
        self.ui.pb_action.hide()
        self.pb_action = QtGui.QPushButton(self)
        self.ui.gridLayout.addWidget(self.pb_action, 1, 1, 1, 3)
        self.pb_action.setText(QtGui.QApplication.translate("Offline", "İndirme işlemine başla", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_action.clicked.connect(self.processDownloadList)
    
    def checkDependencyUpdate(self, package_list, deplist, repo_packages):
        
        
        self.updateListWidget(u"Bağımlılıklar belirleniyor.")
        for i in package_list.keys():
            for j in deplist.keys():
                if i==j:
                    deplist.pop(i)
        
        
        new_deplist = self.checkRecursiveDeps(deplist, repo_packages)
        
        for i in package_list.keys():
            for j in new_deplist.keys():
                if i==j:
                    new_deplist.pop(i)
        
        deplist.update(new_deplist)
        return deplist
        
    
    def checkRecursiveDeps(self, deplist, repo_packages):
        
        deps = {}
        for dep in deplist:
            QtGui.QApplication.processEvents()
            for repo in repo_packages:
                for package in repo_packages[repo][0]:
                    if deplist[dep] == repo_packages[repo][0][package][1] and dep == package:
                        for new_dep in repo_packages[repo][0][package][2]:
                            deps[new_dep] = deplist[dep]
                       
        if not len(deps) == 0:
            deps.update(self.checkRecursiveDeps(deps, repo_packages))
        return deps
            
    def checkObsoletes(self, obselete_list, package):
        for obselete in obselete_list:
            if package == obselete:
                return False
            else:
                return True
        
    def checkReplaces(self, rep_list, package, package_list):
        for ins_package in package_list:
            for rep in rep_list:
                #print ins_package
                if ins_package == rep:
                    return package
                else:
                    return None
    
    def processDownloadList(self):
        try:
            workingDir = QtCore.QDir(self.ui.le_path.text())
            if not workingDir.mkdir("packages"):
                self.rmPackagesDir(workingDir.absolutePath()+"/packages")
            workingDir.mkdir("packages")
        except:
            self.errorMessage("Hata", u"Packages Klasorü oluşturulamadı !")
            return
        
        #disable ui objects
        self.ui.le_path.setEnabled(False)
        self.ui.pb_path.setEnabled(False)
        self.pb_action.setEnabled(False)
        
        sum = len(self.download_list)
        cnt = 1
        
        
        
        for package in self.download_list: #FIXED: Progress bar only shows the package count, must shows the download size based info.
            self.ui.lbl_file.setText(str(cnt)+"/"+str(sum))
            package_name = self.download_list[package].split('/')[7]
            QtGui.QApplication.processEvents()
            message = package+" paketi indiriliyor."
            self.updateListWidget(message)
            self.download(package_name, self.download_list[package], True)
            cnt += 1
            
        self.updateListWidget(u"Paketlerin indirilmesi tamamlandı.")
            
        #after work - enable ui objects
        self.ui.le_path.setEnabled(True)
        self.ui.pb_path.setEnabled(True)
        self.pb_action.setEnabled(True)
        self.ui.updateListWidget(u"Temizlik işlemleri yapılıyor.")
        self.cleaningJobs()
        self.ui.updateListWidget(u"İşlem tamamlandı.")    
            
    def rmPackagesDir(self, top):
        top = str(top)
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
            
    
    def download(self, file_name, url, isPackage=False):
        try:
            u = urllib2.urlopen(url)
        except:
            self.errorMessage("Hata", u"İnternet bağlantınızı kontrol ediniz !")
            return
        if (isPackage):
            workingDir = QtCore.QDir(self.ui.le_path.text())
            f = open(workingDir.absolutePath()+"/packages/"+file_name, 'wb')
        else:
            f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)
        
        file_size_dl = 0
        block_sz = 8192
        while True:
            QtGui.QApplication.processEvents()
            buffer = u.read(block_sz)
            if not buffer:
                break
        
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            #status = status + chr(8)*(len(status)+1)
            #print status,
            self.ui.lbl_progress.setText(status)
        f.close()
        
    def errorMessage(self, header, message):
        QMessageBox.critical(self,
                                header,
                                message)
        return False
    
    def cleaningJobs(self):
        for dirname, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                if filename.split(".")[-1] == "xz" or filename.split(".")[-1] == "xml":
                    os.remove(filename)
                    
    def updateListWidget(self, message):
        item = QtGui.QListWidgetItem(message)
        self.ui.listWidget.addItem(message)
        self.ui.listWidget.setCurrentItem(item)
    
    def showHelp(self):
        pass
    
    

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    OnlineMode = Online()
    OnlineMode.show()
    sys.exit(app.exec_())
