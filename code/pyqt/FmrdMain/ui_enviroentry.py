# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/enviro_entry.ui'
#
# Created: Sat Aug  6 01:32:09 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_EnviroEntryDlg(object):
    def setupUi(self, EnviroEntryDlg):
        EnviroEntryDlg.setObjectName("EnviroEntryDlg")
        EnviroEntryDlg.resize(350, 380)
        EnviroEntryDlg.setMinimumSize(QtCore.QSize(350, 380))
        EnviroEntryDlg.setMaximumSize(QtCore.QSize(350, 380))
        self.weatherBox = QtGui.QGroupBox(EnviroEntryDlg)
        self.weatherBox.setGeometry(QtCore.QRect(9, 187, 319, 141))
        self.weatherBox.setObjectName("weatherBox")
        self.gridLayout = QtGui.QGridLayout(self.weatherBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtGui.QLabel(self.weatherBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.envKOWxSelect = QtGui.QComboBox(self.weatherBox)
        self.envKOWxSelect.setMinimumSize(QtCore.QSize(221, 31))
        self.envKOWxSelect.setMaximumSize(QtCore.QSize(221, 31))
        self.envKOWxSelect.setObjectName("envKOWxSelect")
        self.gridLayout.addWidget(self.envKOWxSelect, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.weatherBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.envHTWxSelect = QtGui.QComboBox(self.weatherBox)
        self.envHTWxSelect.setMinimumSize(QtCore.QSize(221, 31))
        self.envHTWxSelect.setMaximumSize(QtCore.QSize(221, 31))
        self.envHTWxSelect.setObjectName("envHTWxSelect")
        self.gridLayout.addWidget(self.envHTWxSelect, 1, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.weatherBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.envFTWxSelect = QtGui.QComboBox(self.weatherBox)
        self.envFTWxSelect.setMinimumSize(QtCore.QSize(221, 31))
        self.envFTWxSelect.setMaximumSize(QtCore.QSize(221, 31))
        self.envFTWxSelect.setObjectName("envFTWxSelect")
        self.gridLayout.addWidget(self.envFTWxSelect, 2, 1, 1, 1)
        self.layoutWidget = QtGui.QWidget(EnviroEntryDlg)
        self.layoutWidget.setGeometry(QtCore.QRect(8, 18, 241, 161))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_7 = QtGui.QLabel(self.layoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.enviroID_display = QtGui.QLineEdit(self.layoutWidget)
        self.enviroID_display.setMaximumSize(QtCore.QSize(120, 27))
        self.enviroID_display.setStyleSheet("background-color: rgb(194, 190, 186);")
        self.enviroID_display.setMaxLength(7)
        self.enviroID_display.setReadOnly(True)
        self.enviroID_display.setObjectName("enviroID_display")
        self.gridLayout_2.addWidget(self.enviroID_display, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.matchID_display = QtGui.QLineEdit(self.layoutWidget)
        self.matchID_display.setMaximumSize(QtCore.QSize(120, 27))
        self.matchID_display.setStyleSheet("background-color: rgb(194, 190, 186);")
        self.matchID_display.setMaxLength(7)
        self.matchID_display.setReadOnly(True)
        self.matchID_display.setObjectName("matchID_display")
        self.gridLayout_2.addWidget(self.matchID_display, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.envKOTimeEdit = QtGui.QLineEdit(self.layoutWidget)
        self.envKOTimeEdit.setMinimumSize(QtCore.QSize(71, 27))
        self.envKOTimeEdit.setMaximumSize(QtCore.QSize(71, 27))
        self.envKOTimeEdit.setMaxLength(5)
        self.envKOTimeEdit.setObjectName("envKOTimeEdit")
        self.gridLayout_2.addWidget(self.envKOTimeEdit, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.envKOTempEdit = QtGui.QLineEdit(self.layoutWidget)
        self.envKOTempEdit.setMinimumSize(QtCore.QSize(71, 27))
        self.envKOTempEdit.setMaximumSize(QtCore.QSize(71, 27))
        self.envKOTempEdit.setMaxLength(5)
        self.envKOTempEdit.setObjectName("envKOTempEdit")
        self.gridLayout_2.addWidget(self.envKOTempEdit, 3, 1, 1, 1)
        self.layoutWidget1 = QtGui.QWidget(EnviroEntryDlg)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 330, 331, 41))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(238, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.closeButton = QtGui.QPushButton(self.layoutWidget1)
        self.closeButton.setMinimumSize(QtCore.QSize(85, 27))
        self.closeButton.setMaximumSize(QtCore.QSize(85, 27))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/quit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.label_7.setBuddy(self.matchID_display)
        self.label.setBuddy(self.matchID_display)
        self.label_2.setBuddy(self.envKOTimeEdit)
        self.label_3.setBuddy(self.envKOTempEdit)

        self.retranslateUi(EnviroEntryDlg)
        QtCore.QMetaObject.connectSlotsByName(EnviroEntryDlg)

    def retranslateUi(self, EnviroEntryDlg):
        EnviroEntryDlg.setWindowTitle(QtGui.QApplication.translate("EnviroEntryDlg", "Environmental Conditions", None, QtGui.QApplication.UnicodeUTF8))
        self.weatherBox.setTitle(QtGui.QApplication.translate("EnviroEntryDlg", "Weather Conditions", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("EnviroEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Kickoff</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.envKOWxSelect.setToolTip(QtGui.QApplication.translate("EnviroEntryDlg", "Weather conditions at kickoff", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("EnviroEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Halftime</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.envHTWxSelect.setToolTip(QtGui.QApplication.translate("EnviroEntryDlg", "Weather conditions at halftime", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("EnviroEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Fulltime</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.envFTWxSelect.setToolTip(QtGui.QApplication.translate("EnviroEntryDlg", "Weather conditions at end of match", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("EnviroEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Enviro ID</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("EnviroEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Match ID</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("EnviroEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Time</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.envKOTimeEdit.setToolTip(QtGui.QApplication.translate("EnviroEntryDlg", "Local time at kickoff (24-hr HH:MM)", None, QtGui.QApplication.UnicodeUTF8))
        self.envKOTimeEdit.setInputMask(QtGui.QApplication.translate("EnviroEntryDlg", "99:99; ", None, QtGui.QApplication.UnicodeUTF8))
        self.envKOTimeEdit.setText(QtGui.QApplication.translate("EnviroEntryDlg", "19:00", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("EnviroEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Temperature</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.envKOTempEdit.setToolTip(QtGui.QApplication.translate("EnviroEntryDlg", "Ambient temperature at kickoff (deg C)", None, QtGui.QApplication.UnicodeUTF8))
        self.envKOTempEdit.setInputMask(QtGui.QApplication.translate("EnviroEntryDlg", "###.#; ", None, QtGui.QApplication.UnicodeUTF8))
        self.envKOTempEdit.setText(QtGui.QApplication.translate("EnviroEntryDlg", "+20.0", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("EnviroEntryDlg", "&Close", None, QtGui.QApplication.UnicodeUTF8))

import fmrd_resources_rc
