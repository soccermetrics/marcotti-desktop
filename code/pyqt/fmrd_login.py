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

from FmrdMain import ui_fmrdlogin

"""
Contains implementation of login dialog for access to FMRD.

Only class: dbLoginDlg
"""


class dbLoginDlg(QDialog, ui_fmrdlogin.Ui_dbLoginDlg):
    """Implements login dialog for access to database application.
    
    Inherits Ui_dbLoginDlg (ui_fmrdlogin)
    """
    
    USER = 1
    ADMIN = 2
    MAXLOGINS = 3
    
    def __init__(self):
        """ Constructor for dbLoginDlg class."""
        super(dbLoginDlg, self).__init__()
        self.setupUi(self)

        self.attempts = 0

        self.option = dbLoginDlg.USER*self.userButton.isChecked() + dbLoginDlg.ADMIN*self.adminButton.isChecked()
        
        # Define signals and slots
        self.connect(self.dbNameEdit, SIGNAL("textChanged()"), lambda: self.enableWidget(self.loginEdit))
        self.connect(self.loginEdit, SIGNAL("textChanged()"), lambda: self.enableWidget(self.passwordEdit))

    def authenticate(self):
        """ Performs database authentication.  
        
        Records value corresponding to switchboard type selection.
        If authentication is successful, hides login dialog and returns.
        If authentication is not successful, alerts user and clears entry fields.
        If three consecutive failed logins have been made, returns Rejected to caller function.
        
        """
        # get authentication data
        dbName = self.dbNameEdit.text()
        login = self.loginEdit.text()
        password = self.passwordEdit.text()

        self.option = dbLoginDlg.USER*self.userButton.isChecked() + dbLoginDlg.ADMIN*self.adminButton.isChecked()
        
        # attempt to open connection to database
        if self.attempts == 0:
            db = QSqlDatabase.addDatabase("QPSQL") 
        else:
            db = QSqlDatabase.database("QPSQL", False)
        db.setDatabaseName(dbName)
        db.setUserName(login)
        db.setPassword(password)
        
        if not db.open():
            # Alert user of incorrect userid/password combo
            QMessageBox.warning(None,
                "Login Incorrect",
                "The user id and password you entered are incorrect.", 
                QMessageBox.Close)
            self.attempts += 1
            
            # Clear LineEdit fields
            self.dbNameEdit.setText(QString())
            self.loginEdit.setText(QString())
            self.passwordEdit.setText(QString())
            
            # Remove database connection
            # This is done so that DB driver doesn't squawk about duplicate connections
            db.removeDatabase("QPSQL")
            
            # Alert user and send rejection to exec_() if it's 3rd consecutive fail
            if self.attempts == dbLoginDlg.MAXLOGINS:
                QMessageBox.critical(None,
                    "Maximum Login Attempts Exceeded",
                    "You have exceeded the maximum number of login attempts. Press Close to exit.", 
                    QMessageBox.Close)
                self.reject()
        else:
            self.accept()

    def enableWidget(self, widget):
        """Enables widget passed as a parameter if not already enabled."""
        if not widget.isEnabled():
            widget.setEnabled(True)

    def execute(self):
        """Calls exec_() and returns a tuple.
        
        Returns two-member tuple that contains return value of exec_() and switchboard type.
        
        """
        ok = self.exec_()
        return (ok, self.option)
