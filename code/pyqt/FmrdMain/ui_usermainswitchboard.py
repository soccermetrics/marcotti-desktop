# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_userswitchboard.ui'
#
# Created: Fri Apr  1 21:10:58 2011
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_UserMainSwitchboard(object):
    def setupUi(self, UserMainSwitchboard):
        UserMainSwitchboard.setObjectName("UserMainSwitchboard")
        UserMainSwitchboard.resize(360, 420)
        UserMainSwitchboard.setMinimumSize(QtCore.QSize(360, 420))
        UserMainSwitchboard.setMaximumSize(QtCore.QSize(360, 420))
        self.centralwidget = QtGui.QWidget(UserMainSwitchboard)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.compButton = QtGui.QPushButton(self.groupBox)
        self.compButton.setObjectName("compButton")
        self.verticalLayout.addWidget(self.compButton)
        self.teamButton = QtGui.QPushButton(self.groupBox)
        self.teamButton.setObjectName("teamButton")
        self.verticalLayout.addWidget(self.teamButton)
        self.venueButton = QtGui.QPushButton(self.groupBox)
        self.venueButton.setObjectName("venueButton")
        self.verticalLayout.addWidget(self.venueButton)
        self.verticalLayout_4.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.playerButton = QtGui.QPushButton(self.groupBox_2)
        self.playerButton.setObjectName("playerButton")
        self.verticalLayout_2.addWidget(self.playerButton)
        self.refereeButton = QtGui.QPushButton(self.groupBox_2)
        self.refereeButton.setObjectName("refereeButton")
        self.verticalLayout_2.addWidget(self.refereeButton)
        self.managerButton = QtGui.QPushButton(self.groupBox_2)
        self.managerButton.setObjectName("managerButton")
        self.verticalLayout_2.addWidget(self.managerButton)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 1, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.matchButton = QtGui.QPushButton(self.groupBox_3)
        self.matchButton.setObjectName("matchButton")
        self.verticalLayout_3.addWidget(self.matchButton)
        self.goalButton = QtGui.QPushButton(self.groupBox_3)
        self.goalButton.setObjectName("goalButton")
        self.verticalLayout_3.addWidget(self.goalButton)
        self.penButton = QtGui.QPushButton(self.groupBox_3)
        self.penButton.setObjectName("penButton")
        self.verticalLayout_3.addWidget(self.penButton)
        self.offenseButton = QtGui.QPushButton(self.groupBox_3)
        self.offenseButton.setObjectName("offenseButton")
        self.verticalLayout_3.addWidget(self.offenseButton)
        self.subButton = QtGui.QPushButton(self.groupBox_3)
        self.subButton.setObjectName("subButton")
        self.verticalLayout_3.addWidget(self.subButton)
        self.switchButton = QtGui.QPushButton(self.groupBox_3)
        self.switchButton.setObjectName("switchButton")
        self.verticalLayout_3.addWidget(self.switchButton)
        self.gridLayout.addWidget(self.groupBox_3, 0, 2, 1, 1)
        UserMainSwitchboard.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(UserMainSwitchboard)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 360, 23))
        self.menubar.setObjectName("menubar")
        self.menuMain = QtGui.QMenu(self.menubar)
        self.menuMain.setObjectName("menuMain")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        UserMainSwitchboard.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(UserMainSwitchboard)
        self.statusbar.setObjectName("statusbar")
        UserMainSwitchboard.setStatusBar(self.statusbar)
        self.actionQuit = QtGui.QAction(UserMainSwitchboard)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtGui.QAction(UserMainSwitchboard)
        self.actionAbout.setObjectName("actionAbout")
        self.actionRounds = QtGui.QAction(UserMainSwitchboard)
        self.actionRounds.setObjectName("actionRounds")
        self.actionWeather_Conditions = QtGui.QAction(UserMainSwitchboard)
        self.actionWeather_Conditions.setObjectName("actionWeather_Conditions")
        self.actionConfederations = QtGui.QAction(UserMainSwitchboard)
        self.actionConfederations.setObjectName("actionConfederations")
        self.actionCountries = QtGui.QAction(UserMainSwitchboard)
        self.actionCountries.setObjectName("actionCountries")
        self.actionField_Positions = QtGui.QAction(UserMainSwitchboard)
        self.actionField_Positions.setObjectName("actionField_Positions")
        self.actionFlank_Positions = QtGui.QAction(UserMainSwitchboard)
        self.actionFlank_Positions.setObjectName("actionFlank_Positions")
        self.actionPositions = QtGui.QAction(UserMainSwitchboard)
        self.actionPositions.setObjectName("actionPositions")
        self.actionGoal_Events = QtGui.QAction(UserMainSwitchboard)
        self.actionGoal_Events.setObjectName("actionGoal_Events")
        self.actionGoal_Strikes = QtGui.QAction(UserMainSwitchboard)
        self.actionGoal_Strikes.setObjectName("actionGoal_Strikes")
        self.actionPenalty_Outcomes = QtGui.QAction(UserMainSwitchboard)
        self.actionPenalty_Outcomes.setObjectName("actionPenalty_Outcomes")
        self.actionFouls = QtGui.QAction(UserMainSwitchboard)
        self.actionFouls.setObjectName("actionFouls")
        self.actionCards = QtGui.QAction(UserMainSwitchboard)
        self.actionCards.setObjectName("actionCards")
        self.menuMain.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuMain.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(UserMainSwitchboard)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL("triggered()"), UserMainSwitchboard.close)
        QtCore.QMetaObject.connectSlotsByName(UserMainSwitchboard)

    def retranslateUi(self, UserMainSwitchboard):
        UserMainSwitchboard.setWindowTitle(QtGui.QApplication.translate("UserMainSwitchboard", "FMRD Switchboard", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("UserMainSwitchboard", "Match Overview", None, QtGui.QApplication.UnicodeUTF8))
        self.compButton.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Competitions", None, QtGui.QApplication.UnicodeUTF8))
        self.teamButton.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Teams", None, QtGui.QApplication.UnicodeUTF8))
        self.venueButton.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Venues", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("UserMainSwitchboard", "Personnel", None, QtGui.QApplication.UnicodeUTF8))
        self.playerButton.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Players", None, QtGui.QApplication.UnicodeUTF8))
        self.refereeButton.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Referees", None, QtGui.QApplication.UnicodeUTF8))
        self.managerButton.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Managers", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("UserMainSwitchboard", "Match Details", None, QtGui.QApplication.UnicodeUTF8))
        self.matchButton.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Matches", None, QtGui.QApplication.UnicodeUTF8))
        self.goalButton.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Goals", None, QtGui.QApplication.UnicodeUTF8))
        self.penButton.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Penalties", None, QtGui.QApplication.UnicodeUTF8))
        self.offenseButton.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Offenses", None, QtGui.QApplication.UnicodeUTF8))
        self.subButton.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Substitutions", None, QtGui.QApplication.UnicodeUTF8))
        self.switchButton.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Position Switches", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMain.setTitle(QtGui.QApplication.translate("UserMainSwitchboard", "&Main", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("UserMainSwitchboard", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("UserMainSwitchboard", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("UserMainSwitchboard", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("UserMainSwitchboard", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setShortcut(QtGui.QApplication.translate("UserMainSwitchboard", "F1", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRounds.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Rounds", None, QtGui.QApplication.UnicodeUTF8))
        self.actionWeather_Conditions.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Weather Conditions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConfederations.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Confederations", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCountries.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Countries", None, QtGui.QApplication.UnicodeUTF8))
        self.actionField_Positions.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Field Positions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFlank_Positions.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Flank Positions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPositions.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Positions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoal_Events.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Goal Events", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoal_Strikes.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Goal Strikes", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPenalty_Outcomes.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Penalty Outcomes", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFouls.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Fouls", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCards.setText(QtGui.QApplication.translate("UserMainSwitchboard", "Cards", None, QtGui.QApplication.UnicodeUTF8))
