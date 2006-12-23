# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bibentry_form.ui'
#
# Created: Sun Sep 10 14:47:58 2006
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_bibEntryForm(object):
    def setupUi(self, bibEntryForm):
        bibEntryForm.setObjectName("bibEntryForm")
        bibEntryForm.resize(QtCore.QSize(QtCore.QRect(0,0,502,621).size()).expandedTo(bibEntryForm.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(bibEntryForm)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label_2_2 = QtGui.QLabel(bibEntryForm)
        self.label_2_2.setObjectName("label_2_2")
        self.hboxlayout.addWidget(self.label_2_2)

        self.citekeyEdit = QtGui.QLineEdit(bibEntryForm)
        self.citekeyEdit.setObjectName("citekeyEdit")
        self.hboxlayout.addWidget(self.citekeyEdit)

        self.generateKeyButton_2 = QtGui.QPushButton(bibEntryForm)
        self.generateKeyButton_2.setObjectName("generateKeyButton_2")
        self.hboxlayout.addWidget(self.generateKeyButton_2)

        self.typeBox = QtGui.QComboBox(bibEntryForm)
        self.typeBox.setObjectName("typeBox")
        self.hboxlayout.addWidget(self.typeBox)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.label = QtGui.QLabel(bibEntryForm)
        self.label.setObjectName("label")
        self.hboxlayout2.addWidget(self.label)

        spacerItem = QtGui.QSpacerItem(141,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem)
        self.vboxlayout1.addLayout(self.hboxlayout2)

        self.authorsEdit = QtGui.QTextEdit(bibEntryForm)
        self.authorsEdit.setTabChangesFocus(True)
        self.authorsEdit.setObjectName("authorsEdit")
        self.vboxlayout1.addWidget(self.authorsEdit)
        self.hboxlayout1.addLayout(self.vboxlayout1)

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.label_3 = QtGui.QLabel(bibEntryForm)
        self.label_3.setObjectName("label_3")
        self.hboxlayout3.addWidget(self.label_3)

        spacerItem1 = QtGui.QSpacerItem(191,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout3.addItem(spacerItem1)
        self.vboxlayout2.addLayout(self.hboxlayout3)

        self.editorsEdit = QtGui.QTextEdit(bibEntryForm)
        self.editorsEdit.setTabChangesFocus(True)
        self.editorsEdit.setObjectName("editorsEdit")
        self.vboxlayout2.addWidget(self.editorsEdit)
        self.hboxlayout1.addLayout(self.vboxlayout2)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.vboxlayout3 = QtGui.QVBoxLayout()
        self.vboxlayout3.setMargin(0)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setMargin(0)
        self.hboxlayout4.setSpacing(6)
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.label_4 = QtGui.QLabel(bibEntryForm)
        self.label_4.setObjectName("label_4")
        self.hboxlayout4.addWidget(self.label_4)

        spacerItem2 = QtGui.QSpacerItem(401,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout4.addItem(spacerItem2)
        self.vboxlayout3.addLayout(self.hboxlayout4)

        self.titleEdit = QtGui.QTextEdit(bibEntryForm)
        self.titleEdit.setMaximumSize(QtCore.QSize(16777215,50))
        self.titleEdit.setTabChangesFocus(True)
        self.titleEdit.setObjectName("titleEdit")
        self.vboxlayout3.addWidget(self.titleEdit)
        self.vboxlayout.addLayout(self.vboxlayout3)

        self.vboxlayout4 = QtGui.QVBoxLayout()
        self.vboxlayout4.setMargin(0)
        self.vboxlayout4.setSpacing(6)
        self.vboxlayout4.setObjectName("vboxlayout4")

        self.hboxlayout5 = QtGui.QHBoxLayout()
        self.hboxlayout5.setMargin(0)
        self.hboxlayout5.setSpacing(6)
        self.hboxlayout5.setObjectName("hboxlayout5")

        self.label_11 = QtGui.QLabel(bibEntryForm)
        self.label_11.setObjectName("label_11")
        self.hboxlayout5.addWidget(self.label_11)

        spacerItem3 = QtGui.QSpacerItem(331,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout5.addItem(spacerItem3)
        self.vboxlayout4.addLayout(self.hboxlayout5)

        self.collectionTitleEdit = QtGui.QTextEdit(bibEntryForm)
        self.collectionTitleEdit.setMaximumSize(QtCore.QSize(16777215,50))
        self.collectionTitleEdit.setObjectName("collectionTitleEdit")
        self.vboxlayout4.addWidget(self.collectionTitleEdit)
        self.vboxlayout.addLayout(self.vboxlayout4)

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.label_10 = QtGui.QLabel(bibEntryForm)
        self.label_10.setObjectName("label_10")
        self.gridlayout.addWidget(self.label_10,2,2,1,1)

        self.label_8 = QtGui.QLabel(bibEntryForm)
        self.label_8.setObjectName("label_8")
        self.gridlayout.addWidget(self.label_8,1,2,1,1)

        self.label_6 = QtGui.QLabel(bibEntryForm)
        self.label_6.setObjectName("label_6")
        self.gridlayout.addWidget(self.label_6,0,2,1,1)

        self.journalLabel = QtGui.QLabel(bibEntryForm)
        self.journalLabel.setObjectName("journalLabel")
        self.gridlayout.addWidget(self.journalLabel,0,0,1,1)

        self.label_7 = QtGui.QLabel(bibEntryForm)
        self.label_7.setObjectName("label_7")
        self.gridlayout.addWidget(self.label_7,1,0,1,1)

        self.journalEdit = QtGui.QLineEdit(bibEntryForm)
        self.journalEdit.setObjectName("journalEdit")
        self.gridlayout.addWidget(self.journalEdit,0,1,1,1)

        self.yearEdit = QtGui.QLineEdit(bibEntryForm)
        self.yearEdit.setObjectName("yearEdit")
        self.gridlayout.addWidget(self.yearEdit,2,3,1,1)

        self.volumeEdit = QtGui.QLineEdit(bibEntryForm)
        self.volumeEdit.setObjectName("volumeEdit")
        self.gridlayout.addWidget(self.volumeEdit,0,3,1,1)

        self.editionEdit = QtGui.QLineEdit(bibEntryForm)
        self.editionEdit.setObjectName("editionEdit")
        self.gridlayout.addWidget(self.editionEdit,2,1,1,1)

        self.pagesEdit = QtGui.QLineEdit(bibEntryForm)
        self.pagesEdit.setObjectName("pagesEdit")
        self.gridlayout.addWidget(self.pagesEdit,1,3,1,1)

        self.numberEdit = QtGui.QLineEdit(bibEntryForm)
        self.numberEdit.setObjectName("numberEdit")
        self.gridlayout.addWidget(self.numberEdit,1,1,1,1)

        self.label_2 = QtGui.QLabel(bibEntryForm)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,2,0,1,1)
        self.vboxlayout.addLayout(self.gridlayout)

        self.vboxlayout5 = QtGui.QVBoxLayout()
        self.vboxlayout5.setMargin(0)
        self.vboxlayout5.setSpacing(6)
        self.vboxlayout5.setObjectName("vboxlayout5")

        self.hboxlayout6 = QtGui.QHBoxLayout()
        self.hboxlayout6.setMargin(0)
        self.hboxlayout6.setSpacing(6)
        self.hboxlayout6.setObjectName("hboxlayout6")

        self.label_9 = QtGui.QLabel(bibEntryForm)
        self.label_9.setObjectName("label_9")
        self.hboxlayout6.addWidget(self.label_9)

        spacerItem4 = QtGui.QSpacerItem(401,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout6.addItem(spacerItem4)
        self.vboxlayout5.addLayout(self.hboxlayout6)

        self.abstractEdit = QtGui.QTextEdit(bibEntryForm)
        self.abstractEdit.setTabChangesFocus(True)
        self.abstractEdit.setObjectName("abstractEdit")
        self.vboxlayout5.addWidget(self.abstractEdit)
        self.vboxlayout.addLayout(self.vboxlayout5)

        self.hboxlayout7 = QtGui.QHBoxLayout()
        self.hboxlayout7.setMargin(0)
        self.hboxlayout7.setSpacing(6)
        self.hboxlayout7.setObjectName("hboxlayout7")

        spacerItem5 = QtGui.QSpacerItem(231,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout7.addItem(spacerItem5)

        self.submitButton = QtGui.QPushButton(bibEntryForm)
        self.submitButton.setObjectName("submitButton")
        self.hboxlayout7.addWidget(self.submitButton)

        self.cancelButton = QtGui.QPushButton(bibEntryForm)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout7.addWidget(self.cancelButton)
        self.vboxlayout.addLayout(self.hboxlayout7)

        self.retranslateUi(bibEntryForm)
        QtCore.QMetaObject.connectSlotsByName(bibEntryForm)
        bibEntryForm.setTabOrder(self.citekeyEdit,self.typeBox)
        bibEntryForm.setTabOrder(self.typeBox,self.authorsEdit)
        bibEntryForm.setTabOrder(self.authorsEdit,self.editorsEdit)
        bibEntryForm.setTabOrder(self.editorsEdit,self.titleEdit)
        bibEntryForm.setTabOrder(self.titleEdit,self.collectionTitleEdit)
        bibEntryForm.setTabOrder(self.collectionTitleEdit,self.journalEdit)
        bibEntryForm.setTabOrder(self.journalEdit,self.volumeEdit)
        bibEntryForm.setTabOrder(self.volumeEdit,self.numberEdit)
        bibEntryForm.setTabOrder(self.numberEdit,self.pagesEdit)
        bibEntryForm.setTabOrder(self.pagesEdit,self.editionEdit)
        bibEntryForm.setTabOrder(self.editionEdit,self.yearEdit)
        bibEntryForm.setTabOrder(self.yearEdit,self.abstractEdit)
        bibEntryForm.setTabOrder(self.abstractEdit,self.submitButton)
        bibEntryForm.setTabOrder(self.submitButton,self.cancelButton)
        bibEntryForm.setTabOrder(self.cancelButton,self.generateKeyButton_2)

    def retranslateUi(self, bibEntryForm):
        bibEntryForm.setWindowTitle(QtGui.QApplication.translate("bibEntryForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2_2.setText(QtGui.QApplication.translate("bibEntryForm", "Citekey:", None, QtGui.QApplication.UnicodeUTF8))
        self.generateKeyButton_2.setText(QtGui.QApplication.translate("bibEntryForm", "Generate Citekey", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("bibEntryForm", "Authors:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("bibEntryForm", "Editors:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("bibEntryForm", "Title:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("bibEntryForm", "Collection Title:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("bibEntryForm", "Year:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("bibEntryForm", "Pages:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("bibEntryForm", "Volume:", None, QtGui.QApplication.UnicodeUTF8))
        self.journalLabel.setText(QtGui.QApplication.translate("bibEntryForm", "Journal:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("bibEntryForm", "Number:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("bibEntryForm", "Edition:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("bibEntryForm", "Abstract", None, QtGui.QApplication.UnicodeUTF8))
        self.submitButton.setText(QtGui.QApplication.translate("bibEntryForm", "Submit", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("bibEntryForm", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
