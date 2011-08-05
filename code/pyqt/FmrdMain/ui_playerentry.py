# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/player_entry.ui'
#
# Created: Fri Aug  5 15:10:57 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PlayerEntryDlg(object):
    def setupUi(self, PlayerEntryDlg):
        PlayerEntryDlg.setObjectName("PlayerEntryDlg")
        PlayerEntryDlg.resize(800, 250)
        PlayerEntryDlg.setMinimumSize(QtCore.QSize(800, 250))
        PlayerEntryDlg.setMaximumSize(QtCore.QSize(800, 250))
        self.frame_2 = QtGui.QFrame(PlayerEntryDlg)
        self.frame_2.setGeometry(QtCore.QRect(10, 180, 331, 51))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.firstEntry = QtGui.QPushButton(self.frame_2)
        self.firstEntry.setGeometry(QtCore.QRect(10, 10, 71, 33))
        self.firstEntry.setMinimumSize(QtCore.QSize(71, 33))
        self.firstEntry.setMaximumSize(QtCore.QSize(71, 33))
        self.firstEntry.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/first.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.firstEntry.setIcon(icon)
        self.firstEntry.setObjectName("firstEntry")
        self.prevEntry = QtGui.QPushButton(self.frame_2)
        self.prevEntry.setGeometry(QtCore.QRect(90, 10, 71, 33))
        self.prevEntry.setMinimumSize(QtCore.QSize(71, 33))
        self.prevEntry.setMaximumSize(QtCore.QSize(71, 33))
        self.prevEntry.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/prev.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prevEntry.setIcon(icon1)
        self.prevEntry.setObjectName("prevEntry")
        self.nextEntry = QtGui.QPushButton(self.frame_2)
        self.nextEntry.setGeometry(QtCore.QRect(170, 10, 71, 33))
        self.nextEntry.setMinimumSize(QtCore.QSize(71, 33))
        self.nextEntry.setMaximumSize(QtCore.QSize(71, 33))
        self.nextEntry.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextEntry.setIcon(icon2)
        self.nextEntry.setObjectName("nextEntry")
        self.lastEntry = QtGui.QPushButton(self.frame_2)
        self.lastEntry.setGeometry(QtCore.QRect(250, 10, 71, 33))
        self.lastEntry.setMinimumSize(QtCore.QSize(71, 33))
        self.lastEntry.setMaximumSize(QtCore.QSize(71, 33))
        self.lastEntry.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/last.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lastEntry.setIcon(icon3)
        self.lastEntry.setObjectName("lastEntry")
        self.frame = QtGui.QFrame(PlayerEntryDlg)
        self.frame.setGeometry(QtCore.QRect(440, 180, 281, 51))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.addEntry = QtGui.QPushButton(self.frame)
        self.addEntry.setGeometry(QtCore.QRect(10, 10, 80, 33))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addEntry.setIcon(icon4)
        self.addEntry.setObjectName("addEntry")
        self.deleteEntry = QtGui.QPushButton(self.frame)
        self.deleteEntry.setGeometry(QtCore.QRect(100, 10, 82, 33))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteEntry.setIcon(icon5)
        self.deleteEntry.setObjectName("deleteEntry")
        self.closeButton = QtGui.QPushButton(self.frame)
        self.closeButton.setGeometry(QtCore.QRect(190, 10, 80, 33))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("images/quit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon6)
        self.closeButton.setObjectName("closeButton")
        self.line = QtGui.QFrame(PlayerEntryDlg)
        self.line.setGeometry(QtCore.QRect(350, 10, 20, 161))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.layoutWidget = QtGui.QWidget(PlayerEntryDlg)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 341, 161))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.plyrID_display = QtGui.QLineEdit(self.layoutWidget)
        self.plyrID_display.setMaximumSize(QtCore.QSize(81, 27))
        self.plyrID_display.setStyleSheet("background-color: rgb(194, 190, 186);")
        self.plyrID_display.setReadOnly(True)
        self.plyrID_display.setObjectName("plyrID_display")
        self.gridLayout.addWidget(self.plyrID_display, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.plyrFirstNameEdit = QtGui.QLineEdit(self.layoutWidget)
        self.plyrFirstNameEdit.setMinimumSize(QtCore.QSize(219, 27))
        self.plyrFirstNameEdit.setMaximumSize(QtCore.QSize(219, 27))
        self.plyrFirstNameEdit.setObjectName("plyrFirstNameEdit")
        self.gridLayout.addWidget(self.plyrFirstNameEdit, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.plyrLastNameEdit = QtGui.QLineEdit(self.layoutWidget)
        self.plyrLastNameEdit.setMinimumSize(QtCore.QSize(219, 27))
        self.plyrLastNameEdit.setMaximumSize(QtCore.QSize(219, 27))
        self.plyrLastNameEdit.setObjectName("plyrLastNameEdit")
        self.gridLayout.addWidget(self.plyrLastNameEdit, 2, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.plyrNicknameEdit = QtGui.QLineEdit(self.layoutWidget)
        self.plyrNicknameEdit.setMinimumSize(QtCore.QSize(219, 27))
        self.plyrNicknameEdit.setMaximumSize(QtCore.QSize(219, 27))
        self.plyrNicknameEdit.setObjectName("plyrNicknameEdit")
        self.gridLayout.addWidget(self.plyrNicknameEdit, 3, 1, 1, 1)
        self.layoutWidget1 = QtGui.QWidget(PlayerEntryDlg)
        self.layoutWidget1.setGeometry(QtCore.QRect(370, 10, 411, 161))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_7 = QtGui.QLabel(self.layoutWidget1)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.plyrDOBEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.plyrDOBEdit.setMinimumSize(QtCore.QSize(91, 27))
        self.plyrDOBEdit.setMaximumSize(QtCore.QSize(91, 27))
        self.plyrDOBEdit.setObjectName("plyrDOBEdit")
        self.gridLayout_2.addWidget(self.plyrDOBEdit, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.plyrConfedSelect = QtGui.QComboBox(self.layoutWidget1)
        self.plyrConfedSelect.setMinimumSize(QtCore.QSize(241, 27))
        self.plyrConfedSelect.setMaximumSize(QtCore.QSize(241, 27))
        self.plyrConfedSelect.setObjectName("plyrConfedSelect")
        self.gridLayout_2.addWidget(self.plyrConfedSelect, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.plyrCountrySelect = QtGui.QComboBox(self.layoutWidget1)
        self.plyrCountrySelect.setMinimumSize(QtCore.QSize(241, 27))
        self.plyrCountrySelect.setMaximumSize(QtCore.QSize(241, 27))
        self.plyrCountrySelect.setObjectName("plyrCountrySelect")
        self.gridLayout_2.addWidget(self.plyrCountrySelect, 2, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.layoutWidget1)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 3, 0, 1, 1)
        self.plyrPositionSelect = QtGui.QComboBox(self.layoutWidget1)
        self.plyrPositionSelect.setMinimumSize(QtCore.QSize(241, 27))
        self.plyrPositionSelect.setMaximumSize(QtCore.QSize(241, 27))
        self.plyrPositionSelect.setObjectName("plyrPositionSelect")
        self.gridLayout_2.addWidget(self.plyrPositionSelect, 3, 1, 1, 1)
        self.label.setBuddy(self.plyrID_display)
        self.label_4.setBuddy(self.plyrFirstNameEdit)
        self.label_5.setBuddy(self.plyrLastNameEdit)
        self.label_6.setBuddy(self.plyrNicknameEdit)
        self.label_7.setBuddy(self.plyrDOBEdit)
        self.label_2.setBuddy(self.plyrConfedSelect)
        self.label_3.setBuddy(self.plyrCountrySelect)
        self.label_8.setBuddy(self.plyrPositionSelect)

        self.retranslateUi(PlayerEntryDlg)
        QtCore.QMetaObject.connectSlotsByName(PlayerEntryDlg)

    def retranslateUi(self, PlayerEntryDlg):
        PlayerEntryDlg.setWindowTitle(QtGui.QApplication.translate("PlayerEntryDlg", "Player Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.firstEntry.setToolTip(QtGui.QApplication.translate("PlayerEntryDlg", "First Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.prevEntry.setToolTip(QtGui.QApplication.translate("PlayerEntryDlg", "Previous Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.nextEntry.setToolTip(QtGui.QApplication.translate("PlayerEntryDlg", "Next Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.lastEntry.setToolTip(QtGui.QApplication.translate("PlayerEntryDlg", "Last Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.addEntry.setText(QtGui.QApplication.translate("PlayerEntryDlg", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteEntry.setText(QtGui.QApplication.translate("PlayerEntryDlg", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("PlayerEntryDlg", "&Close", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PlayerEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">&amp;ID</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("PlayerEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">&amp;First Name</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.plyrFirstNameEdit.setToolTip(QtGui.QApplication.translate("PlayerEntryDlg", "Player first name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("PlayerEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">&amp;Last Name</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.plyrLastNameEdit.setToolTip(QtGui.QApplication.translate("PlayerEntryDlg", "Player surname", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("PlayerEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Nic&amp;kname</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.plyrNicknameEdit.setToolTip(QtGui.QApplication.translate("PlayerEntryDlg", "Player nickname, if applicable", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("PlayerEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Date of &amp;Birth</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.plyrDOBEdit.setToolTip(QtGui.QApplication.translate("PlayerEntryDlg", "Player date of birth (YYYY-MM-DD)", None, QtGui.QApplication.UnicodeUTF8))
        self.plyrDOBEdit.setInputMask(QtGui.QApplication.translate("PlayerEntryDlg", "9999-99-99; ", None, QtGui.QApplication.UnicodeUTF8))
        self.plyrDOBEdit.setText(QtGui.QApplication.translate("PlayerEntryDlg", "1901-01-01", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PlayerEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">&amp;Region</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.plyrConfedSelect.setToolTip(QtGui.QApplication.translate("PlayerEntryDlg", "Football confederation of player\'s country", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PlayerEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Cou&amp;ntry</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.plyrCountrySelect.setToolTip(QtGui.QApplication.translate("PlayerEntryDlg", "Player\'s country", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("PlayerEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Default &amp;Position</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.plyrPositionSelect.setToolTip(QtGui.QApplication.translate("PlayerEntryDlg", "Player\'s default position", None, QtGui.QApplication.UnicodeUTF8))

import fmrd_resources_rc
