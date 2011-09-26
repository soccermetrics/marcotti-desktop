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
from FmrdLib import (Constants, MsgPrompts)
from FmrdLib.CustomDelegates import *
from FmrdLib.CustomModels import *
from FmrdLib.CheckTables import *

from fmrd_personnel import LineupEntryDlg

"""Contains classes that implement entry forms to match tables of FMRD.

Classes:
EnviroEntryDlg - data entry to Environments table
MatchEntryDlg - data entry to Matches table
"""

class MatchEntryDlg(QDialog, ui_matchentry.Ui_MatchEntryDlg):
    """Implements match entry dialog, and accesses and writes to Matches table.
    
    This dialog is one of the central dialogs of the database entry form. It accepts
    high-level data on the match and opens subdialogs on match lineups and 
    environmental conditions of the match.
    
    """
    
    ID,  DATE, HALF1, HALF2, ATTEND, COMP_ID, ROUND_ID, VENUE_ID, REF_ID = range(9)
    
    def __init__(self, parent=None):
        """Constructor for MatchEntryDlg class."""
        super(MatchEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define local parameters
        HOME_ID = AWAY_ID = 1
        TEAM_NAME = 1
        COUNTRY = 2
        CMP_ID,  COMP_NAME = range(2)
        RND_ID,  ROUND_NAME = range(2)
        VEN_ID,  VENUE_NAME = range(2)
        RF_ID,  REF_NAME,  REF_SORT = range(3)
        CONFED_ID, CONFED_NAME = range(2)
        MG_ID,  MGR_NAME,  MGR_SORT = range(3)
        
        # define underlying database model (tbl_matches)
        # because of foreign keys, instantiate QSqlRelationalTableModel and define relations to it
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_matches")
        self.model.setRelation(MatchEntryDlg.COMP_ID, QSqlRelation("tbl_competitions", "competition_id", "comp_name"))
        self.model.setRelation(MatchEntryDlg.ROUND_ID, QSqlRelation("tbl_rounds", "round_id", "round_desc"))
        self.model.setRelation(MatchEntryDlg.VENUE_ID, QSqlRelation("tbl_venues", "venue_id", "ven_name"))
        self.model.setRelation(MatchEntryDlg.REF_ID, QSqlRelation("referees_list", "referee_id", "full_name"))
        self.model.setSort(MatchEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.setItemDelegate(QSqlRelationalDelegate(self))        

        # relation model for Competitions combobox
        self.compModel = self.model.relationModel(MatchEntryDlg.COMP_ID)
        self.compModel.setSort(CMP_ID, Qt.AscendingOrder)
        self.matchCompSelect.setModel(self.compModel)
        self.matchCompSelect.setModelColumn(self.compModel.fieldIndex("comp_name"))
        self.matchCompSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.matchCompSelect, MatchEntryDlg.COMP_ID)
        
        # relation model for Rounds combobox
        self.roundModel = self.model.relationModel(MatchEntryDlg.ROUND_ID)
        self.roundModel.setSort(RND_ID, Qt.AscendingOrder)
        self.matchRoundSelect.setModel(self.roundModel)
        self.matchRoundSelect.setModelColumn(self.roundModel.fieldIndex("round_desc"))
        self.matchRoundSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.matchRoundSelect, MatchEntryDlg.ROUND_ID)
        
        # relation model for Venues combobox
        self.venueModel = self.model.relationModel(MatchEntryDlg.VENUE_ID)
        self.venueModel.setSort(VEN_ID, Qt.AscendingOrder)
        self.matchVenueSelect.setModel(self.venueModel)
        self.matchVenueSelect.setModelColumn(self.venueModel.fieldIndex("ven_name"))
        self.matchVenueSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.matchVenueSelect, MatchEntryDlg.VENUE_ID)
        
        # relation model for Referees combobox
        self.refereeModel = self.model.relationModel(MatchEntryDlg.REF_ID)
        self.refereeModel.setSort(REF_SORT, Qt.AscendingOrder)
        self.matchRefSelect.setModel(self.refereeModel)
        self.matchRefSelect.setModelColumn(self.refereeModel.fieldIndex("full_name"))
        self.matchRefSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.matchRefSelect, MatchEntryDlg.REF_ID)        

        # map other widgets on form
        self.mapper.addMapping(self.matchID_display, MatchEntryDlg.ID)
        self.mapper.addMapping(self.matchDateEdit, MatchEntryDlg.DATE)
        self.mapper.addMapping(self.firstHalfLengthEdit, MatchEntryDlg.HALF1)
        self.mapper.addMapping(self.secondHalfLengthEdit, MatchEntryDlg.HALF2)
        self.mapper.addMapping(self.attendanceEdit, MatchEntryDlg.ATTEND)
        self.mapper.toFirst()
        
        # define models used in Team and Manager comboboxes
        # we need multiple instantiations of Teams and Managers tables
        # so that there is no confusion in SQL logic
        
        self.homeCountryModel = QSqlTableModel(self)
        self.homeCountryModel.setTable("tbl_countries")
        self.homeCountryModel.setSort(COUNTRY, Qt.AscendingOrder)
        self.homeCountryModel.select()
        
        self.awayCountryModel = QSqlTableModel(self)
        self.awayCountryModel.setTable("tbl_countries")
        self.awayCountryModel.setSort(COUNTRY, Qt.AscendingOrder)
        self.awayCountryModel.select()

        self.homeManagerModel = QSqlTableModel(self)
        self.homeManagerModel.setTable("managers_list")
        self.homeManagerModel.setSort(MGR_SORT, Qt.AscendingOrder)
        self.homeManagerModel.select()
        
        self.awayManagerModel = QSqlTableModel(self)
        self.awayManagerModel.setTable("managers_list")
        self.awayManagerModel.setSort(MGR_SORT, Qt.AscendingOrder)
        self.awayManagerModel.select()
        
        # set up Home Team linking table 
        # set up Home Team combobox with items from tbl_teams table
        self.hometeamModel = TeamLinkingModel("tbl_hometeams", self)
        self.hometeamSelect.setModel(self.homeCountryModel)
        self.hometeamSelect.setModelColumn(self.homeCountryModel.fieldIndex("cty_name"))
        self.hometeamSelect.setCurrentIndex(-1)

        # set up Away Team linking table
        # set up Away Team combobox with items from tbl_teams table
        self.awayteamModel = TeamLinkingModel("tbl_awayteams", self)
        self.awayteamSelect.setModel(self.awayCountryModel)
        self.awayteamSelect.setModelColumn(self.awayCountryModel.fieldIndex("cty_name"))
        self.awayteamSelect.setCurrentIndex(-1)

        # set up Home Manager linking table
        # set up Home Manager combobox with items from managers_list table
        self.homemgrModel = ManagerLinkingModel("tbl_homemanagers", self)
        self.homemgrSelect.setModel(self.homeManagerModel)
        self.homemgrSelect.setModelColumn(self.homeManagerModel.fieldIndex("full_name"))
        self.homemgrSelect.setCurrentIndex(-1)

        # set up Away Manager linking table
        # set up Away Manager combobox with items from managers_list table
        self.awaymgrModel = ManagerLinkingModel("tbl_awaymanagers", self)
        self.awaymgrSelect.setModel(self.awayManagerModel)
        self.awaymgrSelect.setModelColumn(self.awayManagerModel.fieldIndex("full_name"))
        self.awaymgrSelect.setCurrentIndex(-1)

        # Home Team mapper
        self.hometeamMapper = QDataWidgetMapper(self)
        self.hometeamMapper.setSubmitPolicy(QDataWidgetMapper.AutoSubmit)
        self.hometeamMapper.setModel(self.hometeamModel)
        hometeamDelegate = GenericDelegate(self)
        hometeamDelegate.insertColumnDelegate(TEAM_NAME, HomeTeamComboBoxDelegate(self))
        self.hometeamMapper.setItemDelegate(hometeamDelegate)
        self.hometeamMapper.addMapping(self.hometeamSelect, TEAM_NAME)
        self.hometeamMapper.toFirst()
        
        # Away Team mapper
        self.awayteamMapper = QDataWidgetMapper(self)
        self.awayteamMapper.setSubmitPolicy(QDataWidgetMapper.AutoSubmit)
        self.awayteamMapper.setModel(self.awayteamModel)
        awayteamDelegate = GenericDelegate(self)
        awayteamDelegate.insertColumnDelegate(TEAM_NAME, AwayTeamComboBoxDelegate(self))
        self.awayteamMapper.setItemDelegate(awayteamDelegate)
        self.awayteamMapper.addMapping(self.awayteamSelect, TEAM_NAME)
        self.awayteamMapper.toFirst()

        # Home Manager mapper
        self.homemgrMapper = QDataWidgetMapper(self)
        self.homemgrMapper.setSubmitPolicy(QDataWidgetMapper.AutoSubmit)
        self.homemgrMapper.setModel(self.homemgrModel)
        homemgrDelegate = GenericDelegate(self)
        homemgrDelegate.insertColumnDelegate(MGR_NAME, HomeMgrComboBoxDelegate(self))
        self.homemgrMapper.setItemDelegate(homemgrDelegate)
        self.homemgrMapper.addMapping(self.homemgrSelect, MGR_NAME)
        self.homemgrMapper.toFirst()
        
        # Away Manager mapper
        self.awaymgrMapper = QDataWidgetMapper(self)
        self.awaymgrMapper.setSubmitPolicy(QDataWidgetMapper.AutoSubmit)
        self.awaymgrMapper.setModel(self.awaymgrModel)
        awaymgrDelegate = GenericDelegate(self)
        awaymgrDelegate.insertColumnDelegate(MGR_NAME, AwayMgrComboBoxDelegate(self))
        self.awaymgrMapper.setItemDelegate(awaymgrDelegate)
        self.awaymgrMapper.addMapping(self.awaymgrSelect, MGR_NAME)
        self.awaymgrMapper.toFirst()        
        
        # define models used in Confederation comboboxes
        # these comboboxes are used to filter Country comboboxes
        # we need multiple instantiations of Confederations tables
        # so that there is no confusion in SQL logic
        
        # Home Confederation model
        self.homeconfedModel = QSqlTableModel(self)
        self.homeconfedModel.setTable("tbl_confederations")
        self.homeconfedModel.setSort(CONFED_ID, Qt.AscendingOrder)
        self.homeconfedModel.select()
    
        # Home Confederation combobox
        self.homeconfedSelect.setModel(self.homeconfedModel)
        self.homeconfedSelect.setModelColumn(self.homeconfedModel.fieldIndex("confed_name"))
        self.homeconfedSelect.setCurrentIndex(-1)
        
        # Home Confederation mapper 
        homeconfedMapper = QDataWidgetMapper(self)
        homeconfedMapper.setModel(self.homeconfedModel)
        homeconfedMapper.setItemDelegate(HomeConfedComboBoxDelegate(self))
        homeconfedMapper.addMapping(self.homeconfedSelect, CONFED_NAME)
        homeconfedMapper.toFirst()       
        
        # Away Confederation model
        self.awayconfedModel = QSqlTableModel(self)
        self.awayconfedModel.setTable("tbl_confederations")
        self.awayconfedModel.setSort(CONFED_ID, Qt.AscendingOrder)
        self.awayconfedModel.select()
    
        # Away Confederation combobox
        self.awayconfedSelect.setModel(self.awayconfedModel)
        self.awayconfedSelect.setModelColumn(self.awayconfedModel.fieldIndex("confed_name"))
        self.awayconfedSelect.setCurrentIndex(-1)
        
        # Away Confederation mapper 
        awayconfedMapper = QDataWidgetMapper(self)
        awayconfedMapper.setModel(self.awayconfedModel)
        awayconfedMapper.setItemDelegate(AwayConfedComboBoxDelegate(self))
        awayconfedMapper.addMapping(self.awayconfedSelect, CONFED_NAME)
        awayconfedMapper.toFirst()       

        # disable all fields if no records in database table
        if not self.model.rowCount():
            self.matchID_display.setDisabled(True)
            self.matchCompSelect.setDisabled(True)
            self.matchRoundSelect.setDisabled(True)
            self.matchDateEdit.setDisabled(True)
            self.matchRefSelect.setDisabled(True)
            self.matchVenueSelect.setDisabled(True)
            self.firstHalfLengthEdit.setDisabled(True)
            self.secondHalfLengthEdit.setDisabled(True)
            self.attendanceEdit.setDisabled(True)
            self.homeconfedSelect.setDisabled(True)
            self.hometeamSelect.setDisabled(True)
            self.homemgrSelect.setDisabled(True)
            self.awayconfedSelect.setDisabled(True)
            self.awayteamSelect.setDisabled(True)
            self.awaymgrSelect.setDisabled(True)
            
            self.homeLineupButton.setDisabled(True)
            self.awayLineupButton.setDisabled(True)
            self.enviroButton.setDisabled(True)
            
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
        
        # configure signal/slots
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.LAST))
        self.connect(self.saveEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NULL))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)           
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        
        self.connect(self.mapper, SIGNAL("currentIndexChanged(int)"), 
                            lambda: self.updateConfed((self.homeconfedSelect, self.awayconfedSelect), (self.hometeamSelect, self.awayteamSelect)))
        
        self.connect(self.homeconfedSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.enableWidget(self.hometeamSelect))
        self.connect(self.awayconfedSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.enableWidget(self.awayteamSelect))

        self.connect(self.homeconfedSelect, SIGNAL("activated(int)"), 
                                                                        lambda: self.filterCountryBox(self.homeconfedSelect, self.hometeamSelect))
        self.connect(self.awayconfedSelect, SIGNAL("activated(int)"), 
                                                                        lambda: self.filterCountryBox(self.awayconfedSelect, self.awayteamSelect))

        self.connect(self.hometeamSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.enableWidget(self.homemgrSelect))
        self.connect(self.homemgrSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                     lambda: self.enableWidget(self.homeLineupButton))
        self.connect(self.homemgrSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                     lambda: self.enableWidget(self.awayconfedSelect))

        self.connect(self.awayteamSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.enableWidget(self.awaymgrSelect))
        self.connect(self.awaymgrSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                     lambda: self.enableWidget(self.awayLineupButton))
        self.connect(self.awaymgrSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                     lambda: self.enableWidget(self.enviroButton))

        self.connect(self.hometeamSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.updateLinkingTable(self.hometeamMapper, self.hometeamSelect))
        self.connect(self.awayteamSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.updateLinkingTable(self.awayteamMapper, self.awayteamSelect))
        self.connect(self.homemgrSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                     lambda: self.updateLinkingTable(self.homemgrMapper, self.homemgrSelect))
        self.connect(self.awaymgrSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                     lambda: self.updateLinkingTable(self.awaymgrMapper, self.awaymgrSelect))

        self.connect(self.enviroButton, SIGNAL("clicked()"), lambda: self.openEnviros(self.matchID_display.text()))
        self.connect(self.homeLineupButton, SIGNAL("clicked()"), 
                                                                lambda: self.openLineups(self.matchID_display.text(), self.hometeamSelect.currentText()))
        self.connect(self.awayLineupButton, SIGNAL("clicked()"), 
                                                               lambda: self.openLineups(self.matchID_display.text(), self.awayteamSelect.currentText()))

    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if MsgPrompts.SaveDiscardOptionPrompt(self):
                if not self.mapper.submit():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
    
    def submitForms(self):
        """Writes to main database table and linking tables and returns result boolean."""
        
        mapperList = [self.hometeamMapper, self.awayteamMapper, self.homemgrMapper, self.awaymgrMapper] 
        editorList = [self.hometeamSelect, self.awayteamSelect, self.homemgrSelect, self.awaymgrSelect]
        
        if self.mapper.submit(): 
            for mapper, editor in zip(mapperList, editorList):
                if not self.updateLinkingTable(mapper, editor):
                    return False
        else:
            return False
    
    def saveRecord(self, where):
        """"Submits changes to database, navigates through form, and resets subforms."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if MsgPrompts.SaveDiscardOptionPrompt(self):
                if not self.mapper.submit():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
            else:
                self.mapper.revert()
        
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
        
        # refresh subforms
        currentID = self.matchID_display.text()
        self.refreshSubForms(currentID)

    def refreshSubForms(self, currentID):
        """Sets match ID for linking models and refreshes models and mappers."""
        self.hometeamModel.setID(currentID)
        self.hometeamModel.refresh()
        
        self.awayteamModel.setID(currentID)
        self.awayteamModel.refresh()
        
        self.homemgrModel.setID(currentID)
        self.homemgrModel.refresh()

        self.awaymgrModel.setID(currentID)
        self.awaymgrModel.refresh()
        
        # go to first record of mapper
        self.hometeamMapper.toFirst()
        self.awayteamMapper.toFirst()
        self.homemgrMapper.toFirst()
        self.awaymgrMapper.toFirst()

    def addRecord(self):
        """Adds new record at end of entry list.
        
        Disables comboboxes and sets focus to Date field.
        
        """
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
        query.exec_(QString("SELECT MAX(match_id) FROM tbl_matches"))
        if query.next():
            maxMatchID= query.value(0).toInt()[0]
            if not maxMatchID:
                match_id = Constants.MinMatchID
            else:
                match_id= QString()
                match_id.setNum(maxMatchID+1)                  
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        
        # assign value to matchID field
        self.matchID_display.setText(match_id)
        
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
        
        # flush filters
        for widget in [self.homeCountryModel, self.homeManagerModel, self.awayCountryModel, self.awayManagerModel]:
            widget.blockSignals(True)
            widget.setFilter(QString())
            widget.blockSignals(False)
        
        # enable form widgets
        self.matchID_display.setEnabled(True)
        self.matchCompSelect.setEnabled(True)
        self.matchRoundSelect.setEnabled(True)
        self.matchDateEdit.setEnabled(True)
        self.matchRefSelect.setEnabled(True)
        self.matchVenueSelect.setEnabled(True)
        self.firstHalfLengthEdit.setEnabled(True)
        self.secondHalfLengthEdit.setEnabled(True)
        self.attendanceEdit.setEnabled(True)
        self.homeconfedSelect.setEnabled(True)
        
        # initialize form widgets
        self.matchRefSelect.setCurrentIndex(-1)
        self.matchVenueSelect.setCurrentIndex(-1)
        self.homeconfedSelect.setCurrentIndex(-1)
        self.homemgrSelect.setCurrentIndex(-1)
        self.hometeamSelect.setCurrentIndex(-1)
        self.awaymgrSelect.setCurrentIndex(-1)
        self.awayteamSelect.setCurrentIndex(-1)
        self.awayconfedSelect.setCurrentIndex(-1)
        
        # disable comboboxes in home/away section
        self.awayconfedSelect.setDisabled(True)
        self.hometeamSelect.setDisabled(True)
        self.homemgrSelect.setDisabled(True)
        self.awayteamSelect.setDisabled(True)
        self.awaymgrSelect.setDisabled(True)
        self.homeLineupButton.setDisabled(True)
        self.awayLineupButton.setDisabled(True)
        self.enviroButton.setDisabled(True)
        
        self.firstHalfLengthEdit.setText("45")
        self.secondHalfLengthEdit.setText("45")
        self.attendanceEdit.setText("0")
        self.matchDateEdit.setFocus()
        
        # refresh subforms
        self.refreshSubForms(match_id)        
        
    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the match record is not being referenced in the Lineups table.
        If it is not being referenced in Lineups, ask for user confirmation and upon pos-
        itive confirmation, delete records in the following order:
            (1) HomeTeams and AwayTeams linking tables
            (2) HomeManagers and AwayManagers linking tables
            (3) WeatherKickoff, WeatherHalftime, and WeatherFulltime linking tables
            (4) Environments table
            (5) Match table
        If match record is being referenced by Lineups, alert user.
        """
        
        childTableList = ["tbl_lineups"]
        fieldName = "match_id"
        match_id = self.matchID_display.text()
        
        if not CountChildRecords(childTableList, fieldName, match_id):
            if QMessageBox.question(self, QString("Delete Record"), 
                                                QString("Delete current record?"), 
                                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                return
            else:
                # delete corresponding records in HomeTeams and AwayTeams 
                self.hometeamModel.delete(match_id)
                self.awayteamModel.delete(match_id)
                
                # delete corresponding records in HomeManagers and AwayManagers
                self.homemgrModel.delete(match_id)
                self.awaymgrModel.delete(match_id)
                
                # find enviro_id in Environments table that contains match_id
                self.deleteEnviroTables(match_id)
                
                # delete record in Match table
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
        editorList = (self.matchDateEdit, self.firstHalfLengthEdit, self.secondHalfLengthEdit, self.attendanceEdit)
        columnList = (MatchEntryDlg.DATE, MatchEntryDlg.HALF1, MatchEntryDlg.HALF2, MatchEntryDlg.ATTEND)
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.text() != self.model.data(index).toString():
                return True
                
        # combobox fields
        editorList = (self.matchCompSelect, self.matchRoundSelect, self.matchRefSelect, self.matchVenueSelect)
        columnList = (MatchEntryDlg.COMP_ID, MatchEntryDlg.ROUND_ID, MatchEntryDlg.REF_ID, MatchEntryDlg.VENUE_ID)
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.currentText() != self.model.data(index).toString():
                return True
                    
        # combobox fields that map to linking tables
        editorList = (self.hometeamSelect, self.homemgrSelect, self.awayteamSelect, self.awaymgrSelect)
        modelList = (self.hometeamModel, self.homemgrModel, self.awayteamModel, self.awaymgrModel)
        for editor, model in zip(editorList, modelList):
            index = model.index(0, 1)
            editIndex = editor.model().index(editor.currentIndex(), 0)
            if editor.model().data(editIndex).toString() != model.data(index).toString():
                return True

        return False                

    def updateConfed(self, confedList, countryList):
        """Updates current index of Confederation combobox.
        
        Ensures consistency between confederation and selected nation in Country combobox.
        
        """
        print "Calling updateConfed()"
        for confedSelect, countrySelect in zip(confedList, countryList):
            if confedSelect.isEnabled():
                confedSelect.blockSignals(True)
                # define underlying model
                countryModel = countrySelect.model()
                
                # look for current index on Country combobox
                # extract confed_id from underlying model
                currIdx = countrySelect.currentIndex()
                currCountry = countrySelect.currentText()
                id = countryModel.record(currIdx).value("confed_id").toString()
        
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
                confedSelect.setCurrentIndex(confedSelect.findText(confedStr, Qt.MatchExactly))
                
                # call filter Country combobox
                # update index of Country combobox to that of currCountry
                self.filterCountryBox(confedSelect, countrySelect)
                countrySelect.setCurrentIndex(countrySelect.findText(currCountry, Qt.MatchExactly))
                confedSelect.blockSignals(False)
     
    def filterCountryBox(self, confedSelect, countrySelect):
        """Enables and filters Country combobox upon selection in Confederation combobox."""
        print "Calling filterCountryBox()"
        
        countrySelect.blockSignals(True)
        
        # define underlying models
        countryModel = countrySelect.model()
        confedModel = confedSelect.model()
        
        # flush filter
        countryModel.setFilter(QString())
        
        # filter tbl_countries based on confederation selection
        currIdx = confedSelect.currentIndex()
        id = confedModel.record(currIdx).value("confed_id").toString()
        countryModel.setFilter(QString("confed_id = %1").arg(id))
        
        countrySelect.blockSignals(False)
        
    def deleteEnviroTables(self, match_id):
        """Deletes environmental conditions tables that reference a specific match.
        
        (1) Find the enviro_id record in Environments that is tied to a specific match (match_id).
        (2) Delete the linking tables associated with enviro_id.
        (3) Delete the enviro_id record in Environments table.
        
        """
        query = QSqlQuery()
        query.prepare("SELECT enviro_id FROM tbl_environments WHERE match_id = ?")
        query.addBindValue(QVariant(match_id))
        query.exec_()
        if query.next():
            enviro_id = query.value(0).toInt()[0]
            
            list = ["tbl_weatherkickoff", "tbl_weatherhalftime", "tbl_weatherfulltime",  "tbl_environments"]
            deletionQuery = QSqlQuery()
            for table in list:
                deletionQuery.prepare("DELETE FROM %1 WHERE enviro_id = ?")
                deletionQuery.addBindValue(QVariant(enviro_id))
                deletionQuery.exec_()
                
    def updateLinkingTable(self, mapper, editor):
        """Updates custom linking table."""
        
        print "Calling updateLinkingTable()"
        # database table associated with mapper
        # get current index of model
        linkmodel = mapper.model()
        index = linkmodel.index(linkmodel.rowCount()-1, 0)
        boxIndex = editor.currentIndex()
        value = editor.model().record(boxIndex).value(0)
        ok = linkmodel.setData(index, value)
        return ok
        
#        print linkmodel.rowCount()
#        print "%d %d" % (index.row(), index.column())
#        # if no entries in model, call setData() directly
#        if not linkmodel.rowCount():
#            index = QModelIndex()
#            boxIndex = editor.currentIndex()
#            value = editor.model().record(boxIndex).value(0)
#            ok = linkmodel.setData(index, value)
#            print ok

    def enableWidget(self, widget):
        """Enables widget passed in function parameter, if not already enabled."""
        print "Call enableWidget()"
        widget.blockSignals(True)
        if not widget.isEnabled():
            widget.setEnabled(True)
        widget.blockSignals(False)
        
    def openEnviros(self, match_id):
        """Opens Environment subdialog for a specific match from Match dialog.
        
        Saves current match record and instantiates EnviroEntryDlg object and opens window.
        Argument: 
        match_id -- primary key of current record in Matches table
        
        """
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
            return
            
        subdialog = EnviroEntryDlg(match_id, self)
        subdialog.exec_()
        self.mapper.setCurrentIndex(row)
        
    def openLineups(self, match_id, teamName):
        """Opens Lineups subdialog for one of the teams in a specific match from Match dialog.
        
        Saves current match record, instantiates LineupEntryDlg object and opens window.
        Arguments: 
        match_id -- primary key of current record in Matches table
        teamName -- team name corresponding to one of the two participants in 
                            current Match record
        
        This method is only allowed to be called when all of the home/away team
        and manager fields have been populated with non-NULL values.
        
        """
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
            return
            
        subdialog = LineupEntryDlg(match_id, teamName, self)
#        print "Match ID: %s" % match_id
#        print "Team Name: %s" % teamName
        subdialog.exec_()
        self.mapper.setCurrentIndex(row)
    
class EnviroEntryDlg(QDialog, ui_enviroentry.Ui_EnviroEntryDlg):
    """Implements environmental conditions data entry dialog, and accesses and writes to Environments table.
    
    This is a subdialog of the environmental conditions of the match -- kickoff time, ambient temperature, 
    weather conditions at kickoff, halftime, and fulltime.
    
    Argument:
    match_id -- primary key of current record in Matches table
    
    """

    ENVIRO_ID,  MATCH_ID,  KICKOFF,  TEMP = range(4)
    
    def __init__(self, match_id, parent=None):
        """Constructor for EnviroEntryDlg class"""
        super(EnviroEntryDlg, self).__init__(parent)
        self.setupUi(self)
#        print "Calling init() in EnviroEntryDlg"
        
        # define local parameters
        WX_COND = KICKOFF_WX = HALFTIME_WX = FULLTIME_WX = 1

        # define underlying database model (tbl_environments)
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_environments")
        self.model.setFilter(QString("match_id = %1").arg(match_id))
        self.model.select()
        
        # if no entry for given table, create one
        # assign new id to enviro_id edit box
        row = self.model.rowCount()
        if not row:
            # get highest enviro_id from entries in table
            query = QSqlQuery()
            query.exec_(QString("SELECT MAX(enviro_id) FROM tbl_environments"))
            if query.next():
                maxEnviroID = query.value(0).toInt()[0]
                if not maxEnviroID:
                    enviro_id = Constants.MinEnviroID
                else:
                    enviro_id= QString()
                    enviro_id.setNum(maxEnviroID+1)
            # insert row into model
            self.model.insertRow(row)
            # assign ID to enviroID display field
            self.enviroID_display.setText(enviro_id)
            
        # assign value to matchID display field
        self.matchID_display.setText(match_id)

        # define mapper for Environments table
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.AutoSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.enviroID_display, EnviroEntryDlg.ENVIRO_ID)
        self.mapper.addMapping(self.matchID_display, EnviroEntryDlg.MATCH_ID)
        self.mapper.addMapping(self.envKOTimeEdit, EnviroEntryDlg.KICKOFF)
        self.mapper.addMapping(self.envKOTempEdit, EnviroEntryDlg.TEMP)
        self.mapper.toFirst()

        # define Weather Conditions table
        weatherModel = QSqlTableModel(self)
        weatherModel.setTable("tbl_weather")
        weatherModel.setSort(WX_COND, Qt.AscendingOrder)
        weatherModel.select()

        # set up Kickoff Weather linking table 
        # set up Kickoff Weather Condition combobox with items from tbl_weather table
        self.kickoffWeatherModel = WeatherLinkingModel("tbl_weatherkickoff", self)
        self.envKOWxSelect.setModel(weatherModel)
        self.envKOWxSelect.setModelColumn(weatherModel.fieldIndex("wx_conditiondesc"))
        self.envKOWxSelect.setCurrentIndex(-1)
        
        # set up Halftime Weather linking table 
        # set up Halftime Weather Condition combobox with items from tbl_weather table
        self.halftimeWeatherModel = WeatherLinkingModel("tbl_weatherhalftime", self)
        self.envHTWxSelect.setModel(weatherModel)
        self.envHTWxSelect.setModelColumn(weatherModel.fieldIndex("wx_conditiondesc"))
        self.envHTWxSelect.setCurrentIndex(-1)
        
        # set up Fulltime Weather linking table 
        # set up Fulltime Weather Condition combobox with items from tbl_weather table
        self.fulltimeWeatherModel = WeatherLinkingModel("tbl_weatherfulltime", self)
        self.envFTWxSelect.setModel(weatherModel)
        self.envFTWxSelect.setModelColumn(weatherModel.fieldIndex("wx_conditiondesc"))
        self.envFTWxSelect.setCurrentIndex(-1)        

        # define mapper for Kickoff Weather Conditions
        self.kickoffWeatherMapper = QDataWidgetMapper(self)
        self.kickoffWeatherMapper.setSubmitPolicy(QDataWidgetMapper.AutoSubmit)
        self.kickoffWeatherMapper.setModel(self.kickoffWeatherModel)
        kickoffWeatherDelegate = GenericDelegate(self)
        kickoffWeatherDelegate.insertColumnDelegate(KICKOFF_WX, WeatherComboBoxDelegate(self))
        self.kickoffWeatherMapper.setItemDelegate(kickoffWeatherDelegate)
        self.kickoffWeatherMapper.addMapping(self.envKOWxSelect, KICKOFF_WX)
        self.kickoffWeatherMapper.toFirst()
        
        # define mapper for Halftime Weather Conditions
        self.halftimeWeatherMapper = QDataWidgetMapper(self)
        self.halftimeWeatherMapper.setSubmitPolicy(QDataWidgetMapper.AutoSubmit)
        self.halftimeWeatherMapper.setModel(self.halftimeWeatherModel)
        halftimeWeatherDelegate = GenericDelegate(self)
        halftimeWeatherDelegate.insertColumnDelegate(HALFTIME_WX, WeatherComboBoxDelegate(self))
        self.halftimeWeatherMapper.setItemDelegate(halftimeWeatherDelegate)
        self.halftimeWeatherMapper.addMapping(self.envHTWxSelect, HALFTIME_WX)
        self.halftimeWeatherMapper.toFirst()
        
        # define mapper for Fulltime Weather Conditions
        self.fulltimeWeatherMapper = QDataWidgetMapper(self)
        self.fulltimeWeatherMapper.setSubmitPolicy(QDataWidgetMapper.AutoSubmit)
        self.fulltimeWeatherMapper.setModel(self.fulltimeWeatherModel)
        fulltimeWeatherDelegate = GenericDelegate(self)
        fulltimeWeatherDelegate.insertColumnDelegate(FULLTIME_WX, WeatherComboBoxDelegate(self))
        self.fulltimeWeatherMapper.setItemDelegate(fulltimeWeatherDelegate)
        self.fulltimeWeatherMapper.addMapping(self.envFTWxSelect, FULLTIME_WX)
        self.fulltimeWeatherMapper.toFirst()

        # configure signal/slot
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        self.connect(self.envKOWxSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.updateLinkingTable(self.kickoffWeatherMapper, self.envKOWxSelect))
        self.connect(self.envHTWxSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.updateLinkingTable(self.halftimeWeatherMapper, self.envHTWxSelect))
        self.connect(self.envFTWxSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.updateLinkingTable(self.fulltimeWeatherMapper, self.envFTWxSelect))
        
    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if MsgPrompts.SaveDiscardOptionPrompt(self):
                if not self.mapper.submit():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)

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
        editorList = (self.envKOTimeEdit, self.envKOTempEdit)
        columnList = (EnviroEntryDlg.KICKOFF, EnviroEntryDlg.TEMP)
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.text() != self.model.data(index).toString():
                return True
                
        # combobox fields that map to linking tables
        editorList = (self.envKOWxSelect, self.envHTWxSelect, self.envFTWxSelect)   
        modelList = (self.kickoffWeatherModel, self.halftimeWeatherModel, self.fulltimeWeatherModel)
        for editor, model in zip(editorList, modelList):
            index = model.index(0, 1)
            if editor.currentText() != model.data(index).toString():
                return True

        return False                

    def updateLinkingTable(self, mapper, editor):
        """Updates current record or inserts new record in custom linking table.
        
        Arguments:
        mapper -- mapper object associated with data widget and data model
        editor -- data widget object
        """
#        print "Calling updateLinkingTable()"
        # database table associated with mapper
        # get current index of model
        linkmodel = mapper.model()
        index = linkmodel.index(linkmodel.rowCount()-1, 0)
        
        # if no entries in model, call setData() directly
        if not linkmodel.rowCount():
            boxIndex = editor.currentIndex()
            value = editor.model().record(boxIndex).value(0)
            ok = linkmodel.setData(index, value)
