# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/venue_entry.ui'
#
# Created: Sat Aug  6 01:32:18 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_VenueEntryDlg(object):
    def setupUi(self, VenueEntryDlg):
        VenueEntryDlg.setObjectName("VenueEntryDlg")
        VenueEntryDlg.resize(720, 360)
        VenueEntryDlg.setMinimumSize(QtCore.QSize(720, 360))
        VenueEntryDlg.setMaximumSize(QtCore.QSize(720, 360))
        self.frame_2 = QtGui.QFrame(VenueEntryDlg)
        self.frame_2.setGeometry(QtCore.QRect(20, 280, 341, 51))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.firstEntry = QtGui.QPushButton(self.frame_2)
        self.firstEntry.setGeometry(QtCore.QRect(10, 10, 71, 33))
        self.firstEntry.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/first.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.firstEntry.setIcon(icon)
        self.firstEntry.setObjectName("firstEntry")
        self.prevEntry = QtGui.QPushButton(self.frame_2)
        self.prevEntry.setGeometry(QtCore.QRect(90, 10, 71, 33))
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
        self.frame = QtGui.QFrame(VenueEntryDlg)
        self.frame.setGeometry(QtCore.QRect(410, 280, 281, 51))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.addEntry = QtGui.QPushButton(self.frame)
        self.addEntry.setGeometry(QtCore.QRect(10, 10, 80, 31))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addEntry.setIcon(icon4)
        self.addEntry.setObjectName("addEntry")
        self.deleteEntry = QtGui.QPushButton(self.frame)
        self.deleteEntry.setGeometry(QtCore.QRect(100, 10, 80, 31))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteEntry.setIcon(icon5)
        self.deleteEntry.setObjectName("deleteEntry")
        self.closeButton = QtGui.QPushButton(self.frame)
        self.closeButton.setGeometry(QtCore.QRect(190, 10, 80, 31))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/quit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon6)
        self.closeButton.setObjectName("closeButton")
        self.line = QtGui.QFrame(VenueEntryDlg)
        self.line.setGeometry(QtCore.QRect(400, 10, 20, 241))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.layoutWidget = QtGui.QWidget(VenueEntryDlg)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 11, 391, 241))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.venueID_display = QtGui.QLineEdit(self.layoutWidget)
        self.venueID_display.setMaximumSize(QtCore.QSize(100, 27))
        self.venueID_display.setStyleSheet("background-color: rgb(194, 190, 186);")
        self.venueID_display.setReadOnly(True)
        self.venueID_display.setObjectName("venueID_display")
        self.gridLayout.addWidget(self.venueID_display, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.venueNameEdit = QtGui.QLineEdit(self.layoutWidget)
        self.venueNameEdit.setMinimumSize(QtCore.QSize(255, 27))
        self.venueNameEdit.setMaximumSize(QtCore.QSize(255, 27))
        self.venueNameEdit.setObjectName("venueNameEdit")
        self.gridLayout.addWidget(self.venueNameEdit, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.venueCityEdit = QtGui.QLineEdit(self.layoutWidget)
        self.venueCityEdit.setMinimumSize(QtCore.QSize(255, 27))
        self.venueCityEdit.setMaximumSize(QtCore.QSize(255, 27))
        self.venueCityEdit.setObjectName("venueCityEdit")
        self.gridLayout.addWidget(self.venueCityEdit, 2, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.venueConfedSelect = QtGui.QComboBox(self.layoutWidget)
        self.venueConfedSelect.setMinimumSize(QtCore.QSize(255, 31))
        self.venueConfedSelect.setMaximumSize(QtCore.QSize(255, 31))
        self.venueConfedSelect.setWhatsThis("")
        self.venueConfedSelect.setObjectName("venueConfedSelect")
        self.gridLayout.addWidget(self.venueConfedSelect, 3, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.venueCountrySelect = QtGui.QComboBox(self.layoutWidget)
        self.venueCountrySelect.setMinimumSize(QtCore.QSize(255, 31))
        self.venueCountrySelect.setMaximumSize(QtCore.QSize(255, 31))
        self.venueCountrySelect.setObjectName("venueCountrySelect")
        self.gridLayout.addWidget(self.venueCountrySelect, 4, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)
        self.venueTeamSelect = QtGui.QComboBox(self.layoutWidget)
        self.venueTeamSelect.setMinimumSize(QtCore.QSize(255, 31))
        self.venueTeamSelect.setMaximumSize(QtCore.QSize(255, 31))
        self.venueTeamSelect.setObjectName("venueTeamSelect")
        self.gridLayout.addWidget(self.venueTeamSelect, 5, 1, 1, 1)
        self.layoutWidget1 = QtGui.QWidget(VenueEntryDlg)
        self.layoutWidget1.setGeometry(QtCore.QRect(420, 70, 281, 121))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.venueAltEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.venueAltEdit.setMinimumSize(QtCore.QSize(81, 27))
        self.venueAltEdit.setMaximumSize(QtCore.QSize(81, 27))
        self.venueAltEdit.setMaxLength(5)
        self.venueAltEdit.setObjectName("venueAltEdit")
        self.gridLayout_2.addWidget(self.venueAltEdit, 0, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.layoutWidget1)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)
        self.venueLatitudeEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.venueLatitudeEdit.setMinimumSize(QtCore.QSize(100, 27))
        self.venueLatitudeEdit.setMaximumSize(QtCore.QSize(100, 27))
        self.venueLatitudeEdit.setMaxLength(11)
        self.venueLatitudeEdit.setObjectName("venueLatitudeEdit")
        self.gridLayout_2.addWidget(self.venueLatitudeEdit, 1, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.layoutWidget1)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)
        self.venueLongitudeEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.venueLongitudeEdit.setMinimumSize(QtCore.QSize(100, 27))
        self.venueLongitudeEdit.setMaximumSize(QtCore.QSize(100, 27))
        self.venueLongitudeEdit.setMaxLength(11)
        self.venueLongitudeEdit.setObjectName("venueLongitudeEdit")
        self.gridLayout_2.addWidget(self.venueLongitudeEdit, 2, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.layoutWidget1)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.label.setBuddy(self.venueID_display)
        self.label_4.setBuddy(self.venueNameEdit)
        self.label_5.setBuddy(self.venueCityEdit)
        self.label_6.setBuddy(self.venueConfedSelect)
        self.label_3.setBuddy(self.venueCountrySelect)
        self.label_2.setBuddy(self.venueTeamSelect)
        self.label_8.setBuddy(self.venueLatitudeEdit)
        self.label_9.setBuddy(self.venueLongitudeEdit)
        self.label_7.setBuddy(self.venueAltEdit)

        self.retranslateUi(VenueEntryDlg)
        QtCore.QMetaObject.connectSlotsByName(VenueEntryDlg)

    def retranslateUi(self, VenueEntryDlg):
        VenueEntryDlg.setWindowTitle(QtGui.QApplication.translate("VenueEntryDlg", "Venue Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.firstEntry.setToolTip(QtGui.QApplication.translate("VenueEntryDlg", "First Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.prevEntry.setToolTip(QtGui.QApplication.translate("VenueEntryDlg", "Previous Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.nextEntry.setToolTip(QtGui.QApplication.translate("VenueEntryDlg", "Next Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.lastEntry.setToolTip(QtGui.QApplication.translate("VenueEntryDlg", "Last Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.addEntry.setToolTip(QtGui.QApplication.translate("VenueEntryDlg", "Add Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.addEntry.setText(QtGui.QApplication.translate("VenueEntryDlg", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteEntry.setToolTip(QtGui.QApplication.translate("VenueEntryDlg", "Delete Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteEntry.setText(QtGui.QApplication.translate("VenueEntryDlg", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setToolTip(QtGui.QApplication.translate("VenueEntryDlg", "Close Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("VenueEntryDlg", "&Close", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("VenueEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">&amp;ID</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("VenueEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">&amp;Venue Name</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.venueNameEdit.setToolTip(QtGui.QApplication.translate("VenueEntryDlg", "Name of football venue", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("VenueEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Venue &amp;City</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.venueCityEdit.setToolTip(QtGui.QApplication.translate("VenueEntryDlg", "City of football venue", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("VenueEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Con&amp;federation</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.venueConfedSelect.setToolTip(QtGui.QApplication.translate("VenueEntryDlg", "Football confederation", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("VenueEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Cou&amp;ntry</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.venueCountrySelect.setToolTip(QtGui.QApplication.translate("VenueEntryDlg", "Country of football venue", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("VenueEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Home &amp;Team</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.venueTeamSelect.setToolTip(QtGui.QApplication.translate("VenueEntryDlg", "Home team of football venue", None, QtGui.QApplication.UnicodeUTF8))
        self.venueAltEdit.setToolTip(QtGui.QApplication.translate("VenueEntryDlg", "Altitude above mean sea level (meters)", None, QtGui.QApplication.UnicodeUTF8))
        self.venueAltEdit.setInputMask(QtGui.QApplication.translate("VenueEntryDlg", "#0000; ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("VenueEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Latitude (deg)</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.venueLatitudeEdit.setToolTip(QtGui.QApplication.translate("VenueEntryDlg", "Geographic latitude of venue (decimal degrees)", None, QtGui.QApplication.UnicodeUTF8))
        self.venueLatitudeEdit.setInputMask(QtGui.QApplication.translate("VenueEntryDlg", "#000.000000; ", None, QtGui.QApplication.UnicodeUTF8))
        self.venueLatitudeEdit.setText(QtGui.QApplication.translate("VenueEntryDlg", "-000.000000", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("VenueEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Longitude (deg)</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.venueLongitudeEdit.setToolTip(QtGui.QApplication.translate("VenueEntryDlg", "Geographic longitude of venue (decimal degrees)", None, QtGui.QApplication.UnicodeUTF8))
        self.venueLongitudeEdit.setInputMask(QtGui.QApplication.translate("VenueEntryDlg", "#000.000000; ", None, QtGui.QApplication.UnicodeUTF8))
        self.venueLongitudeEdit.setText(QtGui.QApplication.translate("VenueEntryDlg", "-000.000000", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("VenueEntryDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Altitude (m)</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

import fmrd_resources_rc
