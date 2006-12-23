# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'db_connect.ui'
#
# Created: Sat Dec 23 09:23:29 2006
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_dbConnectionDialog(object):
    def setupUi(self, dbConnectionDialog):
        dbConnectionDialog.setObjectName("dbConnectionDialog")
        dbConnectionDialog.resize(QtCore.QSize(QtCore.QRect(0,0,316,243).size()).expandedTo(dbConnectionDialog.minimumSizeHint()))
        dbConnectionDialog.setModal(True)

        self.layoutWidget = QtGui.QWidget(dbConnectionDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20,250,351,33))
        self.layoutWidget.setObjectName("layoutWidget")

        self.layoutWidget1 = QtGui.QWidget(dbConnectionDialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(10,200,295,34))
        self.layoutWidget1.setObjectName("layoutWidget1")

        self.hboxlayout = QtGui.QHBoxLayout(self.layoutWidget1)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(131,31,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.okButton = QtGui.QPushButton(self.layoutWidget1)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)

        self.cancelButton = QtGui.QPushButton(self.layoutWidget1)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout.addWidget(self.cancelButton)

        self.widget = QtGui.QWidget(dbConnectionDialog)
        self.widget.setGeometry(QtCore.QRect(10,10,291,183))
        self.widget.setObjectName("widget")

        self.gridlayout = QtGui.QGridLayout(self.widget)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.dbDriver = QtGui.QComboBox(self.widget)
        self.dbDriver.setObjectName("dbDriver")
        self.gridlayout.addWidget(self.dbDriver,0,1,1,1)

        self.dbHost = QtGui.QLineEdit(self.widget)
        self.dbHost.setObjectName("dbHost")
        self.gridlayout.addWidget(self.dbHost,4,1,1,1)

        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,1,0,1,1)

        self.dbName = QtGui.QLineEdit(self.widget)
        self.dbName.setObjectName("dbName")
        self.gridlayout.addWidget(self.dbName,1,1,1,1)

        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,4,0,1,1)

        self.userName = QtGui.QLineEdit(self.widget)
        self.userName.setObjectName("userName")
        self.gridlayout.addWidget(self.userName,2,1,1,1)

        self.dbPort = QtGui.QLineEdit(self.widget)
        self.dbPort.setObjectName("dbPort")
        self.gridlayout.addWidget(self.dbPort,5,1,1,1)

        self.password = QtGui.QLineEdit(self.widget)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName("password")
        self.gridlayout.addWidget(self.password,3,1,1,1)

        self.label_6 = QtGui.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.gridlayout.addWidget(self.label_6,0,0,1,1)

        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,2,0,1,1)

        self.label_5 = QtGui.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.gridlayout.addWidget(self.label_5,5,0,1,1)

        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,3,0,1,1)

        self.retranslateUi(dbConnectionDialog)
        QtCore.QObject.connect(self.okButton,QtCore.SIGNAL("clicked()"),dbConnectionDialog.accept)
        QtCore.QObject.connect(self.cancelButton,QtCore.SIGNAL("clicked()"),dbConnectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dbConnectionDialog)
        dbConnectionDialog.setTabOrder(self.dbName,self.userName)
        dbConnectionDialog.setTabOrder(self.userName,self.password)
        dbConnectionDialog.setTabOrder(self.password,self.dbHost)
        dbConnectionDialog.setTabOrder(self.dbHost,self.dbPort)
        dbConnectionDialog.setTabOrder(self.dbPort,self.okButton)
        dbConnectionDialog.setTabOrder(self.okButton,self.cancelButton)

    def retranslateUi(self, dbConnectionDialog):
        dbConnectionDialog.setWindowTitle(QtGui.QApplication.translate("dbConnectionDialog", "Database Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("dbConnectionDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("dbConnectionDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("dbConnectionDialog", "Database Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.dbName.setText(QtGui.QApplication.translate("dbConnectionDialog", "refdb", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("dbConnectionDialog", "Database Host:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("dbConnectionDialog", "Driver:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("dbConnectionDialog", "Username:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("dbConnectionDialog", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("dbConnectionDialog", "Password:", None, QtGui.QApplication.UnicodeUTF8))
