#!/usr/bin/env python
#
#    Football Match Result Database (FMRD)
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
from FmrdLib import (Constants, MsgPrompts)
from FmrdLib.CustomDelegates import *

"""Contains classes that implement match overview entry forms to main tables of FMRD.

Classes:
CompEntryDlg -- data entry to Competitions table
TeamEntryDlg -- data entry to Teams table
VenueEntryDlg -- data entry to Venues table

"""

class CompEntryDlg(QDialog, ui_competitionentry.Ui_CompEntryDlg):
    """Implements competition data entry dialog, and accesses and writes to Competitions table.
    
    This dialog accepts data on the name of the football competition.
    
    """
    
    ID,  DESC = range(2)
    
    def __init__(self, parent=None):
        """Constructor for CompEntryDlg class."""
        super(CompEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_competitions")
        self.model.setSort(CompEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.compID_display, CompEntryDlg.ID)
        self.mapper.addMapping(self.competitionEdit, CompEntryDlg.DESC)
        self.mapper.toFirst()
        
        # disable all fields if no records in database table
        if not self.model.rowCount():
            self.compID_display.setDisabled(True)
            self.competitionEdit.setDisabled(True)
            # disable save and delete buttons
            self.saveEntry.setDisabled(True)
            self.deleteEntry.setDisabled(True)
            
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True) 
        
        # disable Next and Last Entry buttons if less than two records
        if self.model.rowCount() < 2:
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
        
    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if not CheckDuplicateRecords("comp_name", self.model.tableName(), self.competitionEdit.text()):        
                if MsgPrompts.SaveDiscardOptionPrompt(self):
                    if not self.mapper.submit():
                        MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
            else:
                MsgPrompts.DuplicateRecordErrorPrompt(self, self.model.tableName(), self.competitionEdit.text())
        QDialog.accept(self)
    
    def saveRecord(self, where):
        """Submits changes to database and navigates through form."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if not CheckDuplicateRecords("comp_name", self.model.tableName(), self.competitionEdit.text()):        
                if MsgPrompts.SaveDiscardOptionPrompt(self):
                    if not self.mapper.submit():
                        MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
            else:
                MsgPrompts.DuplicateRecordErrorPrompt(self, self.model.tableName(), self.competitionEdit.text())
                self.mapper.revert()
                return
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
        
        # enable Delete button if at least one record
        if self.model.rowCount():
            self.deleteEntry.setEnabled(True)
        
    def addRecord(self):
        """Adds new record at end of entry list, and sets focus on Competition Name editable field."""
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if self.isDirty(row):
                if not CheckDuplicateRecords("comp_name", self.model.tableName(), self.competitionEdit.text()):        
                    if MsgPrompts.SaveDiscardOptionPrompt(self):
                        if not self.mapper.submit():
                            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                else:
                    MsgPrompts.DuplicateRecordErrorPrompt(self, self.model.tableName(), self.competitionEdit.text())
                    self.mapper.revert()
                    return
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(competition_id) FROM tbl_competitions"))
        if query.next():
            maxCompetitionID= query.value(0).toInt()[0]
            if not maxCompetitionID:
                competition_id = Constants.MinCompetitionID
            else:
                competition_id= QString()
                competition_id.setNum(maxCompetitionID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to competitionID field
        self.compID_display.setText(competition_id)
        
        # disable next/last navigation buttons
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        # enable first/previous navigation buttons
        if self.model.rowCount() > 1:
            self.prevEntry.setEnabled(True)
            self.firstEntry.setEnabled(True)
            # enable Delete button if at least one record
            self.deleteEntry.setEnabled(True)
        
        # enable Save button
        if not self.saveEntry.isEnabled():
            self.saveEntry.setEnabled(True)
        
        # enable form widgets
        self.compID_display.setEnabled(True)
        self.competitionEdit.setEnabled(True)
        # initialize form widgets
        self.competitionEdit.setFocus()
    
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the competition record is not being referenced in the Matches table.
        If it is not being referenced in the dependent tables, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by child tables, alert user.
        """
        
        childTableList = ["tbl_matches"]
        fieldName = "competition_id"
        competition_id = self.compID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, competition_id):
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
                # disable Delete button if no records in database
                if not self.model.rowCount():
                    self.deleteEntry.setDisabled(True)
        else:
                DeletionErrorPrompt(self)
                
    def isDirty(self, row):
        """Compares current state of data entry form to current record in database, and returns a boolean.
        
        Arguments:
            row: current record in mapper and model
        
        Returns:
            TRUE: there are changes between data entry form and current record in database,
                      or new record in database
            FALSE: no changes between data entry form and current record in database
        """
        if row == self.model.rowCount():
            return True
        else:
            index = self.model.index(row, CompEntryDlg.DESC)        
            if self.competitionEdit.text() != self.model.data(index).toString():
                return True
            else:
                return False                
                
                
