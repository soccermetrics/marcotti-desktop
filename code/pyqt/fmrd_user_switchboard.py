#!/usr/bin/env python
#
#    Football Match Result Database (FMRD)
#    Desktop-based data entry tool
#
#    Implements the Main User Switchboard for the FMRD data entry tool.
#    Instantiates objects that handle data entry interfaces for the 
#    setup and main tables.
# 
#    Copyright (C) 2010-2011, Howard Hamilton
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import functools
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from FmrdMain import ui_usermainswitchboard
from FmrdLib.CheckTables import *
from FmrdLib.MsgPrompts import *

from fmrd_setup import AboutDlg
from fmrd_match import *
from fmrd_matchevent import *
from fmrd_overview import *
from fmrd_personnel import *

# Class: UserMainSwitchboard
# Inherits: Ui_UserMainSwitchboard (ui_usermainswitchboard)
#
# Implements switchboard console in FMRD data entry tool.
# For end-users only (no admin privileges).
class UserMainSwitchboard(QMainWindow, ui_usermainswitchboard.Ui_UserMainSwitchboard):
    
    def __init__(self, parent=None):
        super(UserMainSwitchboard, self).__init__(parent)
        self.setupUi(self) 
        
        # center window in screen
        desktop = QDesktopWidget()
        mainScreen = desktop.screen(desktop.primaryScreen())
        
        screenWidth = mainScreen.width()
        screenHeight = mainScreen.height()
        
        windowSize = self.size()
        windowWidth = windowSize.width()
        windowHeight = windowSize.height()
        
        x = (screenWidth - windowWidth) / 2
        y = (screenHeight - windowHeight) / 2
        y -= 50
 
        self.move ( x, y )

        # configure signal/slot connections for buttons
        QObject.connect(self.compButton, SIGNAL("clicked()"), self.OpenCompetitions)
        QObject.connect(self.teamButton, SIGNAL("clicked()"), self.OpenTeams)
        QObject.connect(self.venueButton, SIGNAL("clicked()"), self.OpenVenues)
        QObject.connect(self.playerButton, SIGNAL("clicked()"), self.OpenPlayers)
        QObject.connect(self.managerButton, SIGNAL("clicked()"), self.OpenManagers)
        QObject.connect(self.refereeButton, SIGNAL("clicked()"), self.OpenReferees)
        QObject.connect(self.matchButton, SIGNAL("clicked()"), self.OpenMatches)
        QObject.connect(self.goalButton, SIGNAL("clicked()"), self.OpenGoals)
        QObject.connect(self.penButton, SIGNAL("clicked()"), self.OpenPenalties)
        QObject.connect(self.offenseButton, SIGNAL("clicked()"), self.OpenOffenses)
        QObject.connect(self.subButton, SIGNAL("clicked()"), self.OpenSubstitutions)
        QObject.connect(self.switchButton, SIGNAL("clicked()"), self.OpenPosSwitches)
        
        # signal/slot connections for menu actions
        QObject.connect(self.actionAbout, SIGNAL("triggered()"), self.OpenAbout)
     
     # routines for opening menu dialogs
     
    def OpenAbout(self):
        dialog = AboutDlg(self)
        dialog.exec_()
    
    # routines for opening main dialogs (access by pushbuttons)
    
    def OpenCompetitions(self):
        dialog = compEntryDlg(self)
        dialog.exec_()
                
    def OpenTeams(self):
        dialog = teamEntryDlg(self)
        dialog.exec_()
        
    def OpenPlayers(self):
        dialog = playerEntryDlg(self)
        dialog.exec_()
        
    def OpenManagers(self):
        dialog = managerEntryDlg(self)
        dialog.exec_()
        
    def OpenReferees(self):
        dialog = refereeEntryDlg(self)
        dialog.exec_()

    def OpenVenues(self):
        if not CheckMinimumVenueHosts():
            VenueErrorPrompt(self)
        else:
            dialog = venueEntryDlg(self)
            dialog.exec_()
        
    def OpenMatches(self):
        if not CheckMinimumMatchCriteria():
            MatchErrorPrompt(self)
        else:
            dialog = matchEntryDlg(self)
            dialog.exec_()

    def OpenGoals(self):
        if not CheckMinimumLineups():
            MatchDetailErrorPrompt(self)
        else:
            dialog = goalEntryDlg(self)
            dialog.exec_()
        
    def OpenPenalties(self):
        if not CheckMinimumLineups():
            MatchDetailErrorPrompt(self)
        else:
            dialog = penaltyEntryDlg(self)
            dialog.exec_()
        
    def OpenOffenses(self):
        if not CheckMinimumLineups():
            MatchDetailErrorPrompt(self)
        else:      
            dialog = offenseEntryDlg(self)
            dialog.exec_()
        
    def OpenSubstitutions(self):
        if not CheckMinimumSubstitutes():
            SubstitutesErrorPrompt(self)
        else:
            dialog = subsEntryDlg(self)
            dialog.exec_()
        
    def OpenPosSwitches(self):
        if not CheckMinimumLineups():
            MatchDetailErrorPrompt(self)
        else:        
            dialog = switchEntryDlg(self)
            dialog.exec_()
        
    def close(self):
        sys.exit()
