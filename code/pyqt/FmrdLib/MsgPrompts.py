#!/usr/bin/env python
#
#    Football Match Result Database (FMRD)
#    Desktop-based data entry tool
#
#    Contains functions that produce Message Box popups to alert user to errors.
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *



# Method: VenueErrorPrompt
#
# Pop-up message box to alert user of insufficient number of teams in Venues table
def VenueErrorPrompt(parent):
    QMessageBox.critical(parent, "Insufficient Teams Table", 
                         """You need at least <b>ONE</b> entry in Teams table""", QMessageBox.Close)
    

# Method: SubstitutesErrorPrompt
#
# Pop-up message box to alert user of insufficient number of subs in Lineup table
def SubstitutesErrorPrompt(parent):
    QMessageBox.critical(parent, "Insufficient Lineup Table", 
                         """You need at least <b>THREE</b> substitutes in Lineup table""", QMessageBox.Close)


# Method: MatchErrorPrompt
#
# Pop-up message box to alert user of incomplete support tables for Match entry
def MatchErrorPrompt(parent):
    QMessageBox.critical(parent, "Cannot enter Match data", 
                         """In order to enter data in Match table, please ensure the following:<br>
                         -- at least <b>ONE</b> entry in Competitions table<br>
                         -- at least <b>TWO</b> entries in Teams table<br>
                         -- at least <b>ONE</b> entry in Venues table<br>
                         -- at least <b>TWO</b> entries in Managers table<br>
                         -- at least <b>ONE</b> entry in Referees table""", QMessageBox.Close)
    

# Method: MatchDetailErrorPrompt
#
# Pop-up message box to alert user of insufficient data in Lineup table
def MatchDetailErrorPrompt(parent):
    QMessageBox.critical(parent, "Insufficient Lineup Table", 
                         """You need at least <b>11</b> starting players in Lineup table, of which<br>
                         <b>ONE</b> is designated captain<br>
                         <b>ONE</b> is designated goalkeeper""", QMessageBox.Close)


def LineupErrorPrompt(parent):
    QMessageBox.critical(parent, "Insufficient Team Lineup Entries", 
                         """You need exactly <b>11</b> starting players in the team lineup, of which<br>
                         <b>ONE</b> is designated captain<br>
                         <b>ONE</b> is designated goalkeeper""", QMessageBox.Close)
                         
def DeletionErrorPrompt(parent):
    QMessageBox.critical(parent, "Cannot Delete Record", 
                         """There are records in child tables dependent on this record.<br>
                         Please delete child records that refer to this record first.""", QMessageBox.Close)
