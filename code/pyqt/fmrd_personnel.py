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

from FmrdMain import *
from FmrdLib import (Constants,  MsgPrompts)
from FmrdLib.CustomDelegates import *
from FmrdLib.CustomModels import *
from FmrdLib.CheckTables import *
from FmrdLib.MsgPrompts import *


"""Contains classes that implement personnel entry forms to main tables of FMRD.

Classes:
ManagerEntryDlg -- data entry to Managers table
PlayerEntryDlg -- data entry to Players table
RefereeEntryDlg -- data entry to Referees table
LineupEntryDlg -- data entry to Lineups table
"""

class ManagerEntryDlg(QDialog, ui_managerentry.Ui_ManagerEntryDlg):
    """Implements manager data entry dialog, and accesses and writes to Managers table.
    
    This dialog accepts data on the managers who participate in a football competition. In
    particular, data on the manager's nationality and date of birth are tracked.
   """
   
    ID,  CTRY_ID, DOB, FNAME, LNAME, NNAME = range(6)

    def __init__(self, parent=None):
        """Constructor for ManagerEntryDlg class."""
        super(ManagerEntryDlg, self).__init__(parent)
        self.setupUi(self)

        # define local parameters
        CONFED_ID, CONFED_NAME = range(2)
        COUNTRY_ID, COUNTRY_NAME = range(2)

        # define underlying database model
        # because of foreign keys, instantiate QSqlRelationalTableModel and
        # define relations to it
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_managers")
        self.model.setRelation(ManagerEntryDlg.CTRY_ID, QSqlRelation("tbl_countries", "country_id", "cty_name"))                
        self.model.setSort(ManagerEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper to Managers table
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        localDelegate = GenericDelegate(self)
        localDelegate.insertColumnDelegate(ManagerEntryDlg.FNAME, NullLineEditDelegate())
        localDelegate.insertColumnDelegate(ManagerEntryDlg.LNAME, NullLineEditDelegate())        
        localDelegate.insertColumnDelegate(ManagerEntryDlg.NNAME, NullLineEditDelegate())
        localDelegate.insertColumnDelegate(ManagerEntryDlg.CTRY_ID, CountryComboBoxDelegate(self))
        self.mapper.setItemDelegate(localDelegate)
        self.mapper.addMapping(self.mgrID_display, ManagerEntryDlg.ID)

        # relation model for Country combobox
        self.countryModel = self.model.relationModel(ManagerEntryDlg.CTRY_ID)
        self.countryModel.setSort(COUNTRY_ID, Qt.AscendingOrder)
        self.mgrCountrySelect.setModel(self.countryModel)
        self.mgrCountrySelect.setModelColumn(self.countryModel.fieldIndex("cty_name"))
        self.mapper.addMapping(self.mgrCountrySelect, ManagerEntryDlg.CTRY_ID)
        
        # map other widgets on form
        self.mapper.addMapping(self.mgrDOBEdit, ManagerEntryDlg.DOB)
        self.mapper.addMapping(self.mgrFirstNameEdit, ManagerEntryDlg.FNAME)
        self.mapper.addMapping(self.mgrLastNameEdit, ManagerEntryDlg.LNAME)
        self.mapper.addMapping(self.mgrNicknameEdit, ManagerEntryDlg.NNAME)
        self.mapper.toFirst()
 
        # set up Confederation combobox that links to tbl_confederations
        # this result is not saved in database record, only used to filter Country combobox
        self.confedModel = QSqlTableModel(self)
        self.confedModel.setTable("tbl_confederations")
        self.confedModel.setSort(CONFED_ID, Qt.AscendingOrder)
        self.confedModel.select()  
        # define Confederation mapper 
        # establish ties between Confederation database model and data widgets on form
        confedMapper = QDataWidgetMapper(self)
        confedMapper.setModel(self.confedModel)
        self.mgrConfedSelect.setModel(self.confedModel)
        confedMapper.setItemDelegate(MgrConfedComboBoxDelegate(self))
        self.mgrConfedSelect.setModelColumn(self.confedModel.fieldIndex("confed_name"))
        confedMapper.addMapping(self.mgrConfedSelect, CONFED_NAME)
        confedMapper.toFirst()
        
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
        self.connect(self.mapper, SIGNAL("currentIndexChanged(int)"), self.updateConfed)
        self.connect(self.mgrConfedSelect, SIGNAL("activated(int)"), self.filterCountryBox)
     
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
        query.exec_(QString("SELECT MAX(manager_id) FROM tbl_managers"))
        if query.next():
            maxManagerID = query.value(0).toInt()[0]
            if not maxManagerID:
                manager_id = Constants.MinManagerID
            else:
                manager_id= QString()
                manager_id.setNum(maxManagerID+1)  
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to managerID field
        self.mgrID_display.setText(manager_id)
        
        self.firstEntry.setEnabled(True)
        self.prevEntry.setEnabled(True)        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True) 
 
        self.mgrDOBEdit.setText("1901-01-01")        
        self.mgrCountrySelect.setDisabled(True)        
        self.mgrFirstNameEdit.setFocus()
    
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the manager record is not being referenced in any of the following tables:
            - HomeManagers linking table
            - AwayManagers linking table
        If it is not being referenced in any of the child tables, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by child tables, alert user.
        """
        
        childTableList = ["tbl_homemanagers", "tbl_awaymanagers"]
        fieldName = "manager_id"
        manager_id = self.mgrID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, manager_id):
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
        
    def updateConfed(self):
        """Updates current index of Confederation combobox.
        
        Ensures consistency between confederation and selected nation in Country combobox.
        
        """
        # look for current index on Country combobox
        # extract confed_id from underlying model
        currIdx = self.mgrCountrySelect.currentIndex()
        currCountry = self.mgrCountrySelect.currentText()
        id = self.countryModel.record(currIdx).value("confed_id").toString()
        
        # make query on tbl_confederations
        # extract confederation name corresponding to confederation ID
        # there will only be one confederation in query result
        query = QSqlQuery()
        query.exec_(QString("SELECT confed_name FROM tbl_confederations WHERE confed_id = %1").arg(id))
        if query.isActive():
            query.next()
            confedStr = query.value(0).toString()
        else:
            confedStr = "-1"
            
        # search for confederation name in combobox, set index to current index
        self.mgrConfedSelect.setCurrentIndex(self.mgrConfedSelect.findText(confedStr, Qt.MatchExactly))
        
        # update index of Country combobox to that of currCountry
        self.filterCountryBox()
        self.mgrCountrySelect.setCurrentIndex(self.mgrCountrySelect.findText(currCountry, Qt.MatchExactly))
     
    def filterCountryBox(self):
        """Enables and filters Country combobox upon selection in Confederation combobox."""
        # enable Country combobox if disabled
        if ~self.mgrCountrySelect.isEnabled():
            self.mgrCountrySelect.setEnabled(True)
        
        # filter tbl_countries based on confederation selection
        currIdx = self.mgrConfedSelect.currentIndex()
        id = self.confedModel.record(currIdx).value("confed_id").toString()
        self.countryModel.setFilter(QString("confed_id = %1").arg(id))
        self.countryModel.select()
        
        
class RefereeEntryDlg(QDialog, ui_refereeentry.Ui_RefereeEntryDlg):
    """Implements referee data entry dialog, and accesses and writes to Referees table.
    
    This dialog accepts data on the referees who participate in a football competition. In
    particular, data on the referee's nationality and date of birth are tracked.
   """
   
    ID,  CTRY_ID, DOB, FNAME, LNAME = range(5)

    def __init__(self, parent=None):
        """Constructor of RefereeEntryDlg class."""
        super(RefereeEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define local parameters
        CONFED_ID, CONFED_NAME = range(2)
        COUNTRY_ID, COUNTRY_NAME = range(2)
                
        # define underlying database model
        # because of foreign keys, instantiate QSqlRelationalTableModel and
        # define relations to it
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_referees")
        self.model.setRelation(RefereeEntryDlg.CTRY_ID, QSqlRelation("tbl_countries", "country_id", "cty_name"))                
        self.model.setSort(RefereeEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        localDelegate = GenericDelegate(self)
        localDelegate.insertColumnDelegate(RefereeEntryDlg.CTRY_ID, CountryComboBoxDelegate(self))
        localDelegate.insertColumnDelegate(RefereeEntryDlg.FNAME, NullLineEditDelegate())
        localDelegate.insertColumnDelegate(RefereeEntryDlg.LNAME, NullLineEditDelegate())        
        self.mapper.setItemDelegate(localDelegate)        
        self.mapper.addMapping(self.refID_display, RefereeEntryDlg.ID)

        # relation model for Country combobox
        self.countryModel = self.model.relationModel(RefereeEntryDlg.CTRY_ID)
        self.countryModel.setSort(COUNTRY_ID, Qt.AscendingOrder)
        self.refCountrySelect.setModel(self.countryModel)
        self.refCountrySelect.setModelColumn(self.countryModel.fieldIndex("cty_name"))
        self.mapper.addMapping(self.refCountrySelect, RefereeEntryDlg.CTRY_ID)

        # map other widgets on form
        self.mapper.addMapping(self.refDOBEdit, RefereeEntryDlg.DOB)
        self.mapper.addMapping(self.refFirstNameEdit, RefereeEntryDlg.FNAME)
        self.mapper.addMapping(self.refLastNameEdit, RefereeEntryDlg.LNAME)
        self.mapper.toFirst()
        
        # set up Confederation combobox that links to tbl_confederations
        # this result is not saved in database record, only used to filter Country combobox
        self.confedModel = QSqlTableModel(self)
        self.confedModel.setTable("tbl_confederations")
        self.confedModel.setSort(CONFED_ID, Qt.AscendingOrder)
        self.confedModel.select()  
        # define Confederation mapper 
        # establish ties between Confederation database model and data widgets on form
        confedMapper = QDataWidgetMapper(self)
        confedMapper.setModel(self.confedModel)
        self.refConfedSelect.setModel(self.confedModel)
        confedMapper.setItemDelegate(RefConfedComboBoxDelegate(self))         
        self.refConfedSelect.setModelColumn(self.confedModel.fieldIndex("confed_name"))
        confedMapper.addMapping(self.refConfedSelect, CONFED_NAME)
        confedMapper.toFirst()
        
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
        self.connect(self.mapper, SIGNAL("currentIndexChanged(int)"), self.updateConfed)
        self.connect(self.refConfedSelect, SIGNAL("activated(int)"), self.filterCountryBox)
     
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
        query.exec_(QString("SELECT MAX(referee_id) FROM tbl_referees"))
        if query.next():
            maxRefereeID = query.value(0).toInt()[0]
            if not maxRefereeID:
                referee_id = Constants.MinRefereeID
            else:
                referee_id= QString()
                referee_id.setNum(maxRefereeID+1)    
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to refereeID field
        self.refID_display.setText(referee_id)

        self.firstEntry.setEnabled(True)
        self.prevEntry.setEnabled(True)
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)        
        
        self.refDOBEdit.setText("1901-01-01")                
        self.refCountrySelect.setDisabled(True)        
        self.refFirstNameEdit.setFocus()
    
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the referee record is not being referenced in the Lineups table.
        If it is not being referenced in Lineups, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by Lineups, alert user.
        """
        
        childTableList = ["tbl_lineups"]
        fieldName = "referee_id"
        referee_id = self.refID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, referee_id):
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

    def updateConfed(self):
        """Updates current index of Confederation combobox.
        
        Ensures consistency between confederation and selected nation in Country combobox.
        
        """
        # look for current index on Country combobox
        # extract confed_id from underlying model
        currIdx = self.refCountrySelect.currentIndex()
        currCountry = self.refCountrySelect.currentText()
        id = self.countryModel.record(currIdx).value("confed_id").toString()
        
        # make query on tbl_confederations
        # extract confederation name corresponding to confederation ID
        # there will only be one confederation in query result
        query = QSqlQuery()
        query.exec_(QString("SELECT confed_name FROM tbl_confederations WHERE confed_id = %1").arg(id))
        if query.isActive():
            query.next()
            confedStr = query.value(0).toString()
        else:
            confedStr = "-1"
            
        # search for confederation name in combobox, set index to current index
        self.refConfedSelect.setCurrentIndex(self.refConfedSelect.findText(confedStr, Qt.MatchExactly))
        
        # update index of Country combobox to that of currCountry
        self.filterCountryBox()
        self.refCountrySelect.setCurrentIndex(self.refCountrySelect.findText(currCountry, Qt.MatchExactly))
     
    def filterCountryBox(self):
        """Enables and filters Country combobox upon selection in Confederation combobox."""
        # enable Country combobox if disabled
        if ~self.refCountrySelect.isEnabled():
            self.refCountrySelect.setEnabled(True)
        
        # filter tbl_countries based on confederation selection
        currIdx = self.refConfedSelect.currentIndex()
        id = self.confedModel.record(currIdx).value("confed_id").toString()
        self.countryModel.setFilter(QString("confed_id = %1").arg(id))
        self.countryModel.select()
    