class TeamEntryDlg(QDialog, ui_teamentry.Ui_TeamEntryDlg):
    """Implements Teams data entry dialog, and accesses and writes to Teams table.
    
    This dialog accepts data on the names of the teams participating in the football competition.
    
    """
    
    ID,  CTRY_ID, NAME = range(3)
    
    def __init__(self, parent=None):
        """Constructor for TeamEntryDlg class."""
        super(TeamEntryDlg, self).__init__(parent)
        self.setupUi(self)

        # define local parameters
        CONFED_ID, CONFED_NAME = range(2)
        COUNTRY_ID, COUNTRY_NAME = range(2)

        # define model
        # underlying database model
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_teams")
        self.model.setRelation(TeamEntryDlg.CTRY_ID, QSqlRelation("tbl_countries", "country_id", "cty_name"))           
        self.model.setSort(TeamEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        localDelegate = GenericDelegate(self)
        localDelegate.insertColumnDelegate(TeamEntryDlg.CTRY_ID, CountryComboBoxDelegate(self))
        self.mapper.setItemDelegate(localDelegate)        
        self.mapper.addMapping(self.teamID_display, TeamEntryDlg.ID)
        
        # relation model for Country combobox
        self.countryModel = self.model.relationModel(TeamEntryDlg.CTRY_ID)
        self.countryModel.setSort(COUNTRY_ID, Qt.AscendingOrder)
        self.teamCountrySelect.setModel(self.countryModel)
        self.teamCountrySelect.setModelColumn(self.countryModel.fieldIndex("cty_name"))    
        self.teamCountrySelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.teamCountrySelect, TeamEntryDlg.CTRY_ID)
        
        # map other widgets on form        
        self.mapper.addMapping(self.teamNameEdit, TeamEntryDlg.NAME)
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
        self.teamConfedSelect.setModel(self.confedModel)
        confedMapper.setItemDelegate(TeamConfedComboBoxDelegate(self))
        self.teamConfedSelect.setModelColumn(self.confedModel.fieldIndex("confed_name"))
        self.teamConfedSelect.setCurrentIndex(-1)
        confedMapper.addMapping(self.teamConfedSelect, CONFED_NAME)
        confedMapper.toFirst()       
        
        # disable all fields if no records in database table
        if not self.model.rowCount():
            self.teamID_display.setDisabled(True)
            self.teamConfedSelect.setDisabled(True)
            self.teamCountrySelect.setDisabled(True)
            # disable save and delete entry buttons
            self.saveEntry.setDisabled(True)
            self.deleteEntry.setDisabled(True)
            
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)

        # disable Next and Last Entry buttons if less than two records
        if self.model.rowCount() < 2:
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
        self.connect(self.teamConfedSelect, SIGNAL("activated(int)"), self.filterCountryBox)        
        
    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if MsgPrompts.SaveDiscardOptionPrompt(self):
                if not self.mapper.submit():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
    
    def saveRecord(self, where):
        """Submits changes to database and navigates through form."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if MsgPrompts.SaveDiscardOptionPrompt(self):
                if not self.mapper.submit():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
            else:
                self.mapper.revert()
                return
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
        
        # enable Delete button if at least one record
        if self.model.rowCount():
            self.deleteEntry.setEnabled(True)        
        
    def addRecord(self):
        """Adds new record at end of entry list, and sets focus on Team Name editable field."""
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if self.isDirty(row):
                if MsgPrompts.SaveDiscardOptionPrompt(self):
                    if not self.mapper.submit():
                        MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                else:
                    self.mapper.revert()
                    return
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(team_id) FROM tbl_teams"))
        if query.next():
            maxTeamID= query.value(0).toInt()[0]
            if not maxTeamID:
                team_id = Constants.MinTeamID
            else:
                team_id= QString()
                team_id.setNum(maxTeamID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to teamID field
        self.teamID_display.setText(team_id)
        
        # disable next/last navigation buttons
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        # enable first/previous navigation buttons
        if self.model.rowCount() > 1:
            self.prevEntry.setEnabled(True)
            self.firstEntry.setEnabled(True)
            # enable Delete button if at least one record
            self.deleteEntry.setEnabled(True)

        # enable Save button
        if not self.saveEntry.isEnabled():
            self.saveEntry.setEnabled(True)
        
        # enable form widgets
        self.teamID_display.setEnabled(True)
        self.teamNameEdit.setEnabled(True)
        self.teamConfedSelect.setEnabled(True)
        self.teamCountrySelect.setEnabled(True)
        
        # initialize form widgets
        self.teamConfedSelect.setCurrentIndex(-1)
        self.teamCountrySelect.setCurrentIndex(-1)
        self.teamNameEdit.setFocus()
    
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the record in Teams table is not being referenced in any of the following tables:
            - HomeTeams linking table
            - AwayTeams linking table
            - Venues table
            - Lineups table
            - Goals table
        If it is not being referenced in any of the child tables, ask for user confirmation and delete 
        record upon positive confirmation.  If it is being referenced by child tables, alert user.
        """
        
        childTableList = ["tbl_hometeams", "tbl_awayteams", "tbl_venues", "tbl_lineups", "tbl_goals"]
        fieldName = "team_id"
        team_id = self.teamID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, team_id):
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
                # disable Delete button if no records in database
                if not self.model.rowCount():
                    self.deleteEntry.setDisabled(True)
        else:
                DeletionErrorPrompt(self)
                
    def isDirty(self, row):
        """Compares current state of data entry form to current record in database, and returns a boolean.
        
        Arguments:
            row: current record in mapper and model
        
        Returns:
            TRUE: there are changes between data entry form and current record in database,
                      or new record in database
            FALSE: no changes between data entry form and current record in database
        """
        index = self.model.index(row, TeamEntryDlg.NAME)        
        if self.teamNameEdit.text() != self.model.data(index).toString():
            return True
            
        index = self.model.index(row, TeamEntryDlg.CTRY_ID)        
        if self.teamCountrySelect.currentText() != self.model.data(index).toString():
            return True
            
        return False
                
                
    def updateConfed(self):
        """Updates current index of Confederation combobox.
        
        Ensures consistency between the current nation and its confederation.
        """
        # look for current index on Country combobox
        # extract confed_id from underlying model
        currIdx = self.teamCountrySelect.currentIndex()
        currCountry = self.teamCountrySelect.currentText()
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
        self.teamConfedSelect.setCurrentIndex(self.teamConfedSelect.findText(confedStr, Qt.MatchExactly))
        
        # update index of Country combobox to that of currCountry
        self.filterCountryBox()
        self.teamCountrySelect.setCurrentIndex(self.teamCountrySelect.findText(currCountry, Qt.MatchExactly))
     
    def filterCountryBox(self):
        """Enables Country combobox and filters contents on Country combobox upon selection of Confederation."""
        # enable Country combobox if disabled
        if ~self.teamCountrySelect.isEnabled():
            self.teamCountrySelect.setEnabled(True)
        
        # filter tbl_countries based on confederation selection
        currIdx = self.teamConfedSelect.currentIndex()
        id = self.confedModel.record(currIdx).value("confed_id").toString()
        self.countryModel.setFilter(QString("confed_id = %1").arg(id))
        self.countryModel.select()
                
                
