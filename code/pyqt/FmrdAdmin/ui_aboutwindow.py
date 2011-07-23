# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_window.ui'
#
# Created: Sun Jan 23 22:16:35 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AboutDlg(object):
    def setupUi(self, AboutDlg):
        AboutDlg.setObjectName("AboutDlg")
        AboutDlg.resize(385, 155)
        AboutDlg.setMinimumSize(QtCore.QSize(385, 155))
        AboutDlg.setMaximumSize(QtCore.QSize(385, 155))
        self.verticalLayout = QtGui.QVBoxLayout(AboutDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(AboutDlg)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(128, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(AboutDlg)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/quit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem1 = QtGui.QSpacerItem(128, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(AboutDlg)
        QtCore.QMetaObject.connectSlotsByName(AboutDlg)

    def retranslateUi(self, AboutDlg):
        AboutDlg.setWindowTitle(QtGui.QApplication.translate("AboutDlg", "About FMRD", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AboutDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Desktop Data Entry Tool</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">for</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Football Match Result Database</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">v1.0.0</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Soccermetrics Research &amp; Consulting, LLC</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("AboutDlg", "Close", None, QtGui.QApplication.UnicodeUTF8))

import fmrd_resources_rc