class PlayerEntryDlg(QDialog, ui_playerentry.Ui_PlayerEntryDlg):
    """Implements player data entry dialog, and accesses and writes to Players table.
    
    This dialog accepts data on the players who participate in a football competition. In
    particular, data on the player's nationality, date of birth, and default position are tracked.
   """
   
    ID,  CTRY_ID, DOB, FNAME, LNAME, NNAME, POS_ID = range(7)
 
    def __init__(self, parent=None):
        """Constructor of PlayerEntryDlg class."""
        super(PlayerEntryDlg, self).__init__(parent)
        self.setupUi(self)

        # define local parameters
        CONFED_ID, CONFED_NAME = range(2)
        COUNTRY_ID, COUNTRY_NAME = range(2)
        POSITION_ID,  POSITION_NAME = range(2)
        
        # define underlying database model
        # because of foreign keys, instantiate QSqlRelationalTableModel and
        # define relations to it
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_players")
        self.model.setRelation(PlayerEntryDlg.CTRY_ID, QSqlRelation("tbl_countries", "country_id", "cty_name"))   
        self.model.setRelation(PlayerEntryDlg.POS_ID, QSqlRelation("positions_list", "position_id", "position_name"))
        self.model.setSort(PlayerEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)       
        localDelegate = GenericDelegate(self)
        localDelegate.insertColumnDelegate(PlayerEntryDlg.FNAME, NullLineEditDelegate())
        localDelegate.insertColumnDelegate(PlayerEntryDlg.LNAME, NullLineEditDelegate())
        localDelegate.insertColumnDelegate(PlayerEntryDlg.NNAME, NullLineEditDelegate())
        localDelegate.insertColumnDelegate(PlayerEntryDlg.CTRY_ID, CountryComboBoxDelegate(self))
        self.mapper.setItemDelegate(localDelegate)
        self.mapper.addMapping(self.plyrID_display, PlayerEntryDlg.ID)

        # relation model for Country combobox
        self.countryModel = self.model.relationModel(PlayerEntryDlg.CTRY_ID)
        self.countryModel.setSort(COUNTRY_NAME, Qt.AscendingOrder)
        self.plyrCountrySelect.setModel(self.countryModel)
        self.plyrCountrySelect.setModelColumn(self.countryModel.fieldIndex("cty_name"))
        self.mapper.addMapping(self.plyrCountrySelect, PlayerEntryDlg.CTRY_ID)
        
        # relation model for Position combobox
        self.positionModel = self.model.relationModel(PlayerEntryDlg.POS_ID)
        self.positionModel.setSort(POSITION_NAME, Qt.AscendingOrder)
        self.plyrPositionSelect.setModel(self.positionModel)
        self.plyrPositionSelect.setModelColumn(self.positionModel.fieldIndex("position_name"))
        self.mapper.addMapping(self.plyrPositionSelect, PlayerEntryDlg.POS_ID)

        # map other widgets on form
        self.mapper.addMapping(self.plyrDOBEdit, PlayerEntryDlg.DOB)
        self.mapper.addMapping(self.plyrFirstNameEdit, PlayerEntryDlg.FNAME)
        self.mapper.addMapping(self.plyrLastNameEdit, PlayerEntryDlg.LNAME)
        self.mapper.addMapping(self.plyrNicknameEdit, PlayerEntryDlg.NNAME)
        self.mapper.toFirst()
        
        # set up Confederation combobox that links to tbl_confederations
        # this result is not saved in database record, only used to filter Country combobox
        self.confedModel = QSqlTableModel(self)
        self.confedModel.setTable("tbl_confederations")
        self.confedModel.setSort(CONFED_ID, Qt.AscendingOrder)
        self.confedModel.select()  
        # define Confederation mapper 
        # establish ties between Confederation database model and data widgets on form
        confedMapper = QDataWidgetMapper(self)
        confedMapper.setModel(self.confedModel)
        self.plyrConfedSelect.setModel(self.confedModel)
        confedMapper.setItemDelegate(PlyrConfedComboBoxDelegate(self))        
        self.plyrConfedSelect.setModelColumn(self.confedModel.fieldIndex("confed_name"))
        confedMapper.addMapping(self.plyrConfedSelect, CONFED_NAME)
        confedMapper.toFirst()
                
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        if self.model.rowCount() <= 1:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
        
         # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.LAST))
        self.connect(self.saveEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NULL))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        self.connect(self.mapper, SIGNAL("currentIndexChanged(int)"), self.updateConfed)
        self.connect(self.plyrConfedSelect, SIGNAL("currentIndexChanged(int)"), self.filterCountryBox)
     
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
            row -= 1
            if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)   
            if row == 0:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
        elif where == Constants.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row == self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
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
        query.exec_(QString("SELECT MAX(player_id) FROM tbl_players"))
        if query.next():
            maxPlayerID = query.value(0).toInt()[0]
            if not maxPlayerID:
                player_id = Constants.MinPlayerID
            else:
                player_id= QString()
                player_id.setNum(maxPlayerID+1)
    
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to playerID field
        self.plyrID_display.setText(player_id)
        
        self.firstEntry.setEnabled(True)
        self.prevEntry.setEnabled(True)
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)   
        
        self.plyrDOBEdit.setText("1901-01-01")        
        self.plyrCountrySelect.setDisabled(True)        
        self.plyrFirstNameEdit.setFocus()
    
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the player record is not being referenced in the Lineups table.
        If it is not being referenced there, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by Lineups, alert user.
        """
        
        childTableList = ["tbl_lineups"]
        fieldName = "player_id"
        player_id = self.plyrID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, player_id):
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
        
    def updateConfed(self):
        """Updates current index of Confederation combobox.
        
        Ensures consistency between confederation and selected nation in Country combobox.
        
        """
        # look for current index on Country combobox
        # extract confed_id from underlying model
        currIdx = self.plyrCountrySelect.currentIndex()
        currCountry = self.plyrCountrySelect.currentText()
        id = self.countryModel.record(currIdx).value("confed_id").toString()
        
        # make query on tbl_confederations
        # extract confederation name corresponding to confederation ID
        # there will only be one confederation in query result
        query = QSqlQuery()
        query.exec_(QString("SELECT confed_name FROM tbl_confederations WHERE confed_id = %1").arg(id))
        if query.isActive():
            query.next()
            confedStr = query.value(0).toString()
        else:
            confedStr = "-1"
            
        # search for confederation name in combobox, set index to current index
        self.plyrConfedSelect.setCurrentIndex(self.plyrConfedSelect.findText(confedStr, Qt.MatchExactly))
        
        # update index of Country combobox to that of currCountry
        self.filterCountryBox()
        self.plyrCountrySelect.setCurrentIndex(self.plyrCountrySelect.findText(currCountry, Qt.MatchExactly))
     
    def filterCountryBox(self):
        """Enables and filters Country combobox upon selection in Confederation combobox."""
        # enable Country combobox if disabled
        if ~self.plyrCountrySelect.isEnabled():
            self.plyrCountrySelect.setEnabled(True)
            
        # flush filter
        self.countryModel.setFilter(QString())
        self.countryModel.select()
        
        # filter tbl_countries based on confederation selection
        currIdx = self.plyrConfedSelect.currentIndex()
        id = self.confedModel.record(currIdx).value("confed_id").toString()
        self.countryModel.setFilter(QString("confed_id = %1").arg(id))
        self.countryModel.select()
        
        
class LineupEntryDlg(QDialog, ui_lineupentry.Ui_LineupEntryDlg):
    """Implements lineup data entry dialog, and accesses and writes to Lineups table.
    
    This dialog accepts data on the players who participate in a specific football match,
    whether as starting players or substitutes. It is here that the players are connected
    to teams and designated as either starters or captain. The Match Events tables are 
    dependent on the data in the Lineups table to insure integrity between the players 
    and the matches in which they participate.
   """
   
    ID,  MATCH_ID, TEAM_ID, PLYR_ID, POS_ID, ST_FLAG, CAPT_FLAG = range(7)
    
    def __init__(self, match_id, teamName, parent=None):
        """Constructor for LineupEntryDlg class."""
        super(LineupEntryDlg, self).__init__(parent)
        self.setupUi(self)
        self.teamName = teamName
        self.match_id = match_id
        
        # Set values to display fields
        self.matchID_display.setText(self.match_id)
        self.team_display.setText(self.teamName)
                        
        # define underlying database model
        # because of foreign keys, instantiate QSqlRelationalTableModel and
        # define relations to it
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_lineups")
        self.model.setRelation(LineupEntryDlg.TEAM_ID, QSqlRelation("tbl_teams", "team_id", "tm_name"))
        self.model.setRelation(LineupEntryDlg.PLYR_ID, QSqlRelation("players_list", "player_id", "full_name"))
        self.model.setRelation(LineupEntryDlg.POS_ID, QSqlRelation("positions_list", "position_id", "position_name"))
        self.model.setSort(LineupEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
               
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)       
        localDelegate = GenericDelegate(self)
        localDelegate.insertColumnDelegate(LineupEntryDlg.TEAM_ID, LineupTeamDisplayDelegate(self))
        localDelegate.insertColumnDelegate(LineupEntryDlg.PLYR_ID, LineupPlayerComboBoxDelegate(self))
        localDelegate.insertColumnDelegate(LineupEntryDlg.POS_ID, LineupPositionComboBoxDelegate(self))
        localDelegate.insertColumnDelegate(LineupEntryDlg.ST_FLAG, CheckBoxDelegate(self))
        localDelegate.insertColumnDelegate(LineupEntryDlg.CAPT_FLAG, CheckBoxDelegate(self))
        self.mapper.setItemDelegate(localDelegate)
        self.mapper.addMapping(self.lineupID_display, LineupEntryDlg.ID)
        self.mapper.addMapping(self.matchID_display, LineupEntryDlg.MATCH_ID)
        self.mapper.addMapping(self.team_display, LineupEntryDlg.TEAM_ID)
        self.mapper.addMapping(self.startingButton, LineupEntryDlg.ST_FLAG)
        self.mapper.addMapping(self.captButton, LineupEntryDlg.CAPT_FLAG)

        # set up player and position comboboxes
        # - need a custom delegate for player so that 
        #   we don't place same player in match lineup twice
        
        PLYR_SORT_NAME = 2
        POSITION_NAME = 1
        
        self.playerModel = self.model.relationModel(LineupEntryDlg.PLYR_ID)
        self.playerModel.setSort(PLYR_SORT_NAME, Qt.AscendingOrder)
        self.playerSelect.setModel(self.playerModel)
        self.playerSelect.setModelColumn(self.playerModel.fieldIndex("full_name"))
        self.mapper.addMapping(self.playerSelect, LineupEntryDlg.PLYR_ID)

        self.positionModel = self.model.relationModel(LineupEntryDlg.POS_ID)
        self.positionModel.setSort(POSITION_NAME, Qt.AscendingOrder)
        self.positionSelect.setModel(self.positionModel)
        self.positionSelect.setModelColumn(self.positionModel.fieldIndex("position_name"))
        self.mapper.addMapping(self.positionSelect, LineupEntryDlg.POS_ID)
        self.model.setFilter(QString("match_id = %1 AND tm_name = '%2'").arg(self.match_id).arg(teamName))         
        self.mapper.toFirst()
        
        # get status report
        self.statusReport()
        
        # if mapper index is undefined, disable Position combobox
        if self.mapper.currentIndex() == -1:
            self.playerSelect.setDisabled(True)
            self.positionSelect.setDisabled(True)

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
        self.connect(self.closeButton, SIGNAL("clicked()"), lambda: self.accept(self.match_id))
        
        self.connect(self.playerSelect, SIGNAL("currentIndexChanged(int)"), self.enableWidget)
        
    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        confirm = MsgPrompts.SaveDiscardOptionPrompt(self)
        if confirm:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
    
    def addRecord(self):
        """Adds new record at end of entry list and updates status bar."""                
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                return
        
        row = self.model.rowCount()
        
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(lineup_id) FROM tbl_lineups"))
        if query.next():
            maxLineupID = query.value(0).toInt()[0]
            if not maxLineupID:
                lineup_id = Constants.MinLineupID
            else:
                lineup_id= QString()
                lineup_id.setNum(maxLineupID+1)
    
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to lineupID field
        self.lineupID_display.setText(lineup_id)

        # enable/disable navigational buttons
        self.firstEntry.setEnabled(True)
        self.prevEntry.setEnabled(True)
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)        

        # enable player select combobox
        self.playerSelect.setEnabled(True)
        self.positionSelect.setDisabled(True)
        
        # update status bar
        self.statusReport()

    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the lineup record is not being referenced in any of the following tables:
            - Goals table
            - Penalties table
            - Offenses table
            - Substitutions table
            - Switch Positions table
        If it is not being referenced in any of the child tables, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by child tables, alert user.
        """
        
        childTableList = ["tbl_goals",  "tbl_penalties", "tbl_offenses", \
        "tbl_insubstitutions", "tbl_outsubstitutions", "tbl_switchpositions"]
        fieldName = "lineup_id"
        lineup_id = self.lineupID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, lineup_id):
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

    def saveRecord(self, where):
        """Submits changes to database and navigates through form."""
        row = self.mapper.currentIndex()
