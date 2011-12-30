#!/usr/bin/env python
#
#    Desktop-based data entry tool for the Football Match Result Database (FMRD)
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
from FmrdLib.Constants import *

from fmrd_match import *
from fmrd_goals import *
from fmrd_penalties import *
from fmrd_subs import *
from fmrd_offenses import *
from fmrd_shootouts import *
from fmrd_overview import *
from fmrd_personnel import *

"""Implements the Main User Switchboard for the FMRD data entry tool.

Instantiates objects that handle data entry interfaces for the 
setup and main tables.
"""


class UserMainSwitchboard(QMainWindow, ui_usermainswitchboard.Ui_UserMainSwitchboard):
    """Implements switchboard console in FMRD data entry tool.
    
    Console set up for end-users without administrative privileges.
    """
    
    def __init__(self, parent=None):
        """Constructor for UserMainSwitchboard class."""
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
        QObject.connect(self.shootoutButton, SIGNAL("clicked()"), self.OpenPenaltyShootouts)
        
        # signal/slot connections for menu actions
        QObject.connect(self.actionAbout, SIGNAL("triggered()"), self.OpenAbout)
     
     # routines for opening menu dialogs
     
    def OpenAbout(self):
        """Opens About window."""
        DisplayAboutDialog(self, Constants.DATAENTRY_VERSION, Constants.SQL_VERSION)
    
    # routines for opening main dialogs (access by pushbuttons)
    
    def OpenCompetitions(self):
        """Opens Competitions window."""
        dialog = CompEntryDlg(self)
        dialog.exec_()

    def OpenPlayers(self):
        """Opens Players window."""
        dialog = PlayerEntryDlg(self)
        dialog.exec_()
        
    def OpenManagers(self):
        """Opens Managers window."""
        dialog = ManagerEntryDlg(self)
        dialog.exec_()
        
    def OpenReferees(self):
        """Opens Referees window."""
        dialog = RefereeEntryDlg(self)
        dialog.exec_()

    def OpenVenues(self):
        """Opens Venues window."""
        dialog = VenueEntryDlg(self)
        dialog.exec_()
        
    def OpenMatches(self):
        """Opens Matches window.
        
        Window opens only if all of the conditions are met:
            (1) at least one record in Referees table
            (2) at least two records in Managers table
            (3) at least one record in Venues table
            (4) at least one record in Competitions table
            
        """
        if not CheckMinimumMatchCriteria():
            MatchErrorPrompt(self)
        else:
            dialog = MatchEntryDlg(self)
            dialog.exec_()

    def OpenGoals(self):
        """Opens Goals window.
        
        Window opens only if all of the conditions are met:
            (1) at least 11 entries in Lineups table where Starting = TRUE
            (2) at least one starting player in Lineups table where Captain = TRUE
            (3) at least one starting player in Lineups table at Goalkeeper position

        """
        if not CheckMinimumLineups():
            MatchDetailErrorPrompt(self)
        else:
            dialog = GoalEntryDlg(self)
            dialog.exec_()
        
    def OpenPenalties(self):
        """Opens Penalties window.
        
        Window opens only if all of the conditions are met:
            (1) at least 11 entries in Lineups table where Starting = TRUE
            (2) at least one starting player in Lineups table where Captain = TRUE
            (3) at least one starting player in Lineups table at Goalkeeper position

        """        
        if not CheckMinimumLineups():
            MatchDetailErrorPrompt(self)
        else:
            dialog = PenaltyEntryDlg(self)
            dialog.exec_()
        
    def OpenOffenses(self):
        """Opens Offenses window.
        
        Window opens only if all of the conditions are met:
            (1) at least 11 entries in Lineups table where Starting = TRUE
            (2) at least one starting player in Lineups table where Captain = TRUE
            (3) at least one starting player in Lineups table at Goalkeeper position

        """
        if not CheckMinimumLineups():
            MatchDetailErrorPrompt(self)
        else:      
            dialog = OffenseEntryDlg(self)
            dialog.exec_()
        
    def OpenSubstitutions(self):
        """Opens Substitutions window.
        
        Window opens if there is at least one record in Lineups table where Starting = FALSE.
        
        """
        if not CheckMinimumSubstitutes():
            SubstitutesErrorPrompt(self)
        else:
            dialog = SubsEntryDlg(self)
            dialog.exec_()
        
    def OpenPosSwitches(self):
        """Opens Position Switches window.
        
        Window opens only if all of the conditions are met:
            (1) at least 11 entries in Lineups table where Starting = TRUE
            (2) at least one starting player in Lineups table where Captain = TRUE
            (3) at least one starting player in Lineups table at Goalkeeper position

        """
        if not CheckMinimumLineups():
            MatchDetailErrorPrompt(self)
        else:        
            dialog = SwitchEntryDlg(self)
            dialog.exec_()
            
    def OpenPenaltyShootouts(self):
        """Opens Penalty Kick Shootouts window.
        
        Window opens only if there is at least one record in KnockoutMatches table.
        """
        if not CheckMinimumKnockoutMatches():
            KnockoutMatchErrorPrompt(self)
        else:
            dialog = PenShootoutEntryDlg(self)
            dialog.exec_()
        
    def close(self):
        """Hides Switchboard window and exits application."""
        sys.exit()
