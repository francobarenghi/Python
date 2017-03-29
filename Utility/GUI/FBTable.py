# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 18:41:19 2011

@author: Proprietario
"""

from PyQt4 import QtCore, QtGui
import new



def FBExtendTableWidget(qtTableWidget):
    qtTableWidget.FBFlags = QtCore.Qt.ItemIsSelectable |\
                            QtCore.Qt.ItemIsEditable |\
                            QtCore.Qt.ItemIsDragEnabled |\
                            QtCore.Qt.ItemIsDropEnabled |\
                            QtCore.Qt.ItemIsUserCheckable |\
                            QtCore.Qt.ItemIsEnabled |\
                            QtCore.Qt.ItemIsTristate

    def setItemString(self, row, col, text, color=QtCore.Qt.white):
        if qtTableWidget.cellWidget(row,col) is None:
            obj = QtGui.QTableWidgetItem(QtCore.QString(str(text)))
            obj.setBackground(QtGui.QBrush(QtGui.QColor(color)))
            obj.setFlags(self.FBFlags)
            qtTableWidget.setItem( row, col, obj)
        else:
            index = qtTableWidget.cellWidget(row,col).findText(text)
            if index >= 0:
                qtTableWidget.cellWidget(row,col).setCurrentIndex(index)

    def getItemString(self, row, col):
        if qtTableWidget.cellWidget(row,col) is None:
            if qtTableWidget.item(row, col) is not None:
                return qtTableWidget.item(row, col).data(QtCore.Qt.DisplayRole).toString().trimmed()
        else:
            return qtTableWidget.cellWidget(row,col).currentText()
        #print __name__,"getItemString", type(qtTableWidget.cellWidget(row,col))

    def setItemCombo(self, row, col, comboItemList, defaultItem=None):
        cb = QtGui.QComboBox(qtTableWidget)
        for item in comboItemList:
            cb.addItem(QtCore.QString(item))
        qtTableWidget.setCellWidget(row, col, cb)
        if defaultItem is not None:
            qtTableWidget.setItemString(row, col, defaultItem)
        #self.cellWidget(row, col).setFlags(self.FBFlags)

    def clearRow(self, row):
        for col in range(qtTableWidget.columnCount()):
            qtTableWidget.setItemString(row, col, "")

    def swapRows(self, row1, row2):
        rows = qtTableWidget.rowCount()
        if row1 < 0 or row2 < 0 or row1 >= rows or row2 >= rows:
            # invalid parameters
            return
        for col in range(qtTableWidget.columnCount()):
            tmp1 = self.getItemString(row1, col)
            tmp2 = self.getItemString(row2, col)
            self.setItemString(row1, col, tmp2)
            self.setItemString(row2, col, tmp1)
            selected = self.currentRow()
            if selected == row1: self.setCurrentCell(row2, 0)
            elif selected == row1: self.setCurrentCell(row2, 0)

    def clearAll(self):
        rows = qtTableWidget.rowCount()
        for row in xrange(rows):
            qtTableWidget.removeRow(rows-row-1)
        cols = qtTableWidget.columnCount()
        for col in xrange(cols):
            qtTableWidget.removeColumn(cols-col-1)

    def configItemsFlags(self, flags):
        self.FBFlags = flags
#        rows = qtTableWidget.rowCount()
#        cols = qtTableWidget.columnCount()
#        for row in xrange(rows):
#            for col in xrange(cols):
#                item = self.item(row, col)
#                f = item.flags()
#                item.setFlags(f ^ flags)


    qtTableWidget.setItemString   = new.instancemethod(setItemString,   qtTableWidget, qtTableWidget.__class__)
    qtTableWidget.getItemString   = new.instancemethod(getItemString,   qtTableWidget, qtTableWidget.__class__)
    qtTableWidget.setItemCombo    = new.instancemethod(setItemCombo,    qtTableWidget, qtTableWidget.__class__)
    qtTableWidget.clearRow        = new.instancemethod(clearRow,        qtTableWidget, qtTableWidget.__class__)
    qtTableWidget.swapRows        = new.instancemethod(swapRows,        qtTableWidget, qtTableWidget.__class__)
    qtTableWidget.clearAll        = new.instancemethod(clearAll,        qtTableWidget, qtTableWidget.__class__)
    qtTableWidget.configItemsFlags= new.instancemethod(configItemsFlags,qtTableWidget, qtTableWidget.__class__)
    return qtTableWidget
   





























class FBTable(QtGui.QTableWidget):
    """
    TableWidget facilities
    """
    
    def __init__(self, tableWidget):
        self = tableWidget

    def setItemString(self, row, col, text, color=QtCore.Qt.white):
        obj = QtGui.QTableWidgetItem(QtCore.QString(str(text)))
        obj.setBackground(QtGui.QBrush(QtGui.QColor(color)))
        self.setItem( row, col, obj)                                                          

    def getItemString(self, row, col):
        return self.item(row, col).data(QtCore.Qt.DisplayRole).toString().trimmed()

    def clearRow(self, row):
        for col in range(self.columnCount()):
            self.setItemString(row, col, "")

    #---------------------------------------------------------------------------
#    def currentRow(self):
#        return self.table.currentRow()
#
#    def setColumnCount(self, columns):
#        return self.table.setColumnCount(columns)
#
#    def setHorizontalHeaderLabels(self, labels):
#        return self.table.setHorizontalHeaderLabels(labels)
#
#    def setRowCount(self, rows):
#        return self.table.setRowCount(rows)
#        
#    def removeRow(self, row):
#        return self.table.removeRow(row)
#
#    def insertRow(self, row):
#        return self.table.insertRow(row)
#
#    def rowCount(self):
#        return self.table.rowCount()
#
#    def setContextMenuPolicy(self, ctxMenu):
#        return self.table.setContextMenuPolicy(ctxMenu)
#
#    def setCursor(self, cursor):
#        return self.table.setCursor(cursor)



#-------------------------------------------------------------------
if __name__ == "__main__":
    pass
#    #import sys
#    app = QtGui.QApplication(sys.argv)
#    qtT = QtGui.QTableWidget(2, 4, None)
#    ext = FBTable(qtT)
#    ext.setItemString(0,0,"tttt")
#    ext.setColumnCount(3)