# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/referee_entry.ui'
#
# Created: Sat Aug  6 01:54:24 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RefereeEntryDlg(object):
    def setupUi(self, RefereeEntryDlg):
        RefereeEntryDlg.setObjectName("RefereeEntryDlg")
        RefereeEntryDlg.resize(800, 250)
        RefereeEntryDlg.setMinimumSize(QtCore.QSize(800, 250))
        RefereeEntryDlg.setMaximumSize(QtCore.QSize(800, 250))
        self.frame_2 = QtGui.QFrame(RefereeEntryDlg)
        self.frame_2.setGeometry(QtCore.QRect(30, 170, 331, 51))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.firstEntry = QtGui.QPushButton(self.frame_2)
        self.firstEntry.setGeometry(QtCore.QRect(10, 10, 71, 33))
        self.firstEntry.setMinimumSize(QtCore.QSize(71, 33))
        self.firstEntry.setMaximumSize(QtCore.QSize(71, 33))
        self.firstEntry.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/first.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.firstEntry.setIcon(icon)
        self.firstEntry.setObjectName("firstEntry")
        self.prevEntry = QtGui.QPushButton(self.frame_2)
        self.prevEntry.setGeometry(QtCore.QRect(90, 10, 71, 33))
        self.prevEntry.setMinimumSize(QtCore.QSize(71, 33))
        self.prevEntry.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/prev.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prevEntry.setIcon(icon1)
        self.prevEntry.setObjectName("prevEntry")
        self.nextEntry = QtGui.QPushButton(self.frame_2)
        self.nextEntry.setGeometry(QtCore.QRect(170, 10, 71, 33))
        self.nextEntry.setMinimumSize(QtCore.QSize(71, 33))
        self.nextEntry.setMaximumSize(QtCore.QSize(71, 33))
        self.nextEntry.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextEntry.setIcon(icon2)
        self.nextEntry.setObjectName("nextEntry")
        self.lastEntry = QtGui.QPushButton(self.frame_2)
        self.lastEntry.setGeometry(QtCore.QRect(250, 10, 71, 33))
        self.lastEntry.setMinimumSize(QtCore.QSize(71, 33))
        self.lastEntry.setMaximumSize(QtCore.QSize(71, 33))
        self.lastEntry.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/last.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lastEntry.setIcon(icon3)
        self.lastEntry.setObjectName("lastEntry")
        self.frame = QtGui.QFrame(RefereeEntryDlg)
        self.frame.setGeometry(QtCore.QRect(450, 170, 281, 51))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.addEntry = QtGui.QPushButton(self.frame)
        self.addEntry.setGeometry(QtCore.QRect(10, 10, 80, 33))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addEntry.setIcon(icon4)
        self.addEntry.setObjectName("addEntry")
        self.deleteEntry = QtGui.QPushButton(self.frame)
        self.deleteEntry.setGeometry(QtCore.QRect(100, 10, 82, 33))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteEntry.setIcon(icon5)
        self.deleteEntry.setObjectName("deleteEntry")
        self.closeButton = QtGui.QPushButton(self.frame)
        self.closeButton.setGeometry(QtCore.QRect(190, 10, 80, 33))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/quit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon6)
        self.closeButton.setObjectName("closeButton")
        self.line = QtGui.QFrame(RefereeEntryDlg)
        self.line.setGeometry(QtCore.QRect(380, 10, 20, 151))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.layoutWidget = QtGui.QWidget(RefereeEntryDlg)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 361, 151))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.refID_display = QtGui.QLineEdit(self.layoutWidget)
        self.refID_display.setMaximumSize(QtCore.QSize(81, 27))
        self.refID_display.setStyleSheet("background-color: rgb(194, 190, 186);")
        self.refID_display.setReadOnly(True)
        self.refID_display.setObjectName("refID_display")
        self.gridLayout.addWidget(self.refID_display, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.refFirstNameEdit = QtGui.QLineEdit(self.layoutWidget)
        self.refFirstNameEdit.setMinimumSize(QtCore.QSize(219, 27))
        self.refFirstNameEdit.setMaximumSize(QtCore.QSize(219, 27))
        self.refFirstNameEdit.setObjectName("refFirstNameEdit")
        self.gridLayout.addWidget(self.refFirstNameEdit, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.refLastNameEdit = QtGui.QLineEdit(self.layoutWidget)
        self.refLastNameEdit.setMinimumSize(QtCore.QSize(219, 27))
        self.refLastNameEdit.setMaximumSize(QtCore.QSize(219, 27))
        self.refLastNameEdit.setObjectName("refLastNameEdit")
        self.gridLayout.addWidget(self.refLastNameEdit, 2, 1, 1, 1)
        self.layoutWidget1 = QtGui.QWidget(RefereeEntryDlg)
        self.layoutWidget1.setGeometry(QtCore.QRect(410, 10, 371, 151))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_7 = QtGui.QLabel(self.layoutWidget1)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.refDOBEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.refDOBEdit.setMinimumSize(QtCore.QSize(91, 27))
        self.refDOBEdit.setMaximumSize(QtCore.QSize(91, 27))
        self.refDOBEdit.setObjectName("refDOBEdit")
        self.gridLayout_2.addWidget(self.refDOBEdit, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.refConfedSelect = QtGui.QComboBox(self.layoutWidget1)
        self.refConfedSelect.setMinimumSize(QtCore.QSize(241, 31))
        self.refConfedSelect.setMaximumSize(QtCore.QSize(241, 31))
        self.refConfedSelect.setObjectName("refConfedSelect")
        self.gridLayout_2.addWidget(self.refConfedSelect, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.refCountrySelect = QtGui.QComboBox(self.layoutWidget1)
        self.refCountrySelect.setMinimumSize(QtCore.QSize(241, 31))
        self.refCountrySelect.setMaximumSize(QtCore.QSize(241, 31))
        self.refCountrySelect.setObjectName("refCountrySelect")
        self.gridLayout_2.addWidget(self.refCountrySelect, 2, 1, 1, 1)
        self.label.setBuddy(self.refID_display)
        self.label_4.setBuddy(self.refFirstNameEdit)
        self.label_5.setBuddy(self.refLastNameEdit)
        self.label_7.setBuddy(self.refDOBEdit)
        self.label_2.setBuddy(self.refConfedSelect)
        self.label_3.setBuddy(self.refCountrySelect)

        self.retranslateUi(RefereeEntryDlg)
        QtCore.QMetaObject.connectSlotsByName(RefereeEntryDlg)

    def retranslateUi(self, RefereeEntryDlg):
        RefereeEntryDlg.setWindowTitle(QtGui.QApplication.translate("RefereeEntryDlg", "Referee Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.firstEntry.setToolTip(QtGui.QApplication.translate("RefereeEntryDlg", "First Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.prevEntry.setToolTip(QtGui.QApplication.translate("RefereeEntryDlg", "Previous Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.nextEntry.setToolTip(QtGui.QApplication.translate("RefereeEntryDlg", "Next Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.lastEntry.setToolTip(QtGui.QApplication.translate("RefereeEntryDlg", "Last Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.addEntry.setText(QtGui.QApplication.translate("RefereeEntryDlg", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteEntry.setText(QtGui.QApplication.translate("RefereeEntryDlg", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("RefereeEntryDlg", "&Close", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("RefereeEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">&amp;ID</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("RefereeEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">&amp;First Name</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.refFirstNameEdit.setToolTip(QtGui.QApplication.translate("RefereeEntryDlg", "Referee first name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("RefereeEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">&amp;Last Name</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.refLastNameEdit.setToolTip(QtGui.QApplication.translate("RefereeEntryDlg", "Referee surname", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("RefereeEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Date of &amp;Birth</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.refDOBEdit.setToolTip(QtGui.QApplication.translate("RefereeEntryDlg", "Referee date of birth (YYYY-MM-DD)", None, QtGui.QApplication.UnicodeUTF8))
        self.refDOBEdit.setInputMask(QtGui.QApplication.translate("RefereeEntryDlg", "9999-99-99; ", None, QtGui.QApplication.UnicodeUTF8))
        self.refDOBEdit.setText(QtGui.QApplication.translate("RefereeEntryDlg", "1901-01-01", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("RefereeEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">&amp;Region</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.refConfedSelect.setToolTip(QtGui.QApplication.translate("RefereeEntryDlg", "Football confederation of referee\'s country", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("RefereeEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Cou&amp;ntry</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.refCountrySelect.setToolTip(QtGui.QApplication.translate("RefereeEntryDlg", "Referee\'s country", None, QtGui.QApplication.UnicodeUTF8))

import fmrd_resources_rc
