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

"""Contains OffenseEntryDlg class that implements disciplinary entry forms to Offense table of FMRD. """

class OffenseEntryDlg(QDialog, ui_offenseentry.Ui_OffenseEntryDlg):
    """Implements bookable offense data entry dialog, and accesses and writes to Offenses table.
    
    This dialog accepts data on disciplinary incidents during a match.
   """

    ID, LINEUP_ID, FOUL_ID, CARD_ID, TIME, STIME = range(6)

    def __init__(self, parent=None):
        """Constructor for OffenseEntryDlg class."""
        super(OffenseEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        CMP_ID = RND_ID = TM_ID = 0
        MATCHDAY_NAME= TEAM = FOUL = CARD = 1
        SORT_NAME = 4

        CMP_ID,  COMP_NAME = range(2)
        PHS_ID,  PHASE_NAME = range(2)
        RND_ID,  ROUND_NAME = range(2)
        GRP_ID,  GROUP_NAME = range(2)
        
        GROUP_ROUND,  GROUP,  GROUP_MATCHDAY = range(1, 4)
        KO_ROUND, KO_MATCHDAY = range(1, 3)

        # define lists of comboboxes
        self.selectWidgets = (
            self.compSelect, self.phaseSelect, self.lgRoundSelect, self.groupSelect, self.grpRoundSelect, 
            self.grpMatchdaySelect, self.koRoundSelect, self.koMatchdaySelect, self.matchSelect, 
            self.teamSelect, self.playerSelect, self.foulSelect, self.cardSelect
        )
        
        self.upperFormWidgets = (
            self.compSelect, self.phaseSelect
        )
        
        self.lowerFormWidgets = (
            self.playerSelect, self.foulSelect, self.cardSelect, self.foultimeEdit
        )
        
        self.phaseWidgets = (
            self.lgRoundSelect, self.koRoundSelect, self.koMatchdaySelect, self.groupSelect, 
            self.grpRoundSelect, self.grpMatchdaySelect                             
        )

        #
        # Define comboboxes used to filter Offense table
        # Ensure that user only sees Offenses for specific match
        #
        
        # Competition combobox
        self.compModel = QSqlTableModel(self)
        self.compModel.setTable("tbl_competitions")
        self.compModel.setSort(CMP_ID, Qt.AscendingOrder)
        self.compModel.select()
        self.compSelect.setModel(self.compModel)
        self.compSelect.setModelColumn(self.compModel.fieldIndex("comp_name"))
        self.compSelect.setCurrentIndex(-1)
        
        # Competition Phases combobox
        self.phaseModel = QSqlTableModel(self)
        self.phaseModel.setTable("tbl_phases")
        self.phaseModel.setSort(PHS_ID, Qt.AscendingOrder)
        self.phaseModel.select()
        self.phaseSelect.setModel(self.phaseModel)
        self.phaseSelect.setModelColumn(self.phaseModel.fieldIndex("phase_desc"))
        self.phaseSelect.setCurrentIndex(-1)

        #
        # define comboboxes used for League matches
        #
        
        # League Rounds
        leagueRoundModel = QSqlTableModel(self)
        leagueRoundModel.setTable("tbl_rounds")
        leagueRoundModel.setSort(ROUND_NAME, Qt.AscendingOrder)
        leagueRoundModel.select()
        self.lgRoundSelect.setModel(leagueRoundModel)
        self.lgRoundSelect.setModelColumn(leagueRoundModel.fieldIndex("round_desc"))
        self.lgRoundSelect.setCurrentIndex(-1)
        
        #
        # define comboboxes used for Group matches
        #
        
        # Group Rounds
        groupRoundModel = QSqlTableModel(self)
        groupRoundModel.setTable("tbl_grouprounds")
        groupRoundModel.setSort(RND_ID, Qt.AscendingOrder)
        groupRoundModel.select()
        self.grpRoundSelect.setModel(groupRoundModel)
        self.grpRoundSelect.setModelColumn(groupRoundModel.fieldIndex("grpround_desc"))
        self.grpRoundSelect.setCurrentIndex(-1)
        
        # Groups
        groupNameModel = QSqlTableModel(self)
        groupNameModel.setTable("tbl_groups")
        groupNameModel.setSort(GROUP_NAME, Qt.AscendingOrder)
        groupNameModel.select()
        self.groupSelect.setModel(groupNameModel)
        self.groupSelect.setModelColumn(groupNameModel.fieldIndex("group_desc"))
        self.groupSelect.setCurrentIndex(-1)
        
        # Matchdays
        groupMatchdayModel = QSqlTableModel(self)
        groupMatchdayModel.setTable("tbl_rounds")
        groupMatchdayModel.setSort(ROUND_NAME, Qt.AscendingOrder)
        groupMatchdayModel.select()
        self.grpMatchdaySelect.setModel(groupMatchdayModel)
        self.grpMatchdaySelect.setModelColumn(groupMatchdayModel.fieldIndex("round_desc"))
        self.grpMatchdaySelect.setCurrentIndex(-1)
                
        #
        # define models used for Knockout matches
        #

        # Knockout Rounds
        knockoutRoundModel = QSqlTableModel(self)
        knockoutRoundModel.setTable("tbl_knockoutrounds")
        knockoutRoundModel.setSort(RND_ID, Qt.AscendingOrder)
        knockoutRoundModel.select()
        self.koRoundSelect.setModel(knockoutRoundModel)
        self.koRoundSelect.setModelColumn(knockoutRoundModel.fieldIndex("koround_desc"))
        self.koRoundSelect.setCurrentIndex(-1)
        
        # Matchdays (Knockout phase)
        knockoutMatchdayModel = QSqlTableModel(self)
        knockoutMatchdayModel.setTable("tbl_matchdays")
        knockoutMatchdayModel.setSort(MATCHDAY_NAME, Qt.AscendingOrder)
        knockoutMatchdayModel.select()
        self.koMatchdaySelect.setModel(knockoutMatchdayModel)
        self.koMatchdaySelect.setModelColumn(knockoutMatchdayModel.fieldIndex("matchday_desc"))
        self.koMatchdaySelect.setCurrentIndex(-1)
        
        #
        # Define Team combobox used to filter Lineup table
        # Ensure that user only sees Players for specific match and team
        #
        
        # Team combobox
        self.teamModel = QSqlTableModel(self)
        self.teamModel.setTable("tbl_teams")
        self.teamModel.setSort(TEAM,  Qt.AscendingOrder)
        self.teamModel.select()
        self.teamSelect.setModel(self.teamModel)
        self.teamSelect.setModelColumn(self.teamModel.fieldIndex("tm_name"))
        self.teamSelect.setCurrentIndex(-1)        
        
        #
        # Define Team combobox used to filter Lineup table
        # Ensure that user only sees Players for specific match and team
        #
        
        # Team combobox
        self.teamModel = QSqlTableModel(self)
        self.teamModel.setTable("tbl_teams")
        self.teamModel.setSort(TEAM,  Qt.AscendingOrder)
        self.teamModel.select()
        self.teamSelect.setModel(self.teamModel)
        self.teamSelect.setModelColumn(self.teamModel.fieldIndex("tm_name"))
        self.teamSelect.setCurrentIndex(-1)        
        
        #
        # Match combobox
        # Instantiate an object here, specific details will
        # be set upon selection of Competition Phase
        #
        
        self.matchModel = QSqlTableModel(self)
        
        #
        # Define Offenses data entry
        #
        
        # 
        # underlying database model (tbl_offenses)
        # because of foreign keys, instantiate QSqlRelationalTableModel and define relations to it        
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_offenses")
        self.model.setRelation(OffenseEntryDlg.LINEUP_ID, QSqlRelation("lineup_list", "lineup_id", "player"))
        self.model.setRelation(OffenseEntryDlg.FOUL_ID, QSqlRelation("tbl_fouls", "foul_id", "foul_desc"))
        self.model.setRelation(OffenseEntryDlg.CARD_ID, QSqlRelation("tbl_cards", "card_id", "card_type"))
        self.model.setSort(OffenseEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        foulDelegate = GenericDelegate(self)
        foulDelegate.insertColumnDelegate(OffenseEntryDlg.LINEUP_ID, EventPlayerComboBoxDelegate(self))
        self.mapper.setItemDelegate(foulDelegate)        

        # set up Player combobox
        self.playerModel = self.model.relationModel(OffenseEntryDlg.LINEUP_ID)
        self.playerModel.setSort(SORT_NAME,  Qt.AscendingOrder)
        self.playerSelect.setModel(self.playerModel)
        self.playerSelect.setModelColumn(self.playerModel.fieldIndex("player"))
        self.playerSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.playerSelect, OffenseEntryDlg.LINEUP_ID)

        # relation model for Foul combobox
        self.foulModel = self.model.relationModel(OffenseEntryDlg.FOUL_ID)
        self.foulModel.setSort(FOUL, Qt.AscendingOrder)
        self.foulSelect.setModel(self.foulModel)
        self.foulSelect.setModelColumn(self.foulModel.fieldIndex("foul_desc"))
        self.foulSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.foulSelect, OffenseEntryDlg.FOUL_ID)        
        
        # relation model for Card combobox
        self.cardModel = self.model.relationModel(OffenseEntryDlg.CARD_ID)
        self.cardModel.setSort(CARD, Qt.AscendingOrder)
        self.cardSelect.setModel(self.cardModel)
        self.cardSelect.setModelColumn(self.cardModel.fieldIndex("card_type"))
        self.cardSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.cardSelect, OffenseEntryDlg.CARD_ID)        

        # map other widgets on form
        self.mapper.addMapping(self.offenseID_display, OffenseEntryDlg.ID)
        self.mapper.addMapping(self.foultimeEdit, OffenseEntryDlg.TIME)
        self.mapper.addMapping(self.stoppageEdit, OffenseEntryDlg.STIME)
        
        #
        # Disable data entry boxes
        #
        
        # disable all comboboxes and line edits 
        # EXCEPT competition combobox upon opening
        
        self.phaseSelect.setDisabled(True)
        
        # disable phase-related widgets
        for widget in self.phaseWidgets:
            widget.setDisabled(True)
        
        self.matchSelect.setDisabled(True)
        self.teamSelect.setDisabled(True)
        
        # disable remaining form widgets
        for widget in self.lowerFormWidgets:
            widget.setDisabled(True)
            
        self.stoppageEdit.setDisabled(True)

        # disable navigation buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        
        # disable add,save, and delete entry buttons
        self.addEntry.setDisabled(True)
        self.saveEntry.setDisabled(True)
        self.deleteEntry.setDisabled(True)
        
        #
        # Signals/Slots configuration
        #
        
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.LAST))
        self.connect(self.saveEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NULL))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)        
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        
        self.connect(self.compSelect, SIGNAL("currentIndexChanged(int)"), lambda: self.enableWidget(self.phaseSelect))
        self.connect(self.phaseSelect, SIGNAL("currentIndexChanged(int)"), self.enablePhaseDetails)
        
        self.connect(self.lgRoundSelect, SIGNAL("currentIndexChanged(int)"), self.enableAndFilterMatches)
        
        self.connect(self.grpRoundSelect, SIGNAL("currentIndexChanged(int)"), self.enableAndFilterGroups)
        self.connect(self.groupSelect, SIGNAL("currentIndexChanged(int)"), self.enableAndFilterMatchdays)
        self.connect(self.grpMatchdaySelect, SIGNAL("currentIndexChanged(int)"), self.enableAndFilterMatches)

        self.connect(self.koRoundSelect, SIGNAL("currentIndexChanged(int)"), self.enableAndFilterMatchdays)
        self.connect(self.koMatchdaySelect, SIGNAL("currentIndexChanged(int)"), self.enableAndFilterMatches)
        
        self.connect(self.matchSelect, SIGNAL("currentIndexChanged(int)"), self.filterOffensesAndTeams)
        self.connect(self.teamSelect, SIGNAL("currentIndexChanged(int)"), self.filterPlayers)
        self.connect(self.foultimeEdit, SIGNAL("editingFinished()"),  lambda: self.enableStoppageTime(self.stoppageEdit))

    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if MsgPrompts.SaveDiscardOptionPrompt(self):
                if not self.mapper.submit():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
   
    def saveRecord(self, where):
        """Submits changes to database, navigates through form, and resets subforms."""
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
            
        self.teamSelect.blockSignals(True)    
        self.mapper.setCurrentIndex(row)
        self.refreshTeamBox()
        self.teamSelect.blockSignals(False)
        
        # enable stoppage time field if there is an entry
        if self.stoppageEdit.text() == "0":
            self.stoppageEdit.setEnabled(False)
        else:
            self.stoppageEdit.setEnabled(True)                

    def deleteRecord(self):
        """Deletes record from database upon user confirmation."""
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        row = self.mapper.currentIndex()
        self.model.removeRow(row)
        if not self.model.submitAll():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
            return
        if row + 1 >= self.model.rowCount():
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row) 
        
        # disable buttons and no widgets if no records in database
        if not self.model.rowCount():
            self.deleteEntry.setDisabled(True)
            self.saveEntry.setDisabled(True)
            for widget in self.selectWidgets:
                widget.setDisabled(True)
                widget.setCurrentIndex(-1)
            self.foultimeEdit.setText(QString())
            self.stoppageEdit.setText("0")
        else:
            self.teamSelect.blockSignals(True)
            self.refreshTeamBox()
            self.teamSelect.blockSignals(False)
        
        # enable stoppage time field if there is an entry
        if self.stoppageEdit.text() == "0":
            self.stoppageEdit.setEnabled(False)
        else:
            self.stoppageEdit.setEnabled(True)        
        
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
        editorList = (self.foultimeEdit, self.stoppageEdit)
        columnList = (OffenseEntryDlg.TIME, OffenseEntryDlg.STIME)
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.text() != self.model.data(index).toString():
                return True
                
        # combobox fields
        editorList = (self.playerSelect, self.foulSelect, self.cardSelect)
        columnList = (OffenseEntryDlg.LINEUP_ID, OffenseEntryDlg.FOUL_ID, OffenseEntryDlg.CARD_ID)
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.currentText() != self.model.data(index).toString():
                return True
                    
        return False        

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
        query.exec_(QString("SELECT MAX(offense_id) FROM tbl_offenses"))
        if query.next():
            maxOffenseID = query.value(0).toInt()[0]
            if not maxOffenseID:
                offense_id = Constants.MinOffenseID
            else:
                offense_id = QString()
                offense_id.setNum(maxOffenseID+1)       
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to goalID field
        self.offenseID_display.setText(offense_id)
        
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
        self.enableWidget(self.saveEntry)
        # enable Team combobox
        self.enableWidget(self.teamSelect)
        
        # disable lower part of form
        for widget in self.lowerFormWidgets:
            widget.setDisabled(True)
        self.stoppageEdit.setDisabled(True)
        # reset indices of lower comboboxes
        for widget in (self.teamSelect, self.playerSelect, self.foulSelect):
            widget.setCurrentIndex(-1)
        
        # set default stoppage time, clear match time
        self.stoppageEdit.setText("0")
        self.foultimeEdit.setText(QString())

    def refreshTeamBox(self):
        """Sets index of team box so that it corresponds with selected player."""
        
        compName = self.compSelect.currentText()
        phaseText = self.phaseSelect.currentText()
        playerName = self.playerSelect.currentText()
        
        # look for team name
        query = QSqlQuery()
        query.prepare("SELECT team FROM lineup_list WHERE player = ? AND "
                               "matchup IN (SELECT matchup FROM match_list WHERE competition = ? AND phase = ?)")
        query.addBindValue(QVariant(playerName))
        query.addBindValue(QVariant(compName))
        query.addBindValue(QVariant(phaseText))
        query.exec_()
        if query.next():
            teamName = query.value(0).toString()
        else:
            teamName = "-1"
                        
        currentIndex = self.teamSelect.findText(teamName, Qt.MatchExactly)
        self.teamSelect.setCurrentIndex(currentIndex)

    def filterPlayers(self):
        """Filters Players combobox down to players in match lineup for selected team, and enable remaining data widgets."""
        
        self.playerSelect.blockSignals(True)
        
        lineupListModel = self.playerSelect.model()
        lineupListModel.setFilter(QString())
        
        # get current matchup
        matchup = self.matchSelect.currentText()
                
        # get match_id by making a query on match_list with matchup
        query = QSqlQuery()
        query.prepare("SELECT match_id FROM match_list WHERE matchup = ?")
        query.addBindValue(QVariant(matchup))
        query.exec_()
        if query.next():
            match_id = query.value(0).toString()
        
        # get current team
        teamName = self.teamSelect.currentText()
        
        # get team_id by querying tbl_teams with team name
        team_id = "-1"
        query = QSqlQuery()
        query.prepare("SELECT team_id FROM tbl_teams WHERE tm_name = ?")
        query.addBindValue(QVariant(teamName))
        query.exec_()
        if query.next():
            team_id = query.value(0).toString()
        
        # filter lineup list model by match_id
        lineupListModel.setFilter(QString("lineup_id IN "
                                                          "(SELECT lineup_id FROM tbl_lineups WHERE match_id = %1 AND team_id = %2)").arg(match_id, team_id))
                
        # enable remaining comboboxes on form
        for widget in (self.playerSelect, self.foulSelect,  self.cardSelect, self.foultimeEdit):
            widget.setEnabled(True)
        # enable stoppage time field if there is an entry
        if self.stoppageEdit.text() == "0":
            self.stoppageEdit.setEnabled(False)
        else:
            self.stoppageEdit.setEnabled(True)        
        
        # set current index to -1
        self.playerSelect.setCurrentIndex(-1)        
        self.playerSelect.blockSignals(False)

    def filterOffensesAndTeams(self):
        """Filters Offenses table down to entries from selected match, and filters Teams combobox down to both participants."""
        
        # block signals from team combobox
        self.teamSelect.blockSignals(True)
        
        # clear filter
        self.model.setFilter(QString())
        
        # get current index
        currentIndex = self.matchSelect.currentIndex()
        
        # get match_id
        match_id = self.matchModel.record(currentIndex).value("match_id").toString()
        
        # filter penalties taken by players who were in lineup for match (match_id)
        self.model.setFilter(QString("tbl_offenses.lineup_id IN (SELECT lineup_id FROM lineup_list WHERE matchup IN "
                                                    "(SELECT matchup FROM match_list WHERE match_id = %1))").arg(match_id))
        self.mapper.toFirst()        
        
        # filter teams involved in match
        teamModel = self.teamSelect.model()
        teamModel.setFilter(QString())
        teamModel.setFilter(QString("team_id IN"
            "(SELECT team_id FROM tbl_hometeams WHERE match_id = %1"
            "UNION SELECT team_id FROM tbl_awayteams WHERE match_id = %1)").arg(match_id))
            
        self.teamSelect.setCurrentIndex(-1)            
        
        # refresh team select box
        self.refreshTeamBox()

        # unblock signals from team combobox
        self.teamSelect.blockSignals(False)

        # enable Add button
        self.addEntry.setEnabled(True)
        
        # if table is not empty
        if self.model.rowCount():
            # enable Save/Delete buttons
            self.saveEntry.setEnabled(True)
            self.deleteEntry.setEnabled(True)
            # enable data entry widgets on lower part of form
            self.enableWidget(self.teamSelect)
            for widget in self.lowerFormWidgets:
                widget.setEnabled(True)
            if self.stoppageEdit.text() == "0":
                self.stoppageEdit.setEnabled(False)
            else:
                self.stoppageEdit.setEnabled(True)
            # enable navigation buttons
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if self.model.rowCount() > 1:
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)        

    def enableWidget(self, widget):
        """Enables widget passed in function parameter, if not already enabled."""
        if not widget.isEnabled():
            widget.setEnabled(True)
        
    def enablePhaseDetails(self):
        """Enables comboboxes associated with specific competition phase.
        
        Sets validator for match time edit field.
        Filters League/Group/Knockout Rounds combobox.
        """
        for widget in self.phaseWidgets:
            widget.setCurrentIndex(-1)
            
        phaseText = self.phaseSelect.currentText()
        if phaseText == "League":
            self.lgRoundSelect.setEnabled(True)
            self.foultimeEdit.setValidator(QIntValidator(0, Constants.MAX_MINUTES, self))
        elif phaseText == "Group":
            self.grpRoundSelect.setEnabled(True)
            self.foultimeEdit.setValidator(QIntValidator(0, Constants.MAX_MINUTES, self))
        elif phaseText == "Knockout":
            self.koRoundSelect.setEnabled(True)
            self.foultimeEdit.setValidator(QIntValidator(0, Constants.MAX_KO_MINUTES, self))
        self.filterRounds(phaseText)
 
    def filterRounds(self, phaseText):
        """Enables Rounds combobox and filters its contents based on Competition and Competition Phase selections.
        
        Argument:
        phaseText -- name of selected Competition Phase (phaseSelect)
        """
        # Competitions model
        compModel = self.compModel
        # get text from current index of Competition combobox
        compName = self.compSelect.currentText()
        
        if phaseText == "League":
            self.lgRoundSelect.blockSignals(True)
            
            # model associated with combobox
            boxModel = self.lgRoundSelect.model()
            # clear filter for combobox model
            boxModel.setFilter(QString())
            # filter combobox model on competition name using league_match_list table
            # therefore we only access matchdays currently entered in database
            boxModel.setFilter(QString("round_desc IN "
                    "(SELECT round FROM league_match_list WHERE competition = '%1')").arg(compName))
            # set current index of widget to -1
            self.lgRoundSelect.setCurrentIndex(-1)
            
            self.lgRoundSelect.blockSignals(False)
        elif phaseText == "Group":
            self.grpRoundSelect.blockSignals(True)
            
            # model associated with combobox
            boxModel = self.grpRoundSelect.model()
            # clear filter for combobox model
            boxModel.setFilter(QString())
            # filter combobox model on competition name using group_match_list table
            # therefore we only access rounds currently entered in database
            boxModel.setFilter(QString("grpround_desc IN "
                    "(SELECT round FROM group_match_list WHERE competition = '%1')").arg(compName))
            # set current index of widget to -1
            self.grpRoundSelect.setCurrentIndex(-1)
            
            self.grpRoundSelect.blockSignals(False)
        elif phaseText == "Knockout":
            self.koRoundSelect.blockSignals(True)
            
            # model associated with combobox
            boxModel = self.koRoundSelect.model()
            # clear filter for combobox model
            boxModel.setFilter(QString())
            # filter combobox model on competition name using knockout_match_list table
            # therefore we only access rounds currently entered in database
            boxModel.setFilter(QString("koround_desc IN "
                    "(SELECT round FROM knockout_match_list WHERE competition = '%1')").arg(compName))
            # set current index of widget to -1
            self.koRoundSelect.setCurrentIndex(-1)
            
            self.koRoundSelect.blockSignals(False)
    
    def enableAndFilterGroups(self):
        """Enables Groups combobox and filters its contents based on selections in Competition Phase, Group Round fields."""
        self.groupSelect.blockSignals(True)
        
        # Enable group combobox
        self.enableWidget(self.groupSelect)
        # Competition model
        compModel = self.compModel
        # get text from current index of Competition combobox
        compName = self.compSelect.currentText()
        # Group round name
        roundName = self.grpRoundSelect.currentText()
        # model associated with combobox
        boxModel = self.groupSelect.model()
        # clear filter for combobox model
        boxModel.setFilter(QString())
        # filter combobox model on competition and round names using group_match_list table
        # therefore we only access groups currently entered in database
        boxModel.setFilter(QString("group_desc IN "
                "(SELECT group_name FROM group_match_list WHERE competition = '%1' AND round = '%2')").arg(compName, roundName))
        self.groupSelect.setCurrentIndex(-1)
        
        self.groupSelect.blockSignals(False)
        
    def enableAndFilterMatchdays(self):
        """Enables Matchdays combobox and filters its contents based on selections in Competition Phase and Knockout/Group fields."""
        
        # Competition model
        compModel = self.compModel
        # get text from current index of Competition combobox
        compName = self.compSelect.currentText()
        
        phaseText = self.phaseSelect.currentText()
        if phaseText == "Group":
            self.grpMatchdaySelect.blockSignals(True)
            
            # Activate matchday widget
            self.enableWidget(self.grpMatchdaySelect)
            # Group round name
            roundName = self.grpRoundSelect.currentText()
            # Group name
            groupName = self.groupSelect.currentText()
            # model associated with combobox
            boxModel = self.grpMatchdaySelect.model()
            # clear filter for combobox model
            boxModel.setFilter(QString())
            # filter combobox model on competition, round, and group names using group_match_list table
            # therefore we only access matchdays currently entered in database
            boxModel.setFilter(QString("round_desc IN (SELECT matchday FROM group_match_list WHERE \
                    competition = '%1' AND round = '%2' AND group_name = '%3')").arg(compName, roundName, groupName))
            self.grpMatchdaySelect.setCurrentIndex(-1)
            
            self.grpMatchdaySelect.blockSignals(False)
        elif phaseText == "Knockout":
            self.koMatchdaySelect.blockSignals(True)
            
            # Activate matchday widget
            self.enableWidget(self.koMatchdaySelect)
            # Knockout round name
            roundName = self.koRoundSelect.currentText()
            # model associated with combobox
            boxModel = self.koMatchdaySelect.model()
            # clear filter for combobox model
            boxModel.setFilter(QString())
            # filter combobox model on competition and round names using knockout_match_list table
            # therefore we only access matchdays currently entered in database
            boxModel.setFilter(QString("matchday_desc IN (SELECT game FROM knockout_match_list WHERE \
                    competition = '%1' AND round = '%2')").arg(compName, roundName))
            self.koMatchdaySelect.setCurrentIndex(-1)
            
            self.koMatchdaySelect.blockSignals(False)
        
    def enableAndFilterMatches(self):
        """Enables Match combobox and filters its contents based on selections in Competition Phase section of form."""
        MCH_ID = 0
        self.matchSelect.blockSignals(True)
        
        # Competition model
        compModel = self.compModel
        # get text from current index of Competition combobox
        compName = self.compSelect.currentText()
        
        # reset Match model filter if there is a db table already assigned
        if self.matchModel.tableName():
            self.matchModel.setFilter(QString())
            
        # use Competition Phase text to set appropriate Match model 
        phaseText = self.phaseSelect.currentText()
        if phaseText == "League":
            
            # get text from current index of Rounds combobox
            roundName = self.lgRoundSelect.currentText()
            # set match model to LeagueMatchList
            # filter match model on round name and competition name
            self.matchModel.setTable("league_match_list")
            self.matchModel.setSort(MCH_ID,  Qt.AscendingOrder)
            self.matchModel.setFilter(QString("round = '%1' AND competition = '%2'").arg(roundName, compName))
            self.matchModel.select()
            
        elif phaseText == "Group":
            
            # get text from current index of Group Rounds combobox
            roundName = self.grpRoundSelect.currentText()
            # get text from current index of Groups combobox
            groupName = self.groupSelect.currentText()
            # get text from current index of Rounds combobox
            matchdayName = self.grpMatchdaySelect.currentText()
            # set match model to GroupMatchList
            # filter match model on competition, round, group, and matchday names
            self.matchModel.setTable("group_match_list")
            self.matchModel.setSort(MCH_ID,  Qt.AscendingOrder)
            self.matchModel.setFilter(QString("competition = '%1' AND round = '%2' AND \
            group_name = '%3' AND matchday = '%4'").arg(compName, roundName, groupName, matchdayName))
            self.matchModel.select()
            
        elif phaseText == "Knockout":
        
            # get text from current index of Knockout Rounds combobox
            roundName = self.koRoundSelect.currentText()
            # get text from current index of Matchdays combobox
            matchdayName = self.koMatchdaySelect.currentText()
            # set match model to KnockoutMatchList
            # filter match model on competition, round, and matchday names
            self.matchModel.setTable("knockout_match_list")
            self.matchModel.setSort(MCH_ID,  Qt.AscendingOrder)
            self.matchModel.setFilter(QString("competition = '%1' AND round = '%2' AND \
            game = '%3'").arg(compName, roundName, matchdayName))
            self.matchModel.select()
            
        # define settings for matchSelect combobox
        self.matchSelect.setModel(self.matchModel)
        self.matchSelect.setModelColumn(self.matchModel.fieldIndex("matchup"))
        self.matchSelect.setCurrentIndex(-1)
        
        # enable matchSelect combobox if not enabled already        
        self.enableWidget(self.matchSelect)
        
        self.matchSelect.blockSignals(False)

    def enableStoppageTime(self, widget):
        """Enables stoppage time widget. 
        
        Enables widget if one of the following conditions are met:
            (1) minutes elapsed are nonzero and divisible by 45
            (2) minutes elapsed exceed 90 and are divisible by 15
        Argument:
        widget -- data widget object (stoppageEdit)
        
        """
        minutes = self.foultimeEdit.text().toInt()[0]
        if (minutes and not (minutes % 45)) or (minutes > 90 and not (minutes % 15)):
            widget.setEnabled(True)
        else:
            widget.setDisabled(True)
