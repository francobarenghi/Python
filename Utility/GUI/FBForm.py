# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 16:34:47 2011

@author: FrancoB
"""

from PyQt4 import QtCore, QtGui
from Utility.Settings import Settings
import sys
import threading



class FBForm(QtGui.QDialog):

    def __init__(self, form, parent=None):
        #super(Derived, self).__init__(param) ############ da tenere a mente
        QtGui.QDialog.__init__(self)
        self.ui=form
        self.ui.setupUi(self)
        self.parent = parent
        self.restoreGeometry()
        self.fbw = None
        try:
            self.fbw = self.ui.layoutWidget
        except: pass
        if self.fbw == None:
            try:
                self.fbw = self.ui.widget
            except: pass
#        if self.fbw == None:
#            raise Exception("no top level widget identified")

    def hideEvent(self, event):
        self.saveGeometry()
        
    def getSettings(self):
        if self.parent is not None:
            return self.parent.getSettings()
        
    def getLocalSettings(self):
        if self.parent is not None:
            return self.parent.getLocalSettings()
        
    def saveGeometry(self):
        if self.parent is not None:
            #try:
                key = "Form/"+self.__module__
                settings = self.parent.getLocalSettings()
                settings.setNodeText("posx", str(self.pos().x()), path=key, create=True)
                settings.setNodeText("posy", str(self.pos().y()), path=key, create=True)
                settings.setNodeText("sizew", str(self.size().width()), path=key, create=True)
                settings.setNodeText("sizeh", str(self.size().height()), path=key, create=True)
            #except:
            #    print __name__, "saveGeometry", sys.exc_info()

    def restoreGeometry(self):
        if self.parent is not None:
            try:
                key = "Form/"+self.__module__
                settings = self.parent.getLocalSettings()
                x = int(settings.getNodeText( "posx", key))
                y = int(settings.getNodeText( "posy", key))
                x = x if x>0 else 0
                y = y if y>0 else 0
                w = int(settings.getNodeText( "sizew", key))
                h = int(settings.getNodeText( "sizeh", key))
                self.move(x, y)
                self.resize(w, h)
            except Settings.NonexistentNodeException:
                pass

    def message(self, text, title="Info", timeout=0.0):
        """
        Displays a message box
        """
        self.msg = FBMessage(QtGui.QMessageBox.Information,
            QtCore.QString(title),
            QtCore.QString(text),
            QtGui.QMessageBox.Ok)
        self.msg.exec_(timeout)

    def messageTimeoutCallback(self):
#        print __name__, "messageTimeoutCallback", threading.current_thread().ident
        if self.msg:
            self.msg.reject()
        

    def inputItemDialog(self, title, itemList):
        """
        Displays an input item dialog box: a dialog with a single selectable items list
        """
        ql = QtCore.QStringList()
        for item in itemList:
            ql.append(QtCore.QString(item))
        item, ok = QtGui.QInputDialog.getItem(self,
                                           title,
                                           "Please select one item:",
                                           ql,
                                           0,
                                           False)
        if ok and item:
            return str(item)
        return None


    def resizeEvent(self, event):
        if self.fbw:
            self.fbw.setGeometry(0, 0, self.geometry().width(), self.geometry().height())


class FBMessage(QtGui.QMessageBox):
    def __init__(self, *arg):
        super(FBMessage, self).__init__(*arg)
        #self.expired = QtCore.pyqtSignal()
        #self.expired.connect(self.onExpired)
        QtCore.QObject.connect(self,
            QtCore.SIGNAL("expired()"),
            self,
            QtCore.SLOT("onExpired()"),
            QtCore.Qt.QueuedConnection)

    def exec_(self, timeout):
        if timeout > 0:
            bt = self.button(QtGui.QMessageBox.Ok)
            bt.setEnabled(False)
            t = threading.Timer(timeout, self.messageTimeoutCallback)
            t.start()
        super(FBMessage, self).exec_()

    def messageTimeoutCallback(self):
#        print __name__, "messageTimeoutCallback", threading.current_thread().ident
        #self.expired.emit()
        self.emit(QtCore.SIGNAL("expired()"))

    @QtCore.pyqtSignature("onExpired()")
    def onExpired(self):
#        print __name__, "onExpired", threading.current_thread().ident
        self.reject()

