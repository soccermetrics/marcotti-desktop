#!/usr/bin/env python
#
#    Desktop-based data entry tool for the Football Match Result Database (FMRD)
#
#    Copyright (C) 2010-2012, Howard Hamilton
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

import platform
from PyQt4.QtCore import *
from PyQt4.QtGui import *

"""Contains functions that produce Message Box popups to alert user to program events."""

def DisplayAboutDialog(parent, version, db_version):
    """Display information about the application and current version."""
    QMessageBox.about(parent, "About FMRD-Desktop", 
                      """<p align="center"> <b>FMRD-Desktop</b> %s <br>
                    Copyright &copy; 2010-2012 by Howard Hamilton.  All rights reserved.<br>
                    This is the desktop-based data entry tool for the<br>
                    <b>Football Match Result Database</b> %s <br>
                    Python %s - Qt %s - PyQt %s on %s</p>""" % 
                    (version, db_version, platform.python_version(), QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))

def SaveDiscardOptionPrompt(parent):
    """Displays pop-up question box to ask user to save or discard current data record upon dialog closure."""
    reply = QMessageBox.question(parent, "Unsaved Record", 
                                 """Would you like to <b>save</b> or <b>discard</b> the current record?""", 
                                 QMessageBox.Save|QMessageBox.Discard)
    if reply == QMessageBox.Save:
        return True
    else:
        return False    

def SubstitutesErrorPrompt(parent):
    """Displays pop-up message box to alert user of insufficient number of subs in Lineup table."""
    QMessageBox.critical(parent, "Insufficient Lineup Table", 
                         """You need at least <b>THREE</b> substitutes in Lineup table""", QMessageBox.Close)

def MatchErrorPrompt(parent):
    """Displays pop-up message box to alert user of incomplete support tables for Match entry."""
    QMessageBox.critical(parent, "Cannot enter Match data", 
                         """In order to enter data in Match table, please ensure the following:<br>
                         -- at least <b>ONE</b> entry in Competitions table<br>
                         -- at least <b>ONE</b> entry in Venues table<br>
                         -- at least <b>TWO</b> entries in Managers table<br>
                         -- at least <b>ONE</b> entry in Referees table""", QMessageBox.Close)

def KnockoutMatchErrorPrompt(parent):
    """Displays pop-up message box to alert user of insufficient number of entries in KnockoutMatches table."""
    QMessageBox.critical(parent, "Insufficient Knockout Match Table", 
                         """You need at least <b>ONE</b> entry in Knockout Matches table""", QMessageBox.Close)

def MatchDetailErrorPrompt(parent):
    """Displays pop-up message box to alert user of insufficient data in Lineup table."""
    QMessageBox.critical(parent, "Insufficient Lineup Table", 
                         """You need at least <b>11</b> starting players in Lineup table, of which<br>
                         <b>ONE</b> is designated captain<br>
                         <b>ONE</b> is designated goalkeeper""", QMessageBox.Close)

def LineupErrorPrompt(parent):
    """Displays pop-up message box to alert user of insufficient data in Lineup table."""
    QMessageBox.critical(parent, "Insufficient Team Lineup Entries", 
                         """You need exactly <b>11</b> starting players in the team lineup, of which<br>
                         <b>ONE</b> is designated captain<br>
                         <b>ONE</b> is designated goalkeeper""", QMessageBox.Close)

def DeletionErrorPrompt(parent):
    """Displays pop-up message box to alert user of existing records that depend on parent record to be deleted."""
    QMessageBox.critical(parent, "Cannot Delete Record", 
                         """There are records in child tables dependent on this record.<br>
                         Please delete child records that refer to this record first.""", QMessageBox.Close)

def DatabaseCommitErrorPrompt(parent, error):
    """Displays pop-up message box to alert user of database record commit error."""
    QMessageBox.critical(parent, "Database Commit Error", 
                         """Error Code %d: %s""" % (error.number(), error.text()), QMessageBox.Close)
                         
def DuplicateRecordErrorPrompt(parent, table, desc):
    """Displays pop-up message box to alert user of identical record already in database."""
    QMessageBox.critical(parent, "Identical Record in Database", 
                         """There is already a record in %s with descriptor '%s' """ % (table, desc), QMessageBox.Close)