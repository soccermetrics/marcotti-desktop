# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/fmrd_login.ui'
#
# Created: Fri Aug  5 15:10:52 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DBLoginDlg(object):
    def setupUi(self, DBLoginDlg):
        DBLoginDlg.setObjectName("DBLoginDlg")
        DBLoginDlg.resize(240, 180)
        DBLoginDlg.setMinimumSize(QtCore.QSize(240, 180))
        DBLoginDlg.setMaximumSize(QtCore.QSize(240, 180))
        self.buttonBox = QtGui.QDialogButtonBox(DBLoginDlg)
        self.buttonBox.setGeometry(QtCore.QRect(0, 140, 221, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtGui.QWidget(DBLoginDlg)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 30, 241, 101))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtGui.QFormLayout(self.layoutWidget)
        self.formLayout.setObjectName("formLayout")
        self.dbnameLabel = QtGui.QLabel(self.layoutWidget)
        self.dbnameLabel.setMinimumSize(QtCore.QSize(81, 21))
        self.dbnameLabel.setMaximumSize(QtCore.QSize(81, 21))
        self.dbnameLabel.setObjectName("dbnameLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.dbnameLabel)
        self.dbNameEdit = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dbNameEdit.sizePolicy().hasHeightForWidth())
        self.dbNameEdit.setSizePolicy(sizePolicy)
        self.dbNameEdit.setMinimumSize(QtCore.QSize(131, 27))
        self.dbNameEdit.setMaximumSize(QtCore.QSize(131, 27))
        self.dbNameEdit.setObjectName("dbNameEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.dbNameEdit)
        self.loginLabel = QtGui.QLabel(self.layoutWidget)
        self.loginLabel.setMinimumSize(QtCore.QSize(81, 21))
        self.loginLabel.setMaximumSize(QtCore.QSize(81, 21))
        self.loginLabel.setObjectName("loginLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.loginLabel)
        self.loginEdit = QtGui.QLineEdit(self.layoutWidget)
        self.loginEdit.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginEdit.sizePolicy().hasHeightForWidth())
        self.loginEdit.setSizePolicy(sizePolicy)
        self.loginEdit.setMinimumSize(QtCore.QSize(131, 27))
        self.loginEdit.setMaximumSize(QtCore.QSize(131, 27))
        self.loginEdit.setObjectName("loginEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.loginEdit)
        self.passwordLabel = QtGui.QLabel(self.layoutWidget)
        self.passwordLabel.setMinimumSize(QtCore.QSize(81, 21))
        self.passwordLabel.setMaximumSize(QtCore.QSize(81, 21))
        self.passwordLabel.setObjectName("passwordLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.passwordLabel)
        self.passwordEdit = QtGui.QLineEdit(self.layoutWidget)
        self.passwordEdit.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.passwordEdit.sizePolicy().hasHeightForWidth())
        self.passwordEdit.setSizePolicy(sizePolicy)
        self.passwordEdit.setMinimumSize(QtCore.QSize(131, 27))
        self.passwordEdit.setMaximumSize(QtCore.QSize(131, 27))
        self.passwordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordEdit.setObjectName("passwordEdit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.passwordEdit)
        self.userButton = QtGui.QRadioButton(DBLoginDlg)
        self.userButton.setGeometry(QtCore.QRect(33, 1, 60, 30))
        self.userButton.setMinimumSize(QtCore.QSize(60, 30))
        self.userButton.setMaximumSize(QtCore.QSize(60, 30))
        self.userButton.setChecked(True)
        self.userButton.setObjectName("userButton")
        self.QtGui.QApplication.translate("DBLoginDlg", "switchboardGroup", None, QtGui.QApplication.UnicodeUTF8) = QtGui.QButtonGroup(DBLoginDlg)
        self.QtGui.QApplication.translate("DBLoginDlg", "switchboardGroup", None, QtGui.QApplication.UnicodeUTF8).setObjectName("QtGui.QApplication.translate(\"DBLoginDlg\", \"switchboardGroup\", None, QtGui.QApplication.UnicodeUTF8)")
        self.QtGui.QApplication.translate("DBLoginDlg", "switchboardGroup", None, QtGui.QApplication.UnicodeUTF8).addButton(self.userButton)
        self.adminButton = QtGui.QRadioButton(DBLoginDlg)
        self.adminButton.setGeometry(QtCore.QRect(131, 1, 75, 30))
        self.adminButton.setMinimumSize(QtCore.QSize(75, 30))
        self.adminButton.setMaximumSize(QtCore.QSize(75, 30))
        self.adminButton.setObjectName("adminButton")
        self.QtGui.QApplication.translate("DBLoginDlg", "switchboardGroup", None, QtGui.QApplication.UnicodeUTF8) = QtGui.QButtonGroup(DBLoginDlg)
        self.QtGui.QApplication.translate("DBLoginDlg", "switchboardGroup", None, QtGui.QApplication.UnicodeUTF8).setObjectName("QtGui.QApplication.translate(\"DBLoginDlg\", \"switchboardGroup\", None, QtGui.QApplication.UnicodeUTF8)")
        self.QtGui.QApplication.translate("DBLoginDlg", "switchboardGroup", None, QtGui.QApplication.UnicodeUTF8).addButton(self.adminButton)

        self.retranslateUi(DBLoginDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DBLoginDlg.authenticate)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DBLoginDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(DBLoginDlg)

    def retranslateUi(self, DBLoginDlg):
        DBLoginDlg.setWindowTitle(QtGui.QApplication.translate("DBLoginDlg", "FMRD Login", None, QtGui.QApplication.UnicodeUTF8))
        self.dbnameLabel.setText(QtGui.QApplication.translate("DBLoginDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">DB Name</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.dbNameEdit.setToolTip(QtGui.QApplication.translate("DBLoginDlg", "Database name", None, QtGui.QApplication.UnicodeUTF8))
        self.loginLabel.setText(QtGui.QApplication.translate("DBLoginDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Login</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.loginEdit.setToolTip(QtGui.QApplication.translate("DBLoginDlg", "Database username", None, QtGui.QApplication.UnicodeUTF8))
        self.passwordLabel.setText(QtGui.QApplication.translate("DBLoginDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Password</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.passwordEdit.setToolTip(QtGui.QApplication.translate("DBLoginDlg", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.userButton.setToolTip(QtGui.QApplication.translate("DBLoginDlg", "User switchboard", None, QtGui.QApplication.UnicodeUTF8))
        self.userButton.setText(QtGui.QApplication.translate("DBLoginDlg", "User", None, QtGui.QApplication.UnicodeUTF8))
        self.adminButton.setToolTip(QtGui.QApplication.translate("DBLoginDlg", "Administrator switchboard", None, QtGui.QApplication.UnicodeUTF8))
        self.adminButton.setText(QtGui.QApplication.translate("DBLoginDlg", "Admin", None, QtGui.QApplication.UnicodeUTF8))