#        print "Calling saveRecord()"
#        print "Current Row: %d" % row
        # make checks
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
            row -= 1
            if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)   
            if row == 0:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
        elif where == Constants.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row == self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
        elif where == Constants.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
            
        self.mapper.setCurrentIndex(row)
        
        # update status bar
        self.statusReport()        

    def enableWidget(self):
        """Enables Position combobox and calls setDefaultIndex()."""
#        print "Calling enableWidget()"
        widget = self.positionSelect
        if not widget.isEnabled():
            widget.setEnabled(True)
        self.setDefaultIndex(widget)

    def setDefaultIndex(self, editor):
        """Sets initial index of player position using PlayersList view."""
#        print "Calling setDefaultIndex()"
        player = self.playerSelect
        playerName = player.currentText()
#        print "Player Name: %s" % playerName
        index = player.currentIndex()
        positionText = player.model().record(index).value("position_name").toString()
        
#        print "Default Position Name: %s" % positionText

        # look for position name and set index
        editor.setCurrentIndex(editor.findText(positionText, Qt.MatchExactly))
        
    def checkPersonnelRecords(self, match_id, team_id):
        """Checks number of personnel records in Lineup table for specific match and team.
        
        Required number of personnel records:
            (1) Exactly 11 starting players
            (2) Exactly 1 starting goalkeeper
            (3) Exactly 1 starting captain
        There also has to be at least one substitute in order to open the Substitutes dialog.
        
        """
        reqStarters = (CountStarters(match_id, team_id) == Constants.MAX_TEAM_STARTERS)
        reqCaptain = (CountCaptains(match_id, team_id) == Constants.MAX_TEAM_STARTING_CAPTAINS)
        reqGoalkeeper = (CountGoalkeepers(match_id, team_id) == Constants.MAX_TEAM_STARTING_GOALKEEPERS)
        
        return reqStarters & reqCaptain & reqGoalkeeper

    def statusReport(self):
        """Updates status fields at bottom of Lineups data entry dialog.
        
        Calls CountStarters(), CountSubstitutes(), CountCaptains() and CountGoalkeepers() 
        and reports results in status fields. Required number of personnel records:
            (1) Exactly 11 starting players
            (2) Exactly 1 starting goalkeeper
            (3) Exactly 1 starting captain
        Calls ColorCode() to set background color of fields:
            Red -- At least one of the requirements are not met
            Green -- All three requirements have been met
            
        """
        text = QString()
        
        match_id = self.match_id
        
        # get team_id by querying tbl_teams with team name
        team_id = "-1"
        query = QSqlQuery()
        query.prepare("SELECT team_id FROM tbl_teams WHERE tm_name = ?")
        query.addBindValue(QVariant(self.teamName))
        query.exec_()
        if query.next():
            team_id = query.value(0).toString()
            
        #   - Number of starters
        numStarters = CountStarters(match_id, team_id)
        self.NumStarter_display.setText(text.setNum(numStarters))
        self.colorCode(self.NumStarter_display, Constants.MAX_TEAM_STARTERS)
        
        #   - Number of subs
        numSubs = CountSubstitutes(match_id, team_id)
        self.NumSubs_display.setText(text.setNum(numSubs))
        
        #   - Starting Captain
        numCaptains = CountCaptains(match_id, team_id)
        self.NumCapt_display.setText(text.setNum(numCaptains))
        self.colorCode(self.NumCapt_display, Constants.MAX_TEAM_STARTING_CAPTAINS)
        
        #   - Starting Goalkeeper
        numGoalkeepers = CountGoalkeepers(match_id, team_id)
        self.NumGK_display.setText(text.setNum(numGoalkeepers))
        self.colorCode(self.NumGK_display, Constants.MAX_TEAM_STARTING_GOALKEEPERS)
        
    def colorCode(self, editor, threshold):
        """Assigns text and background colors in editor widget based on editor text.
        
        Arguments:
            editor -- editable widget
            threshold -- required quantity 
            
        """
        
        red = QColor(255, 0, 0)
        green = QColor(0, 255, 0)
        black = QColor(255, 255, 255)
        white = QColor(0, 0, 0)
        
        palette = editor.palette()
        number = editor.text().toInt()
        if number[0] == threshold:
            palette.setColor(QPalette.Active, QPalette.Text, black)
            palette.setColor(QPalette.Active, QPalette.Base, green)
        else:
            palette.setColor(QPalette.Active, QPalette.Text, white)
            palette.setColor(QPalette.Active, QPalette.Base, red)
            
        editor.setPalette(palette)

