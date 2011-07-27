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

from FmrdMain import ui_mainswitchboard
from FmrdLib.CheckTables import *
from FmrdLib.MsgPrompts import *

from fmrd_setup import *
from fmrd_match import *
from fmrd_matchevent import *
from fmrd_overview import *
from fmrd_personnel import *

"""Implements the Main Switchboard for the FMRD data entry tool.

Instantiates objects that handle data entry interfaces for the 
setup and main tables. 

"""


class MainSwitchboard(QMainWindow, ui_mainswitchboard.Ui_MainSwitchboard):
    """Implements switchboard console for FMRD data entry tool.
   
    Console set up for users with administrative privileges.
   
    """
   
    def __init__(self, parent=None):
        """Constructor for MainSwitchboard class."""
        super(MainSwitchboard, self).__init__(parent)
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
        QObject.connect(self.actionRounds, SIGNAL("triggered()"), self.OpenRounds)
        QObject.connect(self.actionWeather_Conditions,  SIGNAL("triggered()"), self.OpenWeatherConditions)
        QObject.connect(self.actionConfederations, SIGNAL("triggered()"), self.OpenConfederations)
        QObject.connect(self.actionCountries, SIGNAL("triggered()"), self.OpenCountries)
        QObject.connect(self.actionField_Positions, SIGNAL("triggered()"), self.OpenFieldPositions)
        QObject.connect(self.actionFlank_Positions, SIGNAL("triggered()"), self.OpenFlankPositions)
        QObject.connect(self.actionPositions, SIGNAL("triggered()"), self.OpenPositions)
        QObject.connect(self.actionGoal_Strikes, SIGNAL("triggered()"), self.OpenGoalStrikes)
        QObject.connect(self.actionGoal_Events, SIGNAL("triggered()"), self.OpenGoalEvents)
        QObject.connect(self.actionPenalty_Outcomes, SIGNAL("triggered()"), self.OpenPenOutcomes)
        QObject.connect(self.actionFouls, SIGNAL("triggered()"), self.OpenFouls)
        QObject.connect(self.actionCards, SIGNAL("triggered()"), self.OpenCards)
        QObject.connect(self.actionAbout, SIGNAL("triggered()"), self.OpenAbout)
    
    # routines for opening menu dialogs
     
    def OpenAbout(self):
        """Opens About window."""
        dialog = AboutDlg(self)
        dialog.exec_()
        
    def OpenCards(self):
        """Opens Disciplinary Cards window."""
        dialog = cardSetupDlg(self)
        dialog.exec_()
        
    def OpenFouls(self):
        """Opens Fouls window."""
        dialog = foulSetupDlg(self)
        dialog.exec_()
        
    def OpenPenOutcomes(self):
        """Opens Penalty Outcomes window."""
        dialog = penSetupDlg(self)
        dialog.exec_()
        
    def OpenGoalEvents(self):
        """Opens Goal Events window."""
        dialog = goaleventSetupDlg(self)
        dialog.exec_()
        
    def OpenGoalStrikes(self):
        """Opens Goal Strikes window."""
        dialog = goalstrikeSetupDlg(self)
        dialog.exec_()
        
    def OpenFieldPositions(self):
        """Opens Field Position Name window."""
        dialog = fieldposSetupDlg(self)
        dialog.exec_()
        
    def OpenFlankPositions(self):
        """Opens Flank Name window."""
        dialog = flankposSetupDlg(self)
        dialog.exec_()
        
    def OpenPositions(self):
        """Opens composite Position Name window."""
        dialog = posSetupDlg(self)
        dialog.exec_()
        
    def OpenCountries(self):
        """Opens Country window."""
        dialog = countrySetupDlg(self)
        dialog.exec_()
        
    def OpenConfederations(self):
        """Opens Confederation window."""
        dialog = confedSetupDlg(self)
        dialog.exec_()
        
    def OpenRounds(self):
        """Opens Matchday (Rounds) window."""
        dialog = roundSetupDlg(self)
        dialog.exec_()
        
    def OpenWeatherConditions(self):
        """Opens Weather Conditions window."""
        dialog = wxcondSetupDlg(self)
        dialog.exec_()
        
    # routines for opening main dialogs (access by pushbuttons)
    
    def OpenCompetitions(self):
        """Opens Competitions window."""
        dialog = compEntryDlg(self)
        dialog.exec_()
                
    def OpenTeams(self):
        """Opens Teams window."""
        dialog = teamEntryDlg(self)
        dialog.exec_()
        
    def OpenPlayers(self):
        """Opens Players window."""
        dialog = playerEntryDlg(self)
        dialog.exec_()
        
    def OpenManagers(self):
        """Opens Managers window."""
        dialog = managerEntryDlg(self)
        dialog.exec_()
        
    def OpenReferees(self):
        """Opens Referees window."""
        dialog = refereeEntryDlg(self)
        dialog.exec_()

    def OpenVenues(self):
        """Opens Venues window.
        
        Window opens if there is at least one record in Teams table.
        
        """
        if not CheckMinimumVenueHosts():
            VenueErrorPrompt(self)
        else:
            dialog = venueEntryDlg(self)
            dialog.exec_()
        
    def OpenMatches(self):
        """Opens Matches window.
        
        Window opens only if all of the conditions are met:
            (1) at least one record in Referees table
            (2) at least two records in Managers table
            (3) at least two records in Teams table
            (4) at least one record in Venues table
            (5) at least one record in Competitions table
            
        """
        if not CheckMinimumMatchCriteria():
            MatchErrorPrompt(self)
        else:
            dialog = matchEntryDlg(self)
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
            dialog = goalEntryDlg(self)
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
            dialog = penaltyEntryDlg(self)
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
            dialog = offenseEntryDlg(self)
            dialog.exec_()
        
    def OpenSubstitutions(self):
        """Opens Substitutions window.
        
        Window opens if there is at least one record in Lineups table where Starting = FALSE.
        
        """
        if not CheckMinimumSubstitutes():
            SubstitutesErrorPrompt(self)
        else:
            dialog = subsEntryDlg(self)
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
            dialog = switchEntryDlg(self)
            dialog.exec_()
        
    def close(self):
        """Hides Switchboard window and exits application."""
        sys.exit()
