# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 21:52:58 2011

@author: Proprietario
"""

from PyQt4 import QtCore, QtGui

"""
Adds to a widget a custom context menu
"""
class FBContextMenu():
    
    def __init__(self, widget):
        self.widget = widget
        self.widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.widget.setCursor(QtCore.Qt.PointingHandCursor)
        self.callbacks = []
        self.menu = QtGui.QMenu("selezionare una voce", widget)
        QtCore.QObject.connect(widget, 
                               QtCore.SIGNAL("customContextMenuRequested(QPoint)"), 
                               self.on_customContextMenuRequested)
        
    def addItem(self, text, callback):
        action = QtGui.QAction(text, self.widget)
        action.setData(QtCore.QVariant(len(self.callbacks)))
        self.callbacks.append(callback)
        self.widget.connect(action, QtCore.SIGNAL("triggered()"), self.on_context_menu)
        self.menu.addAction(action)

    def addSeparator(self):
        self.menu.addSeparator()

    def getPoint(self):
        return self.point

    def on_customContextMenuRequested(self, point):
        print __name__, "on_customContextMenuRequested"
        self.point = point
        self.menu.exec_(self.widget.mapToGlobal(point))

    def on_context_menu(self):
        print __name__, "on_context_menu"
        action = self.widget.sender()
        index, isValid = action.data().toInt()
        self.callbacks[index](action.text(), self.widget)

