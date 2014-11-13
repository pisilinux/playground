#!/usr/bin/python
# -*- coding: utf-8 -*-

import bugzilla, optparse
import bugzilla.util
import xmlrpclib
import os, sys,logging
import magic
# Class for reporting bugs. This class will enable to login to
# bugzilla and simply manage the bugs and enter new bugs

class Bugs:
    '''
    This is the class for reporting bugs to bugzilla
    Allows users to login to the specified bugzilla
                    create a new bug 
                    add attachment to a bug
                    logout from bugzilla
    '''
    def __init__(self,bzclass=None,version=None,URL=None):
        '''
        Initializes the required fields for Bugzilla
        Parameters
            bzclass (has default value): the class that specify the bugzilla version that is in use
            version (has default value):
            URL     (has default value): URL of bugzilla
        '''
        default_version= '0.6.2'
        default_bzclass = bugzilla.Bugzilla4
        self.default_bz = 'http://192.168.4.86/bugzilla/xmlrpc.cgi'
        last_added_bug = None
        user = None
        password = None
        cookiefile = None
        isLoggedin = False

        #Initializes the bugzilla class to the specified bugzilla version in use
        # Which version of the bugzilla we are using
        # This class is implemented in /usr/lib/python2.7/site-packages/bugzilla/bugzilla3.py file
        if not bzclass :
            self.bzclass=default_bzclass
        else:
            self.bzclass=bzclass
        #Initializes the bugzilla version that is in use
        if not version:
            self.version=default_version
        else:
            self.version=version

        #Initializes the bugzilla server URL that is in use
        if not URL:
            self.bz = self.bzclass(url=self.default_bz)
        else:
            self.bz = self.bzclass(url=URL)


    def login(self,username,password):
        '''
        Login to bugzilla with given username and password
        Parameters
            username : username(e-mail) of the user to login
            password : password of the user to login
        '''
        self.user=username
        self.password=password
        if not self.user:
            return False
        if not self.password:
            return False

        self.isLoggedin  = self.bz.login(self.user,self.password)

        return self.isLoggedin

    def getcookiefile(self):
        '''
        Returns the cookie file that keeps login info
        '''
        return self.cookiefile

    def logout(self):
        '''
        Logout already logged in user from bugilla
        '''
        self.bz.logout()
        self.isLoggedin = False
        print "Successfully logged out"

    def createbug(self,userInfo,sysInfo,severity=None,priority=None,op_sys=None,assigned_to=None,qa_contact=None,cc=None,status=None):
        '''
        Allows to create a new bug entry by logged in user
        Parameter data contains the followings
        REQUIRED:
            product: bug type
            summary:
            description:
        DEFAULTED:
            component:
            version:
            platform:
            severity:
            priority:
            op_sys:
        OPTIONAL:
            assigned_to:
            qa_contact:
            cc:
            status:
        '''

        # get system information
        sysdata=sysInfo

        data={}
        data['product'] = userInfo['product']
        data['component'] = sysdata['component']
        data['version'] = sysdata['version']
        data['summary'] = userInfo['summary']
        data['description'] = userInfo['description']
        data['rep_platform'] = sysdata['platform']

        if severity is not None:
            data['severity'] = severity
        else:
            data['severity'] = 'medium'
        if priority is not None:
            data['priority'] = priority
        else:
            data['priority'] = 'Normal'
        if op_sys is not None:
            data['op_sys'] = op_sys
        else:
            data['op_sys'] = 'Linux'
        if assigned_to is not None:
            data['assigned_to'] = assigned_to

        if qa_contact is not None:
            data['qa_contact'] = qa_contact

        if cc is not None:
            data['cc'] = cc
        if status is not None:
            data['status'] = status

        self.last_added_bug  =  self.bz.createbug(**data)
        self.last_added_bug.refresh()

        return self.last_added_bug

    def attach_file(self,bugid,filepath,desc):
        '''
        Allows users to attach a file to a bug 
        In order to attach multiple files, should be called for each file
        Parameters
            bugid       : determines which bug to attach file
            filepath    : path of the file to be attached
            desc        : description for the attachment
        '''
        if not os.path.exists(filepath):
            print "File does not exist!"
            return

        # Determine mime type of the file
        mimemagic = magic.open(magic.MAGIC_MIME)
        mimemagic.load()
        filetype = mimemagic.file(filepath)
        fileobj = open(filepath)

        # Returns the final component of a pathname
        filename = os.path.basename(filepath)

        # arguments of type dict containing filename, contenttype and filetype
        args = {'filename':filename,'contenttype':filetype,'ispatch':(filetype == 'text/x-patch')}

        attid = self.bz.attachfile(bugid, fileobj, desc,**args)
        print "Created attachment %s on bug %s" % (attid, bugid)

        return attid

    def getBuzillaURL(self):
        return self.default_bz

# End of BugReporter class
