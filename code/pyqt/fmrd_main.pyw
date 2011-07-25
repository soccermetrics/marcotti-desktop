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

from FmrdLib import Constants

from fmrd_login import *
from fmrd_switchboard import *
from fmrd_user_switchboard import * 

"""
This module is the entry point for the data entry tools.  

Performs login verification and opens either user or admin switchboards.
"""

# Function: main
#
    
def main():
    """ Conducts database authentication and executes GUI loop if successful."""
        
    # create app and login objects
    app = QApplication(sys.argv)
    login = dbLoginDlg() 
        
    # open login window with wrapper function so that tuple is returned
    # status = (QDialog.DialogCode, ButtonState)
    status = login.execute()
        
    # if login is successful (QDialog.DialogCode == QDialog.Accepted)
    #    open switchboard based on return value of ButtonState
    # if login unsuccessful or aborted (QDialog.DialogCode == QDialog.Rejected)
    #    exit application
    if status[0] == QDialog.Accepted:
        if status[1] == Constants.USER:
            userwindow = UserMainSwitchboard()
            userwindow.show()
        elif status[1] == Constants.ADMIN:
            adminwindow = MainSwitchboard()
            adminwindow.show()
        sys.exit(app.exec_())


# ----------------------------------------------------------    
# Call main() to run FMRD switchboard    
main()
