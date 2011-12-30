# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/fmrd_drivers.ui'
#
# Created: Thu Dec 29 23:31:04 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DBDriverDlg(object):
    def setupUi(self, DBDriverDlg):
        DBDriverDlg.setObjectName("DBDriverDlg")
        DBDriverDlg.resize(240, 180)
        DBDriverDlg.setMinimumSize(QtCore.QSize(240, 180))
        DBDriverDlg.setMaximumSize(QtCore.QSize(240, 180))
        self.buttonBox = QtGui.QDialogButtonBox(DBDriverDlg)
        self.buttonBox.setGeometry(QtCore.QRect(30, 120, 180, 45))
        self.buttonBox.setMinimumSize(QtCore.QSize(180, 45))
        self.buttonBox.setMaximumSize(QtCore.QSize(180, 45))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtGui.QLabel(DBDriverDlg)
        self.label.setGeometry(QtCore.QRect(10, 10, 221, 21))
        self.label.setObjectName("label")
        self.widget = QtGui.QWidget(DBDriverDlg)
        self.widget.setGeometry(QtCore.QRect(60, 40, 122, 68))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sqliteButton = QtGui.QRadioButton(self.widget)
        self.sqliteButton.setMinimumSize(QtCore.QSize(120, 30))
        self.sqliteButton.setMaximumSize(QtCore.QSize(120, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.sqliteButton.setFont(font)
        self.sqliteButton.setToolTip("")
        self.sqliteButton.setChecked(True)
        self.sqliteButton.setObjectName("sqliteButton")
        self.verticalLayout.addWidget(self.sqliteButton)
        self.postgresButton = QtGui.QRadioButton(self.widget)
        self.postgresButton.setMinimumSize(QtCore.QSize(120, 30))
        self.postgresButton.setMaximumSize(QtCore.QSize(120, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.postgresButton.setFont(font)
        self.postgresButton.setToolTip("")
        self.postgresButton.setObjectName("postgresButton")
        self.verticalLayout.addWidget(self.postgresButton)

        self.retranslateUi(DBDriverDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DBDriverDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DBDriverDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(DBDriverDlg)

    def retranslateUi(self, DBDriverDlg):
        DBDriverDlg.setWindowTitle(QtGui.QApplication.translate("DBDriverDlg", "FMRD", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DBDriverDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Please select a database driver</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.sqliteButton.setText(QtGui.QApplication.translate("DBDriverDlg", "SQLite", None, QtGui.QApplication.UnicodeUTF8))
        self.postgresButton.setText(QtGui.QApplication.translate("DBDriverDlg", "PostgreSQL", None, QtGui.QApplication.UnicodeUTF8))

