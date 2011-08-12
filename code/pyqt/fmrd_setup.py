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

from FmrdAdmin import *
from FmrdLib import (Constants, MsgPrompts)
from FmrdLib.CustomDelegates import *
from FmrdLib.CheckTables import *


""" 
Contains classes that implement entry forms to administrative tables of FMRD.

These tables are pre-loaded when the database is initially set up, so they do not 
need to be changed by the user.  With exception of About window, these 
modules would be incorporated only into an administration version of the tool. 

Classes:
CardSetupDlg -- data entry to Disciplinary Card table
ConfedSetupDlg -- data entry to Confederations table
CountrySetupDlg -- data entry to Countries table
FieldPosSetupDlg -- data entry to Field Positions table
FlankPosSetupDlg -- data entry to Flank Positions table
FoulSetupDlg -- data entry to Fouls table
GoalEventSetupDlg -- data entry to Goal Events table
GoalStrikeSetupDlg -- data entry to Goal Strikes table
PenSetupDlg -- data entry to Penalty Outcomes table
PosSetupDlg -- data entry to Positions table
RoundSetupDlg -- data entry to Rounds table
WxCondSetupDlg -- data entry to Weather Conditions table

"""

class CardSetupDlg(QDialog, ui_cardsetup.Ui_CardSetupDlg):
    """Implements card data entry dialog, and accesses and writes to Disciplinary Card table."""

    ID,  DESC = range(2)
    
    def __init__(self, parent=None):
        """Constructor for CardSetupDlg class."""
        super(CardSetupDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_cards")
        self.model.setSort(CardSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.cardID_display, CardSetupDlg.ID)
        self.mapper.addMapping(self.cardtypeEdit, CardSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)        
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.LAST))
        self.connect(self.saveEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NULL))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        if MsgPrompts.SaveDiscardOptionPrompt(self):
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
    
    def saveRecord(self, where):
        """Submits changes to database and navigates through form."""
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        
        if where == Constants.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == Constants.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == Constants.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == Constants.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    def addRecord(self):
        """Adds new record at end of entry list."""                
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                return
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(card_id) FROM tbl_cards"))
        if query.next():
            maxCardID= query.value(0).toInt()[0]
            if not maxCardID:
                card_id = Constants.MinCardID
            else:
                card_id = QString()
                card_id.setNum(maxCardID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to cardID field
        self.cardID_display.setText(card_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)        
        self.cardtypeEdit.setFocus()
    
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the card record is not being referenced in the Offenses table.
        If it is not being referenced in the dependent table, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by dependent table, alert user.
        """
        
        childTableList = ["tbl_offenses"]
        fieldName = "card_id"
        card_id = self.cardID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, card_id):
            if QMessageBox.question(self, QString("Delete Record"), 
                                                QString("Delete current record?"), 
                                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                return
            else:
                row = self.mapper.currentIndex()
                self.model.removeRow(row)
                if not self.model.submitAll():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                    return
                if row + 1 >= self.model.rowCount():
                    row = self.model.rowCount() - 1
                self.mapper.setCurrentIndex(row) 
        else:
                DeletionErrorPrompt(self)


class FoulSetupDlg(QDialog, ui_foulsetup.Ui_FoulSetupDlg):
    """ Implements fouls data entry dialog, and accesses and writes to Fouls table. """

    ID,  DESC = range(2)
 
    def __init__(self, parent=None):
        """Constructor for FoulSetupDlg class."""
        super(FoulSetupDlg, self).__init__(parent)
        self.setupUi(self)
 
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_fouls")
        self.model.setSort(FoulSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.foulID_display, FoulSetupDlg.ID)
        self.mapper.addMapping(self.foulDescEdit, FoulSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.LAST))
        self.connect(self.saveEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NULL))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        if MsgPrompts.SaveDiscardOptionPrompt(self):
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
    
    def saveRecord(self, where):
        """Submits changes to database and navigates through form."""
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())

        if where == Constants.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == Constants.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == Constants.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == Constants.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    def addRecord(self):
        """Adds new record at end of entry list."""                        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                return
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(foul_id) FROM tbl_fouls"))
        if query.next():
            maxFoulID= query.value(0).toInt()[0]
            if not maxFoulID:
                foul_id = Constants.MinFoulID
            else:
                foul_id = QString()
                foul_id.setNum(maxFoulID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to foulID field
        self.foulID_display.setText(foul_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.foulDescEdit.setFocus()
    
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the foul record is not being referenced in any of the following tables:
            - Penalties table
            - Fouls table
        If it is not being referenced in the dependent table, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by dependent table, alert user.
        """
        
        childTableList = ["tbl_penalties", "tbl_fouls"]
        fieldName = "foul_id"
        foul_id = self.foulID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, foul_id):
            if QMessageBox.question(self, QString("Delete Record"), 
                                                QString("Delete current record?"), 
                                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                return
            else:
                row = self.mapper.currentIndex()
                self.model.removeRow(row)
                if not self.model.submitAll():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                    return
                if row + 1 >= self.model.rowCount():
                    row = self.model.rowCount() - 1
                self.mapper.setCurrentIndex(row) 
        else:
                DeletionErrorPrompt(self)
        
        
class PenSetupDlg(QDialog, ui_penoutcomesetup.Ui_PenSetupDlg):
    """ Implements penalty outcome data entry dialog, and accesses and writes to Penalty Outcomes table. """
    
    ID,  DESC = range(2)
 
    def __init__(self, parent=None):
        """Constructor for PenSetupDlg class."""
        super(PenSetupDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_penoutcomes")
        self.model.setSort(PenSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.penoutcomeID_display, PenSetupDlg.ID)
        self.mapper.addMapping(self.penOutcomeEdit, PenSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.LAST))
        self.connect(self.saveEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NULL))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        confirm = MsgPrompts.SaveDiscardOptionPrompt(self)
        if confirm:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
    
    def saveRecord(self, where):
        """Submits changes to database and navigates through form."""
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        if where == Constants.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == Constants.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == Constants.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == Constants.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    def addRecord(self):
        """Adds new record at end of entry list."""                        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                return
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(penoutcome_id) FROM tbl_penoutcomes"))
        if query.next():
            maxPenOutcomeID = query.value(0).toInt()[0]
            if not maxPenOutcomeID:
                outcome_id = Constants.MinPenOutcomeID
            else:
                outcome_id = QString()
                outcome_id.setNum(maxPenOutcomeID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to penOutcomeID field
        self.penoutcomeID_display.setText(outcome_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.penOutcomeEdit.setFocus()
    
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the penalty outcome record is not being referenced in the Penalties table.
        If it is not being referenced in the dependent table, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by dependent table, alert user.
        """
        
        childTableList = ["tbl_penalties"]
        fieldName = "penoutcome_id"
        penoutcome_id = self.penoutcomeID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, penoutcome_id):
            if QMessageBox.question(self, QString("Delete Record"), 
                                                QString("Delete current record?"), 
                                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                return
            else:
                row = self.mapper.currentIndex()
                self.model.removeRow(row)
                if not self.model.submitAll():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                    return
                if row + 1 >= self.model.rowCount():
                    row = self.model.rowCount() - 1
                self.mapper.setCurrentIndex(row) 
        else:
                DeletionErrorPrompt(self)


class GoalEventSetupDlg(QDialog, ui_goaleventsetup.Ui_GoalEventSetupDlg):
    """Implements goal data entry dialog, and accesses and writes to Goal Events table."""
    
    ID,  DESC = range(2)
 
    def __init__(self, parent=None):
        """Constructor for GoalEventSetupDlg class."""
        super(GoalEventSetupDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_goalevents")
        self.model.setSort(GoalEventSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.goaleventID_display, GoalEventSetupDlg.ID)
        self.mapper.addMapping(self.goaleventEdit, GoalEventSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.LAST))
        self.connect(self.saveEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NULL))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        confirm = MsgPrompts.SaveDiscardOptionPrompt(self)
        if confirm:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
    
    def saveRecord(self, where):
        """Submits changes to database and navigates through form."""
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        if where == GoalEventSetupDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == GoalEventSetupDlg.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == GoalEventSetupDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == GoalEventSetupDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    def addRecord(self):        
        """Adds new record at end of entry list."""                        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                return
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(gtetype_id) FROM tbl_goalevents"))
        if query.next():
            maxGoalEventID= query.value(0).toInt()[0]
            if not maxGoalEventID:
                event_id = Constants.MinGoalEventID
            else:
                event_id = QString()
                event_id.setNum(maxGoalEventID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to GoalEventID field
        self.goaleventID_display.setText(event_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.goaleventEdit.setFocus()
    
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the goal event record is not being referenced in the Goals table.
        If it is not being referenced in the dependent table, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by dependent table, alert user.
        """
        
        childTableList = ["tbl_goals"]
        fieldName = "gtetype_id"
        gtetype_id = self.goaleventID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, gtetype_id):
            if QMessageBox.question(self, QString("Delete Record"), 
                                                QString("Delete current record?"), 
                                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                return
            else:
                row = self.mapper.currentIndex()
                self.model.removeRow(row)
                if not self.model.submitAll():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                    return
                if row + 1 >= self.model.rowCount():
                    row = self.model.rowCount() - 1
                self.mapper.setCurrentIndex(row) 
        else:
                DeletionErrorPrompt(self)


class GoalStrikeSetupDlg(QDialog, ui_goalstrikesetup.Ui_GoalStrikeSetupDlg):
    """Implements goal strike data entry dialog, and accesses and writes Goal Strikes table."""
    
    ID,  DESC = range(2)
 
    def __init__(self, parent=None):
        super(GoalStrikeSetupDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_goalstrikes")
        self.model.setSort(GoalStrikeSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.goalstrikeID_display, GoalStrikeSetupDlg.ID)
        self.mapper.addMapping(self.goalstrikeEdit, GoalStrikeSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.LAST))
        self.connect(self.saveEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NULL))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        confirm = MsgPrompts.SaveDiscardOptionPrompt(self)
        if confirm:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
    
    def saveRecord(self, where):
        """Submits changes to database and navigates through form."""
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        if where == Constants.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == Constants.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == Constants.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == Constants.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    def addRecord(self):
        """Adds new record at end of entry list."""                
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                return
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(gtstype_id) FROM tbl_goalstrikes"))
        if query.next():
            maxGoalStrikeID= query.value(0).toInt()[0]
            if not maxGoalStrikeID:
                strike_id = Constants.MinGoalStrikeID
            else:
                strike_id = QString()
                strike_id.setNum(maxGoalStrikeID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to goalStrikeID field
        self.goalstrikeID_display.setText(strike_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.goalstrikeEdit.setFocus()
    
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the goal strike record is not being referenced in the Goals table.
        If it is not being referenced in the dependent table, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by dependent table, alert user.
        """
        
        childTableList = ["tbl_goals"]
        fieldName = "gtstype_id"
        gtstype_id = self.goalstrikeID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, gtstype_id):
            if QMessageBox.question(self, QString("Delete Record"), 
                                                QString("Delete current record?"), 
                                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                return
            else:
                row = self.mapper.currentIndex()
                self.model.removeRow(row)
                if not self.model.submitAll():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                    return
                if row + 1 >= self.model.rowCount():
                    row = self.model.rowCount() - 1
                self.mapper.setCurrentIndex(row) 
        else:
                DeletionErrorPrompt(self)
        

class FieldPosSetupDlg(QDialog, ui_fieldpossetup.Ui_FieldPosSetupDlg):
    """Implements field position data entry dialog, and accesses and writes to Field Names table."""
    
    ID,  DESC = range(2)
 
    def __init__(self, parent=None):
        """Constructor for FieldPosSetupDlg class."""
        super(FieldPosSetupDlg, self).__init__(parent)
        self.setupUi(self)

        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_fieldnames")
        self.model.setSort(FieldPosSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.fieldposID_display, FieldPosSetupDlg.ID)
        self.mapper.addMapping(self.fieldposEdit, FieldPosSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.LAST))
        self.connect(self.saveEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NULL))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        confirm = MsgPrompts.SaveDiscardOptionPrompt(self)
        if confirm:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
    
    def saveRecord(self, where):
        """Submits changes to database and navigates through form."""
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        if where == Constants.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == Constants.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == Constants.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == Constants.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    def addRecord(self):
        """Adds new record at end of entry list."""                
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                return
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(posfield_id) FROM tbl_fieldnames"))
        if query.next():
            maxFieldID= query.value(0).toInt()[0]
            if not maxFieldID:
                field_id = Constants.MinFieldID
            else:
                field_id = QString()
                field_id.setNum(maxFieldID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to fieldposID field
        self.fieldposID_display.setText(field_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.fieldposEdit.setFocus()
    
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the field position record is not being referenced in the Positions table.
        If it is not being referenced in the dependent table, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by dependent table, alert user.
        """
        
        childTableList = ["tbl_positions"]
        fieldName = "posfield_id"
        field_id = self.fieldposID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, field_id):
            if QMessageBox.question(self, QString("Delete Record"), 
                                                QString("Delete current record?"), 
                                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                return
            else:
                row = self.mapper.currentIndex()
                self.model.removeRow(row)
                if not self.model.submitAll():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                    return
                if row + 1 >= self.model.rowCount():
                    row = self.model.rowCount() - 1
                self.mapper.setCurrentIndex(row) 
        else:
                DeletionErrorPrompt(self)
        
        
class FlankPosSetupDlg(QDialog, ui_flankpossetup.Ui_FlankPosSetupDlg):
    """Implements flank position data entry dialog, and accesses and writes to Flank Names table."""
    
    ID,  DESC = range(2)
 
    def __init__(self, parent=None):
        """Constructor of FlankPosSetupDlg class."""
        super(FlankPosSetupDlg, self).__init__(parent)
        self.setupUi(self)

        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_flanknames")
        self.model.setSort(FlankPosSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        localDelegate = GenericDelegate(self)
        localDelegate.insertColumnDelegate(FlankPosSetupDlg.DESC, NullLineEditDelegate())
        self.mapper.setItemDelegate(localDelegate)        
        self.mapper.addMapping(self.flankposID_display, FlankPosSetupDlg.ID)
        self.mapper.addMapping(self.flankposEdit, FlankPosSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.LAST))
        self.connect(self.saveEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NULL))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        confirm = MsgPrompts.SaveDiscardOptionPrompt(self)
        if confirm:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
    
    def saveRecord(self, where):
        """Submits changes to database and navigates through form."""
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        if where == Constants.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == Constants.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == Constants.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == Constants.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    def addRecord(self):
        """Adds new record at end of entry list."""                
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                return
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(posflank_id) FROM tbl_flanknames"))
        if query.next():
            maxFlankID= query.value(0).toInt()[0]
            if not maxFlankID:
                flank_id = Constants.MinFlankID
            else:
                flank_id = QString()
                flank_id.setNum(maxFlankID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to flankposID field
        self.flankposID_display.setText(flank_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.flankposEdit.setFocus()
    
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the flank position record is not being referenced in the Positions table.
        If it is not being referenced in the dependent table, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by dependent table, alert user.
        """
        
        childTableList = ["tbl_positions"]
        fieldName = "posflank_id"
        flank_id = self.flankposID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, flank_id):
            if QMessageBox.question(self, QString("Delete Record"), 
                                                QString("Delete current record?"), 
                                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                return
            else:
                row = self.mapper.currentIndex()
                self.model.removeRow(row)
                if not self.model.submitAll():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                    return
                if row + 1 >= self.model.rowCount():
                    row = self.model.rowCount() - 1
                self.mapper.setCurrentIndex(row) 
        else:
                DeletionErrorPrompt(self)

        
# Implements user interface to Position table, which links to Flank Position and Field Position tables.
class PosSetupDlg(QDialog, ui_positionsetup.Ui_PosSetupDlg):
    """Implements position data entry dialog, which accesses and writes to the Positions table.
    
    The player position is a composite of the flank descriptor and the field position.  Some positions do
    not have a field descriptor (goalkeeper), so the flank descriptor can be left blank.
    
    """
    
    POS_ID,  FIELD_ID,  FLANK_ID = range(3)    

    def __init__(self, parent=None):
        """Constructor to PosSetupDlg class."""
        super(PosSetupDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define model
        # underlying database model
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_positions")
        self.model.setRelation(PosSetupDlg.FIELD_ID, QSqlRelation("tbl_fieldnames", "posfield_id", "posfield_name"))
        self.model.setRelation(PosSetupDlg.FLANK_ID, QSqlRelation("tbl_flanknames", "posflank_id", "posflank_name"))        
        self.model.setSort(PosSetupDlg.POS_ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.setItemDelegate(QSqlRelationalDelegate(self))
        self.mapper.addMapping(self.positionID_display, PosSetupDlg.POS_ID)
        # set up Field Position combobox that links to tbl_fieldnames
        fieldrelationModel = self.model.relationModel(PosSetupDlg.FIELD_ID)
        self.fieldposSelect.setModel(fieldrelationModel)
        self.fieldposSelect.setModelColumn(fieldrelationModel.fieldIndex("posfield_name"))        
        self.mapper.addMapping(self.fieldposSelect, PosSetupDlg.FIELD_ID)        
         # set up Flank Position combobox that links to tbl_flanknames
        flankrelationModel = self.model.relationModel(PosSetupDlg.FLANK_ID)
        self.flankposSelect.setModel(flankrelationModel)
        self.flankposSelect.setModelColumn(flankrelationModel.fieldIndex("posflank_name"))
        self.mapper.addMapping(self.flankposSelect, PosSetupDlg.FLANK_ID)        
        self.mapper.toFirst()         
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.LAST))
        self.connect(self.saveEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NULL))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        
    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        confirm = MsgPrompts.SaveDiscardOptionPrompt(self)
        if confirm:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
        
    def saveRecord(self, where):
        """Submits changes to database and navigates through form."""
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        if where == Constants.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == Constants.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == Constants.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == Constants.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    def addRecord(self):
        """Adds new record at end of entry list."""                
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                return
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(position_id) FROM tbl_positions"))
        if query.next():
            maxPositionID = query.value(0).toInt()[0]
            if not maxPositionID:
                position_id = Constants.MinPositionID
            else:
                position_id = QString()
                position_id.setNum(maxPositionID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to PositionID field
        self.positionID_display.setText(position_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)        
        self.countryEdit.setFocus()
        self.confedSelect.setCurrentIndex(-1)
        
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the position record is not being referenced in any of the following tables:
            - Players table
            - Lineup table
        If it is not being referenced in any of the child tables, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by child tables, alert user.
        """
        
        childTableList = ["tbl_players", "tbl_lineups"]
        fieldName = "position_id"
        position_id = self.positionID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, position_id):
            if QMessageBox.question(self, QString("Delete Record"), 
                                                QString("Delete current record?"), 
                                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                return
            else:
                row = self.mapper.currentIndex()
                self.model.removeRow(row)
                if not self.model.submitAll():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                    return
                if row + 1 >= self.model.rowCount():
                    row = self.model.rowCount() - 1
                self.mapper.setCurrentIndex(row) 
        else:
                DeletionErrorPrompt(self)

class CountrySetupDlg(QDialog, ui_countrysetup.Ui_CountrySetupDlg):
    """Implements country data entry dialog, which accesses and writes to Countries table.
    
    The country is linked with the confederation of which it is a member.
    
    """
    
    ID,  REGION_ID,  NAME = range(3)    
    
    def __init__(self, parent=None):
        """Constructor for CountrySetupDlg class."""
        super(CountrySetupDlg, self).__init__(parent)
        self.setupUi(self)         
        
        # define model
        # underlying database model
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_countries")
        self.model.setRelation(CountrySetupDlg.REGION_ID, QSqlRelation("tbl_confederations", "confed_id", "confed_name"))
        self.model.setSort(CountrySetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.setItemDelegate(QSqlRelationalDelegate(self))
        self.mapper.addMapping(self.countryID_display, CountrySetupDlg.ID)
        self.mapper.addMapping(self.countryEdit, CountrySetupDlg.NAME)        
         # set up combobox that links to foreign table
        relationModel = self.model.relationModel(CountrySetupDlg.REGION_ID)
        self.confedSelect.setModel(relationModel)
        self.confedSelect.setModelColumn(relationModel.fieldIndex("confed_name"))
        self.mapper.addMapping(self.confedSelect, CountrySetupDlg.REGION_ID)        
        self.mapper.toFirst()        
       
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)

        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.LAST))
        self.connect(self.saveEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NULL))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        
    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        confirm = MsgPrompts.SaveDiscardOptionPrompt(self)
        if confirm:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
        
    def saveRecord(self, where):
        """Submits changes to database and navigates through form."""
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        if where == Constants.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == Constants.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == Constants.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == Constants.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    def addRecord(self):
        """Adds new record at end of entry list."""                
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                return
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(country_id) FROM tbl_countries"))
        if query.next():
            maxCountryID= query.value(0).toInt()[0]
            if not maxCountryID:
                country_id = Constants.MinCountryID
            else:
                country_id = QString()
                country_id.setNum(maxCountryID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to countryID field
        self.countryID_display.setText(country_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)        
        self.countryEdit.setFocus()
        self.confedSelect.setCurrentIndex(-1)
        
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the country record is not being referenced in any of the following tables:
            - Players table
            - Referees table
            - Managers table
            - Venues table
        If it is not being referenced in any of the child tables, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by child tables, alert user.
        """
        
        childTableList = ["tbl_players", "tbl_referees",  "tbl_managers",  "tbl_venues"]
        fieldName = "country_id"
        country_id = self.countryID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, country_id):
            if QMessageBox.question(self, QString("Delete Record"), 
                                                QString("Delete current record?"), 
                                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                return
            else:
                row = self.mapper.currentIndex()
                self.model.removeRow(row)
                if not self.model.submitAll():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                    return
                if row + 1 >= self.model.rowCount():
                    row = self.model.rowCount() - 1
                self.mapper.setCurrentIndex(row) 
        else:
                DeletionErrorPrompt(self)
        

class ConfedSetupDlg(QDialog, ui_confederationsetup.Ui_ConfedSetupDlg):
    """Implements confederation data entry dialog, which accesses and writes to Confederations table."""

    ID,  NAME = range(2)
    
    def __init__(self, parent=None):
        """Constructor for ConfedSetupDlg class."""
        super(ConfedSetupDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_confederations")
        self.model.setSort(ConfedSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.confedID_display, ConfedSetupDlg.ID)
        self.mapper.addMapping(self.confederationEdit, ConfedSetupDlg.NAME)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.LAST))
        self.connect(self.saveEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NULL))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        confirm = MsgPrompts.SaveDiscardOptionPrompt(self)
        if confirm:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
        
    def saveRecord(self, where):
        """Submits changes to database and navigates through form."""
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        if where == Constants.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == Constants.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == Constants.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == Constants.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    def addRecord(self):
        """Adds new record at end of entry list."""                
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                return
        
        # move to end of table and insert new record
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(confed_id) FROM tbl_confederations"))
        if query.next():
            maxConfedID= query.value(0).toInt()[0]
            if not maxConfedID:
                confed_id = Constants.MinConfedID
            else:
                confed_id = QString()
                confed_id.setNum(maxConfedID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to confedID field
        self.confedID_display.setText(confed_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.confederationEdit.setFocus()
        
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the confederation record is not being referenced in the Country table.
        If it is not being referenced in the dependent table, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by the dependent table, alert user.
        """
        
        childTableList = ["tbl_countries"]
        fieldName = "confed_id"
        confed_id = self.confedID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, confed_id):
            if QMessageBox.question(self, QString("Delete Record"), 
                                                QString("Delete current record?"), 
                                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                return
            else:
                row = self.mapper.currentIndex()
                self.model.removeRow(row)
                if not self.model.submitAll():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                    return
                if row + 1 >= self.model.rowCount():
                    row = self.model.rowCount() - 1
                self.mapper.setCurrentIndex(row) 
        else:
                DeletionErrorPrompt(self)


class RoundSetupDlg(QDialog, ui_roundsetup.Ui_RoundSetupDlg):
    """Implements matchday data entry dialog, and accesses and writes to Rounds table."""
    
    ID,  DESC = range(2)
    
    def __init__(self, parent=None):
        """Constructor for RoundSetupDlg class."""
        super(RoundSetupDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_rounds")
        self.model.setSort(RoundSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.roundID_display, RoundSetupDlg.ID)
        self.mapper.addMapping(self.rounddescEdit, RoundSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.LAST))
        self.connect(self.saveEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NULL))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
    
    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        confirm = MsgPrompts.SaveDiscardOptionPrompt(self)
        if confirm:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
    
    def saveRecord(self, where):
        """Submits changes to database and navigates through form."""
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        if where == Constants.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == Constants.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == Constants.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == Constants.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    def addRecord(self):
        """Adds new record at end of entry list."""                
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                return
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(round_id) FROM tbl_rounds"))
        if query.next():
            maxRoundID = query.value(0).toInt()[0]
            if not maxRoundID:
                round_id = Constants.MinRoundID
            else:
                round_id = QString()
                round_id.setNum(maxRoundID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to RoundID field
        self.roundID_display.setText(round_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)        
        self.rounddescEdit.setFocus()
    
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the matchday record is not being referenced in the Matches table.
        If it is not being referenced in the dependent table, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by the dependent table, alert user.
        """
        
        childTableList = ["tbl_matches"]
        fieldName = "round_id"
        round_id = self.roundID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, round_id):
            if QMessageBox.question(self, QString("Delete Record"), 
                                                QString("Delete current record?"), 
                                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                return
            else:
                row = self.mapper.currentIndex()
                self.model.removeRow(row)
                if not self.model.submitAll():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                    return
                if row + 1 >= self.model.rowCount():
                    row = self.model.rowCount() - 1
                self.mapper.setCurrentIndex(row) 
        else:
                DeletionErrorPrompt(self)
            
            
class WxCondSetupDlg(QDialog, ui_weathersetup.Ui_WxCondSetupDlg):
    """Implements weather condition data entry dialog, accesses and writes to WeatherConditions table."""
    
    ID,  DESC = range(2)
    
    def __init__(self, parent=None):
        """Constructor for WxCondSetupDlg class."""
        super(WxCondSetupDlg, self).__init__(parent)
        self.setupUi(self)
 
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_weather")
        self.model.setSort(WxCondSetupDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.weatherID_display, WxCondSetupDlg.ID)
        self.mapper.addMapping(self.wxcondEdit, WxCondSetupDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.LAST))
        self.connect(self.saveEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NULL))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        confirm = MsgPrompts.SaveDiscardOptionPrompt(self)
        if confirm:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
    
    def saveRecord(self, where):
        """Submits changes to database and navigates through form."""
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        if where == Constants.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == Constants.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == Constants.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == Constants.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    def addRecord(self):
        """Adds new record at end of entry list."""                
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                return
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(weather_id) FROM tbl_weather"))
        if query.next():
            maxWeatherID = query.value(0).toInt()[0]
            if not maxWeatherID:
                weather_id = Constants.MinWeatherID
            else:
                weather_id = QString()
                weather_id.setNum(maxWeatherID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to WeatherID field
        self.weatherID_display.setText(weather_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.wxcondEdit.setFocus()
    
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the weather condition record is not being referenced in any of the following tables:
            - WeatherKickoff linking table
            - WeatherHalftime linking table
            - WeatherFulltime linking table
        If it is not being referenced in any of the child tables, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by child tables, alert user.
        """
        
        childTableList = ["tbl_weatherkickoff", "tbl_weatherhalftime", "tbl_weatherfulltime"]
        fieldName = "weather_id"
        weather_id = self.weatherID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, weather_id):
            if QMessageBox.question(self, QString("Delete Record"), 
                                                QString("Delete current record?"), 
                                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                return
            else:
                row = self.mapper.currentIndex()
                self.model.removeRow(row)
                if not self.model.submitAll():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                    return
                if row + 1 >= self.model.rowCount():
                    row = self.model.rowCount() - 1
                self.mapper.setCurrentIndex(row) 
        else:
                DeletionErrorPrompt(self)
