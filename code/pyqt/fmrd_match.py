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
    
    ID,  DATE, HALF1, HALF2, COMP_ID, ROUND_ID, VENUE_ID, REF_ID = range(8)
    
    def __init__(self, parent=None):
        """Constructor for MatchEntryDlg class."""
        super(MatchEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define local parameters
        HOME_ID = AWAY_ID = 1
        CMP_ID,  COMP_NAME = range(2)
        RND_ID,  ROUND_NAME = range(2)
        VEN_ID,  VENUE_NAME = range(2)
        RF_ID,  REF_NAME,  REF_SORT = range(3)
        TM_ID,  TEAM_NAME = range(2)
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
        self.mapper.addMapping(self.matchCompSelect, MatchEntryDlg.COMP_ID)
        
        # relation model for Rounds combobox
        self.roundModel = self.model.relationModel(MatchEntryDlg.ROUND_ID)
        self.roundModel.setSort(RND_ID, Qt.AscendingOrder)
        self.matchRoundSelect.setModel(self.roundModel)
        self.matchRoundSelect.setModelColumn(self.roundModel.fieldIndex("round_desc"))
        self.mapper.addMapping(self.matchRoundSelect, MatchEntryDlg.ROUND_ID)
        
        # relation model for Venues combobox
        self.venueModel = self.model.relationModel(MatchEntryDlg.VENUE_ID)
        self.venueModel.setSort(VEN_ID, Qt.AscendingOrder)
        self.matchVenueSelect.setModel(self.venueModel)
        self.matchVenueSelect.setModelColumn(self.venueModel.fieldIndex("ven_name"))
        self.mapper.addMapping(self.matchVenueSelect, MatchEntryDlg.VENUE_ID)
        
        # relation model for Referees combobox
        self.refereeModel = self.model.relationModel(MatchEntryDlg.REF_ID)
        self.refereeModel.setSort(REF_SORT, Qt.AscendingOrder)
        self.matchRefSelect.setModel(self.refereeModel)
        self.matchRefSelect.setModelColumn(self.refereeModel.fieldIndex("full_name"))
        self.mapper.addMapping(self.matchRefSelect, MatchEntryDlg.REF_ID)        

        # map other widgets on form
        self.mapper.addMapping(self.matchID_display, MatchEntryDlg.ID)
        self.mapper.addMapping(self.matchDateEdit, MatchEntryDlg.DATE)
        self.mapper.addMapping(self.firstHalfLengthEdit, MatchEntryDlg.HALF1)
        self.mapper.addMapping(self.secondHalfLengthEdit, MatchEntryDlg.HALF2)
        self.mapper.toFirst()
        
        # define models used in Team and Manager comboboxes
        # we need multiple instantiations of Teams and Managers tables
        # so that there is no confusion in SQL logic
        
        homeTeamModel = QSqlTableModel(self)
        homeTeamModel.setTable("tbl_teams")
        homeTeamModel.setSort(TEAM_NAME, Qt.AscendingOrder)
        homeTeamModel.select()
        
        awayTeamModel = QSqlTableModel(self)
        awayTeamModel.setTable("tbl_teams")
        awayTeamModel.setSort(TEAM_NAME, Qt.AscendingOrder)
        awayTeamModel.select()

        homeManagerModel = QSqlTableModel(self)
        homeManagerModel.setTable("managers_list")
        homeManagerModel.setSort(MGR_SORT, Qt.AscendingOrder)
        homeManagerModel.select()
        
        awayManagerModel = QSqlTableModel(self)
        awayManagerModel.setTable("managers_list")
        awayManagerModel.setSort(MGR_SORT, Qt.AscendingOrder)
        awayManagerModel.select()
        
        # set up Home Team linking table 
        # set up Home Team combobox with items from tbl_teams table
        self.hometeamModel = TeamLinkingModel("tbl_hometeams", self)
        self.hometeamSelect.setModel(homeTeamModel)
        self.hometeamSelect.setModelColumn(homeTeamModel.fieldIndex("tm_name"))
        self.hometeamSelect.setCurrentIndex(-1)

        # set up Away Team linking table
        # set up Away Team combobox with items from tbl_teams table
        self.awayteamModel = TeamLinkingModel("tbl_awayteams", self)
        self.awayteamSelect.setModel(awayTeamModel)
        self.awayteamSelect.setModelColumn(awayTeamModel.fieldIndex("tm_name"))
        self.awayteamSelect.setCurrentIndex(-1)

        # set up Home Manager linking table
        # set up Home Manager combobox with items from managers_list table
        self.homemgrModel = ManagerLinkingModel("tbl_homemanagers", self)
        self.homemgrSelect.setModel(homeManagerModel)
        self.homemgrSelect.setModelColumn(homeManagerModel.fieldIndex("full_name"))
        self.homemgrSelect.setCurrentIndex(-1)

        # set up Away Manager linking table
        # set up Away Manager combobox with items from managers_list table
        self.awaymgrModel = ManagerLinkingModel("tbl_awaymanagers", self)
        self.awaymgrSelect.setModel(awayManagerModel)
        self.awaymgrSelect.setModelColumn(awayManagerModel.fieldIndex("full_name"))
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
              
        # disable buttons depending on number of records in tbl_matches
        if self.model.rowCount() <= 1:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
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
        self.connect(self.closeButton, SIGNAL("clicked()"), self, SLOT("close()"))

        self.connect(self.hometeamSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.enableWidget(self.awayteamSelect))
        self.connect(self.homemgrSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                     lambda: self.enableWidget(self.homeLineupButton))
        self.connect(self.awayteamSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.enableWidget(self.awaymgrSelect))
        self.connect(self.awaymgrSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                     lambda: self.enableWidget(self.awayLineupButton))

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
        confirm = MsgPrompts.SaveDiscardOptionPrompt(self)
        if confirm:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
    
    def saveRecord(self, where):
        """"Submits changes to database, navigates through form, and resets subforms."""
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
        self.homemgrModel.refresh()
        
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
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
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
        
        # disable navigation button
        self.lastEntry.setDisabled(True)
        self.nextEntry.setDisabled(True)
        if row >= 1:
            self.prevEntry.setEnabled(True)
            self.firstEntry.setEnabled(True)
        
        # disable comboboxes in home/away team section
        self.homemgrSelect.setDisabled(True)
        self.awayteamSelect.setDisabled(True)
        self.awaymgrSelect.setDisabled(True)
        self.homeLineupButton.setDisabled(True)
        self.awayLineupButton.setDisabled(True)
        
        # set default values to:
        #   1st/2nd half length widgets
        #   match date
        self.firstHalfLengthEdit.setText("45")
        self.secondHalfLengthEdit.setText("45")
        self.matchDateEdit.setText("1901-01-01")
        
        # set focus on match date entry
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
        else:
                DeletionErrorPrompt(self)

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
        
#        print "Calling updateLinkingTable()"
        # database table associated with mapper
        # get current index of model
        linkmodel = mapper.model()
        index = linkmodel.index(linkmodel.rowCount()-1, 0)
        
        # if no entries in model, call setData() directly
        if not linkmodel.rowCount():
            index = QModelIndex()
            boxIndex = editor.currentIndex()
            value = editor.model().record(boxIndex).value(0)
            ok = linkmodel.setData(index, value)

    def enableWidget(self, widget):
        """Enables widget passed in function parameter, if not already enabled."""
        if not widget.isEnabled():
            widget.setEnabled(True)
        
    def openEnviros(self, match_id):
        """Opens Environment subdialog for a specific match from Match dialog.
        
        Saves current match record and instantiates EnviroEntryDlg object and opens window.
        Argument: 
        match_id -- primary key of current record in Matches table
        
        """
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
            return
            
        subdialog = EnviroEntryDlg(match_id, self)
        subdialog.exec_()
        
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
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
            return
            
        subdialog = LineupEntryDlg(match_id, teamName, self)
#        print "Match ID: %s" % match_id
#        print "Team Name: %s" % teamName
        subdialog.exec_()
    
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
        confirm = MsgPrompts.SaveDiscardOptionPrompt(self)
        if confirm:
            if not self.mapper.submit():
                MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
        
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


