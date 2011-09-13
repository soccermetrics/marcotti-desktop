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
from FmrdLib.CheckTables import *

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


class VenueEntryDlg(QDialog, ui_venueentry.Ui_VenueEntryDlg):
    """Implements Venues data entry dialog, and accesses and writes to Venues table.
    
    This dialog accepts data on the match venues used in the football competition.
    
    """
    
    ID,  CTRY_ID, TZ_ID,  CITY, NAME, ALT, LAT, LONG = range(8)

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
        self.venueAltEdit.setEnabled(True)
        self.venueLatitudeEdit.setEnabled(True)
        self.venueLongitudeEdit.setEnabled(True)
        self.venueHistoryButton.setEnabled(True)
        
        # initialization of data widgets
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
        editorList = (self.venueTimezoneSelect, self.venueCountrySelect)
        columnList = (VenueEntryDlg.TZ_ID, VenueEntryDlg.CTRY_ID)
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
    
    ID, VENUE_ID, EFFDATE, SURFACE_ID, PITCH_LENGTH, PITCH_WIDTH, CAPACITY, SEATS = range(8)
    
    def __init__(self, venue_id, parent=None):
        """Constructor for VenueHistoryDlg class"""
        super(VenueHistoryDlg, self).__init__(parent)
        self.setupUi(self)
        self.local_id = venue_id
    
        SURF_NAME = 1
        
        # define underlying database model (tbl_venuehistory)
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_venuehistory")
        self.model.setRelation(VenueHistoryDlg.SURFACE_ID, QSqlRelation("tbl_venuesurfaces", "venuesurface_id", "vensurf_desc"))
        self.model.setFilter(QString("venue_id = %1").arg(venue_id))
        self.model.setSort(VenueHistoryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # set up validators
        self.venueLengthEdit.setInputMask("000")
        self.venueLengthEdit.setValidator(QIntValidator(90, 120, self.layoutWidget))
        
        self.venueWidthEdit.setInputMask("00")
        self.venueWidthEdit.setValidator(QIntValidator(45, 90, self.layoutWidget))
        
        self.venueCapacityEdit.setInputMask("000000")
        self.venueCapacityEdit.setValidator(QIntValidator(0, 999999, self.layoutWidget))
        
        self.venueSeatsEdit.setInputMask("000000")
        self.venueSeatsEdit.setValidator(QIntValidator(0, 999999, self.layoutWidget))
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        localDelegate = GenericDelegate(self)
        localDelegate.insertColumnDelegate(VenueHistoryDlg.VENUE_ID, IDLineEditDelegate("tbl_venues", "ven_name", "venue_id", self))
        self.mapper.setItemDelegate(localDelegate)
        self.mapper.addMapping(self.historyID_display, VenueHistoryDlg.ID)
        self.mapper.addMapping(self.venueName_display, VenueHistoryDlg.VENUE_ID)
        self.mapper.addMapping(self.venueDateEdit, VenueHistoryDlg.EFFDATE)
        
        # relation model for Playing Surface combobox
        self.surfaceModel = self.model.relationModel(VenueHistoryDlg.SURFACE_ID)
        self.surfaceModel.setSort(SURF_NAME, Qt.AscendingOrder)
        self.venueSurfaceSelect.setModel(self.surfaceModel)
        self.venueSurfaceSelect.setModelColumn(self.surfaceModel.fieldIndex("vensurf_desc"))
        self.venueSurfaceSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.venueSurfaceSelect, VenueHistoryDlg.SURFACE_ID)
        
        # map other widgets on form
        self.mapper.addMapping(self.venueLengthEdit, VenueHistoryDlg.PITCH_LENGTH)
        self.mapper.addMapping(self.venueWidthEdit, VenueHistoryDlg.PITCH_WIDTH)
        self.mapper.addMapping(self.venueCapacityEdit, VenueHistoryDlg.CAPACITY)
        self.mapper.addMapping(self.venueSeatsEdit, VenueHistoryDlg.SEATS)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)

        # disable Next and Last Entry buttons if less than two records
        if self.model.rowCount() < 2:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)

        # disable all fields and History button if no records in database table
        if not self.model.rowCount():
            self.historyID_display.setDisabled(True)
            self.venueDateEdit.setDisabled(True)
            self.venueSurfaceSelect.setDisabled(True)
            self.venueLengthEdit.setDisabled(True)
            self.venueWidthEdit.setDisabled(True)
            self.venueCapacityEdit.setDisabled(True)
            self.venueSeatsEdit.setDisabled(True)
            # disable save and delete entry buttons
            self.saveEntry.setDisabled(True)
            self.deleteEntry.setDisabled(True)
        
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
        """Adds new record at end of entry list."""        
        
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
        query.exec_(QString("SELECT MAX(venuehistory_id) FROM tbl_venuehistory"))
        if query.next():
            maxVenueHistoryID = query.value(0).toInt()[0]
            if not maxVenueHistoryID:
                venuehistory_id = Constants.MinVenueHistoryID
            else:
                venuehistory_id= QString()
                venuehistory_id.setNum(maxVenueHistoryID+1)
    
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to playerhistoryID field
        self.historyID_display.setText(venuehistory_id)
        
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
        
        # enable form widgets and History button
        self.historyID_display.setEnabled(True)
        self.venueDateEdit.setEnabled(True)
        self.venueSurfaceSelect.setEnabled(True)
        self.venueLengthEdit.setEnabled(True)
        self.venueWidthEdit.setEnabled(True)
        self.venueCapacityEdit.setEnabled(True)
        self.venueSeatsEdit.setEnabled(True)
        
        # initialize form widgets
        self.venueLengthEdit.setText("105")
        self.venueWidthEdit.setText("68")
        self.venueCapacityEdit.setText("0")
        self.venueSeatsEdit.setText("0")
        self.venueDateEdit.setFocus()
    
    def deleteRecord(self):
        """Deletes record from database upon user confirmation."""
        
        if QMessageBox.question(self, QString("Delete Record"), 
                                            QString("Delete current record?"), 
                                            QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        else:
            # delete records in Player History table
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
                
    def isDirty(self, row):
        """Compares current state of data entry form to current record in database, and returns a boolean.
        
        Arguments:
            row: current record in mapper and model
        
        Returns:
            TRUE: there are changes between data entry form and current record in database,
                      or new record in database
            FALSE: no changes between data entry form and current record in database
                      or no records in database
        """
        
        if not self.model.rowCount():
            return False
            
        # line edit fields
        editorList = (self.venueDateEdit, self.venueLengthEdit, self.venueWidthEdit, self.venueCapacityEdit, self.venueSeatsEdit)
        columnList = (VenueHistoryDlg.EFFDATE, VenueHistoryDlg.PITCH_LENGTH, VenueHistoryDlg.PITCH_WIDTH, 
                              VenueHistoryDlg.CAPACITY, VenueHistoryDlg.SEATS)
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.text() != self.model.data(index).toString():
                return True
                
        # combobox fields
        editorList = (self.venueSurfaceSelect, )
        columnList = (VenueHistoryDlg.SURFACE_ID, )
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.currentText() != self.model.data(index).toString():
                return True
        
        return False