class VenueEntryDlg(QDialog, ui_venueentry.Ui_VenueEntryDlg):
    """Implements Venues data entry dialog, and accesses and writes to Venues table.
    
    This dialog accepts data on the match venues used in the football competition.
    
    """
    
    ID,  TEAM_ID,  CTRY_ID, TZ_ID,  CITY, NAME, ALT, LAT, LONG = range(9)

    def __init__(self, parent=None):
        super(VenueEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define local parameters
        CONFED_ID, CONFED_NAME = range(2)
        COUNTRY_NAME = HOST_NAME = 1
        TIMEZONE_OFFSET = 3

        # define validators for geographic fields
        self.venueLatitudeEdit.setValidator(QDoubleValidator(-90.000000, 90.000000, 6, self.layoutWidget))
        self.venueLongitudeEdit.setValidator(QDoubleValidator(-180.000000, 180.000000, 6, self.layoutWidget))
        self.venueAltEdit.setValidator(QIntValidator(0, 5000, self.layoutWidget))
        
        # define underlying database model
        # because of foreign keys, instantiate QSqlRelationalTableModel and
        # define relations to it
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_venues")
        self.model.setRelation(VenueEntryDlg.TEAM_ID, QSqlRelation("tbl_teams", "team_id", "tm_name"))
        self.model.setRelation(VenueEntryDlg.CTRY_ID, QSqlRelation("tbl_countries", "country_id", "cty_name"))
        self.model.setRelation(VenueEntryDlg.TZ_ID, QSqlRelation("tbl_timezones", "timezone_id", "tz_name"))
        self.model.setSort(VenueEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        localDelegate = GenericDelegate(self)
        localDelegate.insertColumnDelegate(VenueEntryDlg.CTRY_ID, CountryComboBoxDelegate(self))
        localDelegate.insertColumnDelegate(VenueEntryDlg.LAT, GeoCoordinateDelegate(self))
        localDelegate.insertColumnDelegate(VenueEntryDlg.LONG, GeoCoordinateDelegate(self))
        self.mapper.setItemDelegate(localDelegate)
        self.mapper.addMapping(self.venueID_display, VenueEntryDlg.ID)
        
        # relation model for Home Team combobox
        self.teamModel = self.model.relationModel(VenueEntryDlg.TEAM_ID)
        self.teamModel.setSort(HOST_NAME, Qt.AscendingOrder)
        self.venueTeamSelect.setModel(self.teamModel)
        self.venueTeamSelect.setModelColumn(self.teamModel.fieldIndex("tm_name"))
        self.venueTeamSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.venueTeamSelect, VenueEntryDlg.TEAM_ID)        
        
        # relation model for Country combobox
        self.countryModel = self.model.relationModel(VenueEntryDlg.CTRY_ID)
        self.countryModel.setSort(COUNTRY_NAME, Qt.AscendingOrder)
        self.venueCountrySelect.setModel(self.countryModel)
        self.venueCountrySelect.setModelColumn(self.countryModel.fieldIndex("cty_name"))
        self.venueCountrySelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.venueCountrySelect, VenueEntryDlg.CTRY_ID)
        
        # relation model for Time Zone combobox
        self.timezoneModel = self.model.relationModel(VenueEntryDlg.TZ_ID)
        self.timezoneModel.setSort(TIMEZONE_OFFSET, Qt.AscendingOrder)
        self.venueTimezoneSelect.setModel(self.timezoneModel)
        self.venueTimezoneSelect.setModelColumn(self.timezoneModel.fieldIndex("tz_name"))
        self.venueTimezoneSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.venueTimezoneSelect, VenueEntryDlg.TZ_ID)
        
        # map other widgets on form
        self.mapper.addMapping(self.venueCityEdit, VenueEntryDlg.CITY)
        self.mapper.addMapping(self.venueNameEdit, VenueEntryDlg.NAME)
        self.mapper.addMapping(self.venueAltEdit, VenueEntryDlg.ALT)
        self.mapper.addMapping(self.venueLatitudeEdit, VenueEntryDlg.LAT)
        self.mapper.addMapping(self.venueLongitudeEdit, VenueEntryDlg.LONG)
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
        self.venueConfedSelect.setModel(self.confedModel)
        confedMapper.setItemDelegate(VenConfedComboBoxDelegate(self))
        self.venueConfedSelect.setModelColumn(self.confedModel.fieldIndex("confed_name"))
        self.venueConfedSelect.setCurrentIndex(-1)
        confedMapper.addMapping(self.venueConfedSelect, CONFED_NAME)
        confedMapper.toFirst()       
       
        # disable all fields if no records in database table
        if not self.model.rowCount():
            self.venueID_display.setDisabled(True)
            self.venueNameEdit.setDisabled(True)
            self.venueCityEdit.setDisabled(True)
            self.venueConfedSelect.setDisabled(True)
            self.venueCountrySelect.setDisabled(True)
            self.venueTeamSelect.setDisabled(True)
            self.venueTimezoneSelect.setDisabled(True)
            self.venueAltEdit.setDisabled(True)
            self.venueLatitudeEdit.setDisabled(True)
            self.venueLongitudeEdit.setDisabled(True)
            self.venueHistoryButton.setDisabled(True)
            # disable save and delete entry buttons
            self.saveEntry.setDisabled(True)
            self.deleteEntry.setDisabled(True)
       
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)       

        # disable Next and Last Entry buttons if less than two records
        if self.model.rowCount() < 2:
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
        self.connect(self.venueConfedSelect, SIGNAL("activated(int)"), self.filterCountriesAndTimeZones)
        self.connect(self.venueHistoryButton, SIGNAL("clicked()"), lambda: self.openVenueHistory(self.venueID_display.text()))
     
    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if MsgPrompts.SaveDiscardOptionPrompt(self):
                if not self.mapper.submit():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
    
    def saveRecord(self, where):
        """Submits changes to database and navigates through form."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if MsgPrompts.SaveDiscardOptionPrompt(self):
                if not self.mapper.submit():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
            else:
                self.mapper.revert()
                return
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
        
        # enable Delete button if at least one record
        if self.model.rowCount():
            self.deleteEntry.setEnabled(True)        
        
    def addRecord(self):
        """Adds new record at end of entry list, and sets focus on Venue Name editable field while disabling all others."""
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if self.isDirty(row):
                if MsgPrompts.SaveDiscardOptionPrompt(self):
                    if not self.mapper.submit():
                        MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                else:
                    self.mapper.revert()
                    return
        
        row = self.model.rowCount()        
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(venue_id) FROM tbl_venues"))
        if query.next():
            maxVenueID= query.value(0).toInt()[0]
            if not maxVenueID:
                venue_id = Constants.MinVenueID
            else:
                venue_id= QString()
                venue_id.setNum(maxVenueID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to venueID field
        self.venueID_display.setText(venue_id)
        
        # disable next/last navigation buttons
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        # enable first/previous navigation buttons
        if self.model.rowCount() > 1:
            self.prevEntry.setEnabled(True)
            self.firstEntry.setEnabled(True)
            # enable Delete button if at least one record
            self.deleteEntry.setEnabled(True)
        
        # enable Save button
        if not self.saveEntry.isEnabled():
            self.saveEntry.setEnabled(True)

        # enable data widgets
        self.venueID_display.setEnabled(True)
        self.venueNameEdit.setEnabled(True)
        self.venueCityEdit.setEnabled(True)
        self.venueConfedSelect.setEnabled(True)
        self.venueTeamSelect.setEnabled(True)
        self.venueAltEdit.setEnabled(True)
        self.venueLatitudeEdit.setEnabled(True)
        self.venueLongitudeEdit.setEnabled(True)
        self.venueHistoryButton.setEnabled(True)
        
        # initialization of data widgets
        self.venueTeamSelect.setCurrentIndex(-1)
        self.venueTimezoneSelect.setCurrentIndex(-1)
        self.venueConfedSelect.setCurrentIndex(-1)
        self.venueAltEdit.setText("0")
        self.venueLatitudeEdit.setText("0.000000")
        self.venueLongitudeEdit.setText("0.000000")
        
        self.venueCountrySelect.setDisabled(True)        
        self.venueTimezoneSelect.setDisabled(True)
        self.venueNameEdit.setFocus()
    
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the venue record is not being referenced in the Matches table.
        If it is not being referenced in the dependent table, ask for user confirmation, and 
        upon positive response delete records in the following order:
            (1) Venue History table
            (2) Venues table
        If it is being referenced by dependent table, alert user.
        """
        
        childTableList = ["tbl_matches"]
        fieldName = "venue_id"
        venue_id = self.venueID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, venue_id):
            if QMessageBox.question(self, QString("Delete Record"), 
                                                QString("Delete current record?"), 
                                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                return
            else:
                # delete corresponding records in VenueHistory table
                self.deleteVenueHistories(venue_id)
                # delete records in Venues table
                row = self.mapper.currentIndex()
                self.model.removeRow(row)
                if not self.model.submitAll():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                    return
                if row + 1 >= self.model.rowCount():
                    row = self.model.rowCount() - 1
                self.mapper.setCurrentIndex(row) 
                # disable Delete button if no records in database
                if not self.model.rowCount():
                    self.deleteEntry.setDisabled(True)                
        else:
                DeletionErrorPrompt(self)
                
    def isDirty(self, row):
        """Compares current state of data entry form to current record in database, and returns a boolean.
        
        Arguments:
            row: current record in mapper and model
        
        Returns:
            TRUE: there are changes between data entry form and current record in database,
                      or new record in database
            FALSE: no changes between data entry form and current record in database
        """
        
        # line edit fields
        editorList = (self.venueNameEdit, self.venueAltEdit, self.venueLatitudeEdit, self.venueLongitudeEdit)
        columnList = (VenueEntryDlg.NAME, VenueEntryDlg.ALT, VenueEntryDlg.LAT, VenueEntryDlg.LONG)
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.text() != self.model.data(index).toString():
                return True
                
        # combobox fields
        editorList = (self.venueTeamSelect, self.venueTimezoneSelect, self.venueCountrySelect)
        columnList = (VenueEntryDlg.TEAM_ID, VenueEntryDlg.TZ_ID, VenueEntryDlg.CTRY_ID)
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.currentText() != self.model.data(index).toString():
                return True
        
        return False
                
    def deleteVenueHistories(self, venue_id):
        """Deletes venue history records that reference a specific match venue."""
        
        deletionQuery = QSqlQuery()
        deletionQuery.prepare("DELETE FROM tbl_venuehistory WHERE venue_id = ?")
        deletionQuery.addBindValue(QVariant(venue_id))
        deletionQuery.exec_()

    def updateConfed(self):
        """Updates current index of Confederation combobox.
        
        Ensures consistency between the current nation, the current time zone, 
        and the confederation to which both belong.
        """
        # look for current index on Country combobox
        # extract confed_id from underlying model
        currIdx = self.venueCountrySelect.currentIndex()
        currCountry = self.venueCountrySelect.currentText()
        id = self.countryModel.record(currIdx).value("confed_id").toString()
        
        # get current text on Time Zone combobox
        currTimeZone = self.venueTimezoneSelect.currentText()
                
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
        self.venueConfedSelect.setCurrentIndex(self.venueConfedSelect.findText(confedStr, Qt.MatchExactly))
        
        self.filterCountriesAndTimeZones()
        # update index of Country combobox to that of currCountry
        self.venueCountrySelect.setCurrentIndex(self.venueCountrySelect.findText(currCountry, Qt.MatchExactly))
        # update index of Time Zone combobox to that of currTimeZone
        self.venueTimezoneSelect.setCurrentIndex(self.venueTimezoneSelect.findText(currTimeZone, Qt.MatchExactly))
        
    def filterCountriesAndTimeZones(self):
        """Enables Country and Time Zone comboboxes and filters contents.
       
       Filters Country and Time Zone comboboxes upon selection of Confederation."""
        # flush filter
        self.countryModel.setFilter(QString())
        self.timezoneModel.setFilter(QString())
        self.countryModel.select()
        self.timezoneModel.select()
        
        # enable Country combobox if disabled
        if ~self.venueCountrySelect.isEnabled():
            self.venueCountrySelect.setEnabled(True)
            
        # enable Time Zone combobox if disabled
        if ~self.venueTimezoneSelect.isEnabled():
            self.venueTimezoneSelect.setEnabled(True)
        
        # extract confed_id
        currIdx = self.venueConfedSelect.currentIndex()
        id = self.confedModel.record(currIdx).value("confed_id").toString()
        # filter tbl_countries and tbl_timezones
        self.countryModel.setFilter(QString("confed_id = %1").arg(id))
        self.timezoneModel.setFilter(QString("confed_id = %1").arg(id))
        self.countryModel.select()
        self.timezoneModel.select()
    
    def openVenueHistory(self, venue_id):
        """Opens Venue History subdialog for a specific match from Match dialog.
        
        Saves current match record, instantiates VenueHistoryDlg object and opens window.
        Argument: 
        venue_id -- primary key of current record in Venues table
        
        """
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
            return
            
        subdialog = VenueHistoryDlg(venue_id, self)
        subdialog.exec_()
        self.mapper.setCurrentIndex(row)
        
        
class VenueHistoryDlg(QDialog, ui_venuehistoryentry.Ui_VenueHistoryDlg):
    """Implements Venue History data entry dialog, and accesses and writes to VenueHistory table.
    
    This dialog accepts historical data on the playing surface, dimensions, and seated and unseated
    capacity of the venue.
    
    """
    
    HISTORY_ID, VENUE_ID, EFFDATE, SURFACE_ID, PITCH_LENGTH, PITCH_WIDTH, CAPACITY, SEATS = range(8)
    
    def __init__(self, venue_id, parent=None):
        """Constructor for VenueHistoryDlg class"""
        super(VenueHistoryDlg, self).__init__(parent)
        self.setupUi(self)
        self.venue_id = venue_id
    
        # define underlying database model (tbl_venuehistory)
        sourceModel = QSqlRelationalTableModel(self)
        sourceModel.setTable("tbl_venuehistory")
        sourceModel.setRelation(VenueHistoryDlg.VENUE_ID, QSqlRelation("tbl_venues", "venue_id", "ven_name"))
        sourceModel.setRelation(VenueHistoryDlg.SURFACE_ID, QSqlRelation("tbl_venuesurfaces", "venuesurface_id", "vensurf_desc"))
        
        # set header data for table view
        sourceModel.setHeaderData(VenueHistoryDlg.EFFDATE, Qt.Horizontal, QVariant("Effective Date"))
        sourceModel.setHeaderData(VenueHistoryDlg.SURFACE_ID, Qt.Horizontal, QVariant("Playing Surface"))
        sourceModel.setHeaderData(VenueHistoryDlg.PITCH_LENGTH, Qt.Horizontal, QVariant("Pitch Length (m)"))
        sourceModel.setHeaderData(VenueHistoryDlg.PITCH_WIDTH, Qt.Horizontal, QVariant("Pitch Width (m)"))
        sourceModel.setHeaderData(VenueHistoryDlg.CAPACITY, Qt.Horizontal, QVariant("Capacity"))
        sourceModel.setHeaderData(VenueHistoryDlg.SEATS, Qt.Horizontal, QVariant("Seats"))
        sourceModel.select()

        # set venue name
        query = QSqlQuery()
        query.exec_(QString("SELECT ven_name FROM tbl_venues WHERE venue_id = %1").arg(self.venue_id))
        if query.isActive():
            query.next()
            venueName = query.value(0).toString()
        else:
            return
        self.venueName_display.setText(venueName)
                
        # define proxy model
        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSourceModel(sourceModel)
        # define filter on venue name
        self.proxyModel.setFilterRegExp(QRegExp(venueName, Qt.CaseSensitive, QRegExp.FixedString))
        self.proxyModel.setFilterKeyColumn(VenueHistoryDlg.VENUE_ID)
        # define sort on effective date
        self.proxyModel.sort(VenueHistoryDlg.EFFDATE, Qt.AscendingOrder)        
        
        # define table view
        self.venueHistory.setModel(self.proxyModel)
        # form GenericDelegate
        venueDelegate = GenericDelegate(self)
        venueDelegate.insertColumnDelegate(VenueHistoryDlg.EFFDATE, DateColumnDelegate())
        venueDelegate.insertColumnDelegate(VenueHistoryDlg.SURFACE_ID, SurfaceColumnDelegate())
        venueDelegate.insertColumnDelegate(VenueHistoryDlg.PITCH_LENGTH, NumericColumnDelegate(90, 120, "000"))
        venueDelegate.insertColumnDelegate(VenueHistoryDlg.PITCH_WIDTH, NumericColumnDelegate(45, 90, "00"))
        venueDelegate.insertColumnDelegate(VenueHistoryDlg.CAPACITY, NumericColumnDelegate(0, 999999, "000000"))
        venueDelegate.insertColumnDelegate(VenueHistoryDlg.SEATS, NumericColumnDelegate(0, 999999, "000000"))
        self.venueHistory.setItemDelegate(venueDelegate)

        self.venueHistory.setSelectionMode(QTableView.SingleSelection)
        self.venueHistory.setSelectionBehavior(QTableView.SelectRows)
        self.venueHistory.setColumnHidden(VenueHistoryDlg.HISTORY_ID, True)
        self.venueHistory.setColumnHidden(VenueHistoryDlg.VENUE_ID, True)
        self.venueHistory.resizeColumnsToContents()
        self.venueHistory.horizontalHeader().setStretchLastSection(True)
                
        # configure signal/slot        
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        
    def accept(self):
        """Commits changes to database and closes dialog."""
        index = self.venueHistory.currentIndex()
        row = index.row()
        idIndex = self.proxyModel.index(row, VenueHistoryDlg.VENUE_ID)
        self.proxyModel.setData(idIndex, QVariant(self.venue_id))
        self.proxyModel.submit()
        QDialog.accept(self)
        
    def addRecord(self):
        """Inserts a new record in the database and focuses on the effective date field in table view."""
        index = self.venueHistory.currentIndex()
        row = index.row()
        if index.isValid():
            idIndex = self.proxyModel.index(row, VenueHistoryDlg.VENUE_ID)
            self.proxyModel.setData(idIndex, QVariant(self.venue_id))
            self.proxyModel.submit()
        row = self.proxyModel.rowCount()
        self.proxyModel.insertRow(row)
        index = self.proxyModel.index(row, VenueHistoryDlg.EFFDATE)
        self.venueHistory.setCurrentIndex(index)
        self.venueHistory.edit(index)
        
    def deleteRecord(self):
        """Deletes current row in table view from database.
        
        Deletion is handled at the model level.
        """
        index = self.venueHistory.currentIndex()
        if not index.isValid():
            return
        if QMessageBox.question(self, QString("Delete Record"), 
                                            QString("Delete current record?"), 
                                            QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        else:        
            self.proxyModel.removeRow(index.row())
            self.proxyModel.submit()
