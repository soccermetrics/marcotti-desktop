#!/usr/bin/env python
#
#    Football Match Result Database (FMRD)
#    Desktop-based data entry tool
#
#    Contains classes that implement match overview entry forms to main tables of FMRD.
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
from FmrdLib import Constants
from FmrdLib.CustomDelegates import *

# Class: compEntryDlg
# Inherits: Ui_compEntryDlg (ui_competitionentry)
#
# Implements user interface to Competitions table.
class compEntryDlg(QDialog, ui_competitionentry.Ui_compEntryDlg):

    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID,  DESC = range(2)
    
    def __init__(self, parent=None):
        super(compEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_competitions")
        self.model.setSort(compEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.compID_display, compEntryDlg.ID)
        self.mapper.addMapping(self.competitionEdit, compEntryDlg.DESC)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)        
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(compEntryDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(compEntryDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(compEntryDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(compEntryDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        
    # accept: Submit changes to database, and then close window
    def accept(self):
        self.mapper.submit()
        QDialog.accept(self)
    
    # saveRecord: Submit changes to database,
    #                     advance to next record 
    #                     apply conditions if at first/last record
    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == teamEntryDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == teamEntryDlg.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == teamEntryDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == teamEntryDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    # addRecord: add new record at end of entry list
    #                    set focus to edit line    
    def addRecord(self):
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(competition_id) FROM tbl_competitions"))
        if query.next():
            maxCompetitionID= query.value(0).toInt()[0]
            if not maxCompetitionID:
                competition_id = Constants.MinCompetitionID
            else:
                self.mapper.submit()
                competition_id= QString()
                competition_id.setNum(maxCompetitionID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to competitionID field
        self.compID_display.setText(competition_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)        
        self.competitionEdit.setFocus()
    
    # deleteRecord: delete record from database
    #                        ask user to confirm deletion
    def deleteRecord(self):
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)        
                
# Class: teamEntryDlg
# Inherits: Ui_teamEntryDlg (ui_teamentry)
#
# Implements user interface for Teams table.
class teamEntryDlg(QDialog, ui_teamentry.Ui_teamEntryDlg):

    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID,  NAME = range(2)
    
    def __init__(self, parent=None):
        super(teamEntryDlg, self).__init__(parent)
        self.setupUi(self)

        # define model
        # underlying database model
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_teams")
        self.model.setSort(teamEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.teamID_display, teamEntryDlg.ID)
        self.mapper.addMapping(self.teamNameEdit, teamEntryDlg.NAME)
        self.mapper.toFirst()
        
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        
        # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(teamEntryDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(teamEntryDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(teamEntryDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(teamEntryDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        
    # accept: Submit changes to database, and then close window
    def accept(self):
        self.mapper.submit()
        QDialog.accept(self)
    
    # saveRecord: Submit changes to database,
    #                     advance to next record 
    #                     apply conditions if at first/last record
    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == teamEntryDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == teamEntryDlg.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == teamEntryDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == teamEntryDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)
        
    # addRecord: add new record at end of entry list
    #                    set focus to edit line    
    def addRecord(self):
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(team_id) FROM tbl_teams"))
        if query.next():
            maxTeamID= query.value(0).toInt()[0]
            if not maxTeamID:
                team_id = Constants.MinTeamID
            else:
                self.mapper.submit()
                team_id= QString()
                team_id.setNum(maxTeamID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to teamID field
        self.teamID_display.setText(team_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        self.teamNameEdit.setFocus()
    
    # deleteRecord: delete record from database
    #                        ask user to confirm deletion
    def deleteRecord(self):
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)        
        
# venueEntryDlg: Venue entry dialog
class venueEntryDlg(QDialog, ui_venueentry.Ui_venueEntryDlg):

    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID,  TEAM_ID,  CTRY_ID, CITY, NAME, ALT, LAT, LONG = range(8)

    def __init__(self, parent=None):
        super(venueEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define local parameters
        CONFED_ID, CONFED_NAME = range(2)
        COUNTRY_ID, COUNTRY_NAME = range(2)
        HOST_ID, HOST_NAME = range(2)

        # define underlying database model
        # because of foreign keys, instantiate QSqlRelationalTableModel and
        # define relations to it
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_venues")
        self.model.setRelation(venueEntryDlg.TEAM_ID, QSqlRelation("tbl_teams", "team_id", "tm_name"))
        self.model.setRelation(venueEntryDlg.CTRY_ID, QSqlRelation("tbl_countries", "country_id", "cty_name"))   
        self.model.setSort(venueEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        localDelegate = GenericDelegate(self)
        localDelegate.insertColumnDelegate(venueEntryDlg.CTRY_ID, CountryComboBoxDelegate(self))
        self.mapper.setItemDelegate(localDelegate)
        self.mapper.addMapping(self.venueID_display, venueEntryDlg.ID)
        
        # relation model for Country combobox
        self.countryModel = self.model.relationModel(venueEntryDlg.CTRY_ID)
        self.countryModel.setSort(COUNTRY_ID, Qt.AscendingOrder)
        self.venueCountrySelect.setModel(self.countryModel)
        self.venueCountrySelect.setModelColumn(self.countryModel.fieldIndex("cty_name"))
        self.mapper.addMapping(self.venueCountrySelect, venueEntryDlg.CTRY_ID)
        
        # relation model for Home Team combobox
        self.teamModel = self.model.relationModel(venueEntryDlg.TEAM_ID)
        self.teamModel.setSort(HOST_ID, Qt.AscendingOrder)
        self.venueTeamSelect.setModel(self.teamModel)
        self.venueTeamSelect.setModelColumn(self.teamModel.fieldIndex("tm_name"))
        self.mapper.addMapping(self.venueTeamSelect, venueEntryDlg.TEAM_ID)        
        
        # map other widgets on form
        self.mapper.addMapping(self.venueCityEdit, venueEntryDlg.CITY)
        self.mapper.addMapping(self.venueNameEdit, venueEntryDlg.NAME)
        self.mapper.addMapping(self.venueAltEdit, venueEntryDlg.ALT)
        self.mapper.addMapping(self.venueLatitudeEdit, venueEntryDlg.LAT)
        self.mapper.addMapping(self.venueLongitudeEdit, venueEntryDlg.LONG)
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
        confedMapper.addMapping(self.venueConfedSelect, CONFED_NAME)
        confedMapper.toFirst()       
       
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)       

         # configure signal/slot
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(venueEntryDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(venueEntryDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(venueEntryDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(venueEntryDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        self.connect(self.mapper, SIGNAL("currentIndexChanged(int)"), self.updateConfed)
        self.connect(self.venueConfedSelect, SIGNAL("activated(int)"), self.filterCountryBox)
     
    # Method: updateConfed
    #
    # Update current index of Confederation combobox
    # Ensures consistency between confederation and nation
    # in existing records
    def updateConfed(self):
        # look for current index on Country combobox
        # extract confed_id from underlying model
        currIdx = self.venueCountrySelect.currentIndex()
        currCountry = self.venueCountrySelect.currentText()
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
        self.venueConfedSelect.setCurrentIndex(self.venueConfedSelect.findText(confedStr, Qt.MatchExactly))
        
        # update index of Country combobox to that of currCountry
        self.filterCountryBox()
        self.venueCountrySelect.setCurrentIndex(self.venueCountrySelect.findText(currCountry, Qt.MatchExactly))
     
    # Method: filterCountryBox
    #
    # Enable Country combobox (if not already enabled) and filter contents 
    # of Country combobox when confederation is selected
    def filterCountryBox(self):
        # enable Country combobox if disabled
        if ~self.venueCountrySelect.isEnabled():
            self.venueCountrySelect.setEnabled(True)
        
        # filter tbl_countries based on confederation selection
        currIdx = self.venueConfedSelect.currentIndex()
        id = self.confedModel.record(currIdx).value("confed_id").toString()
        self.countryModel.setFilter(QString("confed_id = %1").arg(id))
        self.countryModel.select()
        
    # Method: accept
    #
    # Submit changes to database, and then close window
    def accept(self):
        self.mapper.submit()
        QDialog.accept(self)
    
    # Method: saveRecord
    # 
    # Submit changes to database,
    # advance to next record, 
    # apply conditions if at first/last record
    def saveRecord(self, where):
        row = self.mapper.currentIndex()
        self.mapper.submit()
        if where == teamEntryDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == teamEntryDlg.PREV:
            if row <= 1:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
                row = 0
            else:
                if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)                    
                row -= 1
        elif where == teamEntryDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row >= self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
                row = self.model.rowCount() - 1
        elif where == teamEntryDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1            
        self.mapper.setCurrentIndex(row)
        
    # Method: addRecord
    #
    # Add new record at end of entry list
    # Disable Country combobox
    # Set focus to First Name field
    def addRecord(self):
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()        
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(venue_id) FROM tbl_venues"))
        if query.next():
            maxVenueID= query.value(0).toInt()[0]
            if not maxVenueID:
                venue_id = Constants.MinVenueID
            else:
                self.mapper.submit()
                venue_id= QString()
                venue_id.setNum(maxVenueID+1)          
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to venueID field
        self.venueID_display.setText(venue_id)
        
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)        
        self.venueCountrySelect.setDisabled(True)        
        self.venueNameEdit.setFocus()
    
    # Method: deleteRecord
    #
    # Delete record from database upon user confirmation
    def deleteRecord(self):
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        self.model.submitAll()
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row) 

