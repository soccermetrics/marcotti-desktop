# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'penalty_entry.ui'
#
# Created: Fri Jan 28 01:00:49 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_penaltyEntryDlg(object):
    def setupUi(self, penaltyEntryDlg):
        penaltyEntryDlg.setObjectName("penaltyEntryDlg")
        penaltyEntryDlg.resize(560, 450)
        penaltyEntryDlg.setMinimumSize(QtCore.QSize(560, 450))
        penaltyEntryDlg.setMaximumSize(QtCore.QSize(560, 450))
        self.layoutWidget_2 = QtGui.QWidget(penaltyEntryDlg)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 151, 421, 241))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtGui.QLabel(self.layoutWidget_2)
        self.label_4.setMinimumSize(QtCore.QSize(129, 31))
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.penaltyID_display = QtGui.QLineEdit(self.layoutWidget_2)
        self.penaltyID_display.setMaximumSize(QtCore.QSize(120, 27))
        self.penaltyID_display.setStyleSheet("background-color: rgb(194, 190, 186);")
        self.penaltyID_display.setMaxLength(7)
        self.penaltyID_display.setReadOnly(True)
        self.penaltyID_display.setObjectName("penaltyID_display")
        self.gridLayout_2.addWidget(self.penaltyID_display, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.layoutWidget_2)
        self.label_5.setMinimumSize(QtCore.QSize(129, 31))
        self.label_5.setMaximumSize(QtCore.QSize(129, 31))
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.teamSelect = QtGui.QComboBox(self.layoutWidget_2)
        self.teamSelect.setMinimumSize(QtCore.QSize(261, 31))
        self.teamSelect.setMaximumSize(QtCore.QSize(261, 31))
        self.teamSelect.setObjectName("teamSelect")
        self.gridLayout_2.addWidget(self.teamSelect, 1, 1, 1, 2)
        self.label_10 = QtGui.QLabel(self.layoutWidget_2)
        self.label_10.setMinimumSize(QtCore.QSize(129, 31))
        self.label_10.setMaximumSize(QtCore.QSize(129, 31))
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 2, 0, 1, 1)
        self.playerSelect = QtGui.QComboBox(self.layoutWidget_2)
        self.playerSelect.setMinimumSize(QtCore.QSize(231, 31))
        self.playerSelect.setMaximumSize(QtCore.QSize(231, 31))
        self.playerSelect.setObjectName("playerSelect")
        self.gridLayout_2.addWidget(self.playerSelect, 2, 1, 1, 2)
        self.label_7 = QtGui.QLabel(self.layoutWidget_2)
        self.label_7.setMinimumSize(QtCore.QSize(129, 31))
        self.label_7.setMaximumSize(QtCore.QSize(129, 31))
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 3, 0, 1, 1)
        self.foulSelect = QtGui.QComboBox(self.layoutWidget_2)
        self.foulSelect.setMinimumSize(QtCore.QSize(201, 31))
        self.foulSelect.setMaximumSize(QtCore.QSize(201, 31))
        self.foulSelect.setObjectName("foulSelect")
        self.gridLayout_2.addWidget(self.foulSelect, 3, 1, 1, 2)
        self.label_6 = QtGui.QLabel(self.layoutWidget_2)
        self.label_6.setMinimumSize(QtCore.QSize(129, 31))
        self.label_6.setMaximumSize(QtCore.QSize(129, 31))
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 4, 0, 1, 1)
        self.penoutcomeSelect = QtGui.QComboBox(self.layoutWidget_2)
        self.penoutcomeSelect.setMinimumSize(QtCore.QSize(201, 31))
        self.penoutcomeSelect.setMaximumSize(QtCore.QSize(201, 31))
        self.penoutcomeSelect.setObjectName("penoutcomeSelect")
        self.gridLayout_2.addWidget(self.penoutcomeSelect, 4, 1, 1, 2)
        self.label_8 = QtGui.QLabel(self.layoutWidget_2)
        self.label_8.setMinimumSize(QtCore.QSize(129, 31))
        self.label_8.setMaximumSize(QtCore.QSize(129, 31))
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 5, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pentimeEdit = QtGui.QLineEdit(self.layoutWidget_2)
        self.pentimeEdit.setMinimumSize(QtCore.QSize(41, 27))
        self.pentimeEdit.setMaximumSize(QtCore.QSize(41, 27))
        self.pentimeEdit.setMaxLength(2)
        self.pentimeEdit.setObjectName("pentimeEdit")
        self.horizontalLayout.addWidget(self.pentimeEdit)
        self.label_9 = QtGui.QLabel(self.layoutWidget_2)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout.addWidget(self.label_9)
        self.stoppageEdit = QtGui.QLineEdit(self.layoutWidget_2)
        self.stoppageEdit.setMinimumSize(QtCore.QSize(41, 27))
        self.stoppageEdit.setMaximumSize(QtCore.QSize(41, 27))
        self.stoppageEdit.setMaxLength(2)
        self.stoppageEdit.setObjectName("stoppageEdit")
        self.horizontalLayout.addWidget(self.stoppageEdit)
        self.gridLayout_2.addLayout(self.horizontalLayout, 5, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(138, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 5, 2, 1, 1)
        self.layoutWidget_3 = QtGui.QWidget(penaltyEntryDlg)
        self.layoutWidget_3.setGeometry(QtCore.QRect(40, 400, 351, 41))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.firstEntry = QtGui.QPushButton(self.layoutWidget_3)
        self.firstEntry.setMinimumSize(QtCore.QSize(77, 27))
        self.firstEntry.setMaximumSize(QtCore.QSize(77, 27))
        self.firstEntry.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/first.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.firstEntry.setIcon(icon)
        self.firstEntry.setObjectName("firstEntry")
        self.horizontalLayout_2.addWidget(self.firstEntry)
        self.prevEntry = QtGui.QPushButton(self.layoutWidget_3)
        self.prevEntry.setMinimumSize(QtCore.QSize(77, 27))
        self.prevEntry.setMaximumSize(QtCore.QSize(77, 27))
        self.prevEntry.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/prev.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prevEntry.setIcon(icon1)
        self.prevEntry.setObjectName("prevEntry")
        self.horizontalLayout_2.addWidget(self.prevEntry)
        self.nextEntry = QtGui.QPushButton(self.layoutWidget_3)
        self.nextEntry.setMinimumSize(QtCore.QSize(77, 27))
        self.nextEntry.setMaximumSize(QtCore.QSize(77, 27))
        self.nextEntry.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextEntry.setIcon(icon2)
        self.nextEntry.setObjectName("nextEntry")
        self.horizontalLayout_2.addWidget(self.nextEntry)
        self.lastEntry = QtGui.QPushButton(self.layoutWidget_3)
        self.lastEntry.setMinimumSize(QtCore.QSize(77, 27))
        self.lastEntry.setMaximumSize(QtCore.QSize(77, 27))
        self.lastEntry.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/last.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lastEntry.setIcon(icon3)
        self.lastEntry.setObjectName("lastEntry")
        self.horizontalLayout_2.addWidget(self.lastEntry)
        self.layoutWidget_4 = QtGui.QWidget(penaltyEntryDlg)
        self.layoutWidget_4.setGeometry(QtCore.QRect(10, 6, 421, 121))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget_4)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.layoutWidget_4)
        self.label.setMinimumSize(QtCore.QSize(129, 31))
        self.label.setMaximumSize(QtCore.QSize(129, 31))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.compSelect = QtGui.QComboBox(self.layoutWidget_4)
        self.compSelect.setMinimumSize(QtCore.QSize(271, 31))
        self.compSelect.setMaximumSize(QtCore.QSize(271, 31))
        self.compSelect.setObjectName("compSelect")
        self.gridLayout.addWidget(self.compSelect, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget_4)
        self.label_2.setMinimumSize(QtCore.QSize(129, 31))
        self.label_2.setMaximumSize(QtCore.QSize(129, 31))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.roundSelect = QtGui.QComboBox(self.layoutWidget_4)
        self.roundSelect.setMinimumSize(QtCore.QSize(171, 31))
        self.roundSelect.setMaximumSize(QtCore.QSize(171, 31))
        self.roundSelect.setObjectName("roundSelect")
        self.gridLayout.addWidget(self.roundSelect, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget_4)
        self.label_3.setMinimumSize(QtCore.QSize(129, 31))
        self.label_3.setMaximumSize(QtCore.QSize(129, 31))
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.matchSelect = QtGui.QComboBox(self.layoutWidget_4)
        self.matchSelect.setMinimumSize(QtCore.QSize(271, 31))
        self.matchSelect.setMaximumSize(QtCore.QSize(271, 31))
        self.matchSelect.setObjectName("matchSelect")
        self.gridLayout.addWidget(self.matchSelect, 2, 1, 1, 1)
        self.line = QtGui.QFrame(penaltyEntryDlg)
        self.line.setGeometry(QtCore.QRect(10, 130, 431, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtGui.QFrame(penaltyEntryDlg)
        self.line_2.setGeometry(QtCore.QRect(430, 0, 20, 391))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.layoutWidget = QtGui.QWidget(penaltyEntryDlg)
        self.layoutWidget.setGeometry(QtCore.QRect(450, 150, 101, 241))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addEntry = QtGui.QPushButton(self.layoutWidget)
        self.addEntry.setMinimumSize(QtCore.QSize(85, 33))
        self.addEntry.setMaximumSize(QtCore.QSize(85, 33))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addEntry.setIcon(icon4)
        self.addEntry.setObjectName("addEntry")
        self.verticalLayout.addWidget(self.addEntry)
        self.deleteEntry = QtGui.QPushButton(self.layoutWidget)
        self.deleteEntry.setMinimumSize(QtCore.QSize(85, 33))
        self.deleteEntry.setMaximumSize(QtCore.QSize(85, 33))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteEntry.setIcon(icon5)
        self.deleteEntry.setObjectName("deleteEntry")
        self.verticalLayout.addWidget(self.deleteEntry)
        spacerItem1 = QtGui.QSpacerItem(20, 168, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.closeButton = QtGui.QPushButton(self.layoutWidget)
        self.closeButton.setMinimumSize(QtCore.QSize(85, 33))
        self.closeButton.setMaximumSize(QtCore.QSize(85, 33))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/quit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon6)
        self.closeButton.setObjectName("closeButton")
        self.verticalLayout.addWidget(self.closeButton)

        self.retranslateUi(penaltyEntryDlg)
        QtCore.QMetaObject.connectSlotsByName(penaltyEntryDlg)

    def retranslateUi(self, penaltyEntryDlg):
        penaltyEntryDlg.setWindowTitle(QtGui.QApplication.translate("penaltyEntryDlg", "Penalty Kick Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("penaltyEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Penalty ID</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("penaltyEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Team</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.teamSelect.setToolTip(QtGui.QApplication.translate("penaltyEntryDlg", "Team of penalty kick taker", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("penaltyEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Player</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.playerSelect.setToolTip(QtGui.QApplication.translate("penaltyEntryDlg", "Penalty kick taker", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("penaltyEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Foul</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.foulSelect.setToolTip(QtGui.QApplication.translate("penaltyEntryDlg", "Foul that resulted in penalty", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("penaltyEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Penalty Outcome</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.penoutcomeSelect.setToolTip(QtGui.QApplication.translate("penaltyEntryDlg", "Penalty kick outcome", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("penaltyEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Time of Penalty</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pentimeEdit.setToolTip(QtGui.QApplication.translate("penaltyEntryDlg", "Match time", None, QtGui.QApplication.UnicodeUTF8))
        self.pentimeEdit.setInputMask(QtGui.QApplication.translate("penaltyEntryDlg", "00; ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("penaltyEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">+</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.stoppageEdit.setToolTip(QtGui.QApplication.translate("penaltyEntryDlg", "Stoppage time", None, QtGui.QApplication.UnicodeUTF8))
        self.stoppageEdit.setInputMask(QtGui.QApplication.translate("penaltyEntryDlg", "00; ", None, QtGui.QApplication.UnicodeUTF8))
        self.firstEntry.setToolTip(QtGui.QApplication.translate("penaltyEntryDlg", "First Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.prevEntry.setToolTip(QtGui.QApplication.translate("penaltyEntryDlg", "Previous Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.nextEntry.setToolTip(QtGui.QApplication.translate("penaltyEntryDlg", "Next Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.lastEntry.setToolTip(QtGui.QApplication.translate("penaltyEntryDlg", "Last Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("penaltyEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Competition</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("penaltyEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Round</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("penaltyEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Match</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.addEntry.setToolTip(QtGui.QApplication.translate("penaltyEntryDlg", "Add Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.addEntry.setText(QtGui.QApplication.translate("penaltyEntryDlg", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteEntry.setToolTip(QtGui.QApplication.translate("penaltyEntryDlg", "Delete Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteEntry.setText(QtGui.QApplication.translate("penaltyEntryDlg", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setToolTip(QtGui.QApplication.translate("penaltyEntryDlg", "Close Window", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("penaltyEntryDlg", "&Close", None, QtGui.QApplication.UnicodeUTF8))

import fmrd_resources_rc
