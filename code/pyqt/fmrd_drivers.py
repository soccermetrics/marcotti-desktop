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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from FmrdMain import ui_fmrddrivers
from FmrdLib import Constants

"""
Contains implementation of database driver dialog.

Only class: DBDriverDlg
"""

class DBDriverDlg(QDialog, ui_fmrddrivers.Ui_DBDriverDlg):
    """Implements database driver selection dialog.
    
    Inherits Ui_DBDriverDlg (ui_fmrddrivers)
    """

    def __init__(self):
        """ Constructor for DBDriverDlg class."""
        super(DBDriverDlg, self).__init__()
        self.setupUi(self)
        
        self.option = Constants.SQLITE*self.sqliteButton.isChecked() + Constants.POSTGRES*self.postgresButton.isChecked()
        self.connect(self.sqliteButton, SIGNAL("toggled()"), self.updateSelection)
        self.connect(self.postgresButton, SIGNAL("toggled()"), self.updateSelection)

    def updateSelection(self):
        """Updates status of radio buttons."""
        self.option = Constants.SQLITE*self.sqliteButton.isChecked() + Constants.POSTGRES*self.postgresButton.isChecked()
        
    def execute(self):
        """Calls exec_() and returns a tuple.
        
        Returns two-member tuple that contains return value of exec_() and driver type.
        
        """
        ok = self.exec_()
        return (ok, self.option)
    
