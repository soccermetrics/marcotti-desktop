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

"""Contains classes that implement substitute-related entry forms to main tables of FMRD. 

Classes:
SubsEntryDlg -- data entry to Substitutions table
SwitchEntryDlg -- data entry to Switch Positions table
"""

class SubsEntryDlg(QDialog, ui_subsentry.Ui_SubsEntryDlg):
    """Implements substitutions data entry dialog, and accesses and writes to Substitutions table and In(Out)Substitutions linking tables.
    
    This dialog accepts data on substitution events during a match. 
   """
   
    ID, TIME, STIME = range(3)
    
    def __init__(self, parent=None):
        """Constructor for SubsEntryDlg class."""
        super(SubsEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define local parameters
        CMP_ID = RND_ID = TM_ID = 0
        MATCHDAY_NAME= IN_ID = OUT_ID = 1
        TEAM = 2
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
            self.teamSelect, self.inplayerSelect, self.outplayerSelect
        )
        
        self.upperFormWidgets = (
            self.compSelect, self.phaseSelect
        )
        
        self.lowerFormWidgets = (
            self.inplayerSelect, self.outplayerSelect, self.subtimeEdit
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
        self.teamModel.setTable("tbl_countries")
        self.teamModel.setSort(TEAM,  Qt.AscendingOrder)
        self.teamModel.select()
        self.teamSelect.setModel(self.teamModel)
        self.teamSelect.setModelColumn(self.teamModel.fieldIndex("cty_name"))
        self.teamSelect.setCurrentIndex(-1)        
        
        #
        # Match combobox
        # Instantiate an object here, specific details will
        # be set upon selection of Competition Phase
        #
        
        self.matchModel = QSqlTableModel(self)
        
        #
        # Define Substitutions data entry
        #
        
        # define underlying database model (tbl_substitutions)
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_substitutions")
        self.model.setSort(SubsEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.subsID_display, SubsEntryDlg.ID)
        self.mapper.addMapping(self.subtimeEdit, SubsEntryDlg.TIME)
        self.mapper.addMapping(self.stoppageEdit, SubsEntryDlg.STIME)

        # lineup models
        # need two copies of the same model so that
        # combobox filtering works
        playerInModel = QSqlTableModel(self)
        playerInModel.setTable("lineup_list")
        playerInModel.setSort(SORT_NAME, Qt.AscendingOrder)
        playerInModel.select()

        playerOutModel = QSqlTableModel(self)
        playerOutModel.setTable("lineup_list")
        playerOutModel.setSort(SORT_NAME, Qt.AscendingOrder)
        playerOutModel.select()

        # in substitution linking list
        self.inplayerModel = SubstituteLinkingModel("tbl_insubstitutions", self)
        self.inplayerSelect.setModel(playerInModel)
        self.inplayerSelect.setModelColumn(playerInModel.fieldIndex("player"))
        self.inplayerSelect.setCurrentIndex(-1)

        # out substitution linking list
        self.outplayerModel = SubstituteLinkingModel("tbl_outsubstitutions", self)
        self.outplayerSelect.setModel(playerOutModel)
        self.outplayerSelect.setModelColumn(playerOutModel.fieldIndex("player"))
        self.outplayerSelect.setCurrentIndex(-1)
        
        # in substitution mapper
        self.inplayerMapper = QDataWidgetMapper(self)
        self.inplayerMapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.inplayerMapper.setModel(self.inplayerModel)
        inplayerDelegate = GenericDelegate(self)
        inplayerDelegate.insertColumnDelegate(IN_ID, SubInComboBoxDelegate(self))
        self.inplayerMapper.setItemDelegate(inplayerDelegate)
        self.inplayerMapper.addMapping(self.inplayerSelect, IN_ID)
        self.inplayerMapper.toFirst()
        
        # out substitution mapper
        self.outplayerMapper = QDataWidgetMapper(self)
        self.outplayerMapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.outplayerMapper.setModel(self.outplayerModel)
        outplayerDelegate = GenericDelegate(self)
        outplayerDelegate.insertColumnDelegate(OUT_ID, SubOutComboBoxDelegate(self))
        self.outplayerMapper.setItemDelegate(outplayerDelegate)
        self.outplayerMapper.addMapping(self.outplayerSelect, OUT_ID)
        self.outplayerMapper.toFirst()
        
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
        
        # disable add, save, and delete entry buttons
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
        
        self.connect(self.matchSelect, SIGNAL("currentIndexChanged(int)"), self.filterSubstitutionsAndTeams)      
        self.connect(self.teamSelect, SIGNAL("currentIndexChanged(int)"), self.filterPlayers)                
        self.connect(self.subtimeEdit, SIGNAL("editingFinished()"),  lambda: self.enableStoppageTime(self.stoppageEdit))
 
    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if MsgPrompts.SaveDiscardOptionPrompt(self):
                if not self.mapper.submit():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                else:
                    self.updateLinkingTable(self.inplayerMapper, self.inplayerSelect)
                    self.updateLinkingTable(self.outplayerMapper, self.outplayerSelect)
        QDialog.accept(self)
   
    def saveRecord(self, where):
        """Submits changes to database, navigates through form, and resets subforms."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if MsgPrompts.SaveDiscardOptionPrompt(self):
                if not self.mapper.submit():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                else:
                    self.updateLinkingTable(self.inplayerMapper, self.inplayerSelect)
                    self.updateLinkingTable(self.outplayerMapper, self.outplayerSelect)                    
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
            
        subs_id = self.subsID_display.text()

        self.teamSelect.blockSignals(True)
        self.mapper.setCurrentIndex(row)
        self.refreshSubForms(subs_id)                
        self.refreshTeamBox()
        self.teamSelect.blockSignals(False)
                
        # enable stoppage time field if there is an entry
        if self.stoppageEdit.text() == "0":
            self.stoppageEdit.setEnabled(False)
        else:
            self.stoppageEdit.setEnabled(True)                

    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        Delete records in linking tables first, then delete record in parent table.
        
        """
        if QMessageBox.question(self, QString("Delete Record"), 
                                QString("Delete current record?"), 
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
            
        # get current subs_id
        subs_id = self.subsID_display.text()
        
        # delete corresponding records in linking tables
        self.inplayerModel.delete(subs_id)
        self.outplayerModel.delete(subs_id)
        
        # delete current record in parent table
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
            self.subtimeEdit.setText(QString())
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
        editorList = (self.subtimeEdit, self.stoppageEdit)
        columnList = (SubsEntryDlg.TIME, SubsEntryDlg.STIME)
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.text() != self.model.data(index).toString():
                return True
                
        # combobox fields that map to linking tables
        editorList = (self.inplayerSelect, self.outplayerSelect)   
        modelList = (self.inplayerModel, self.outplayerModel)
        for editor, model in zip(editorList, modelList):
            index = model.index(0, 1)
            if editor.currentText() != model.data(index).toString():
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
                        self.updateLinkingTable(self.inplayerMapper, self.inplayerSelect)
                        self.updateLinkingTable(self.outplayerMapper, self.outplayerSelect)                        
                else:
                    self.mapper.revert()
                    return
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(subs_id) FROM tbl_substitutions"))
        if query.next():
            maxSubsID = query.value(0).toInt()[0]
            if not maxSubsID:
                subs_id = Constants.MinSubstitutionID
            else:
                subs_id = QString()
                subs_id.setNum(maxSubsID+1)                  
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        
        # assign value to subsID field
        self.subsID_display.setText(subs_id)
        
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
        for widget in (self.teamSelect, self.inplayerSelect, self.outplayerSelect):
            widget.setCurrentIndex(-1)
        
        # set default stoppage time, clear match time
        self.stoppageEdit.setText("0")
        self.subtimeEdit.setText(QString())
        
        # refresh subforms
        self.refreshSubForms(subs_id)        

    def refreshTeamBox(self):
        """Sets index of team box so that it corresponds with selected player."""
        
        compName = self.compSelect.currentText()
        phaseText = self.phaseSelect.currentText()
        playerName = self.inplayerSelect.currentText()
        
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
        """Enables player, offense, and card comboboxes if not enabled already."""
        # enable data entry widgets
        for widget in self.lowerFormWidgets:
            widget.setEnabled(True)
        
        # enable stoppage time field if there is an entry
        if self.stoppageEdit.text() == "0":
            self.stoppageEdit.setEnabled(False)
        else:
            self.stoppageEdit.setEnabled(True)        
        
        self.filterInSubs()
        self.filterOutSubs()
        
    def refreshSubForms(self, currentID):
        """Sets match ID for linking models and refreshes models and mappers."""
        self.inplayerModel.setID(currentID)
        self.inplayerModel.refresh()
        
        self.outplayerModel.setID(currentID)
        self.outplayerModel.refresh()
                
        self.inplayerMapper.toFirst()
        self.outplayerMapper.toFirst()
        
    def updateLinkingTable(self, mapper, editor):
        """Updates custom linking table."""
        linkmodel = mapper.model()
        index = linkmodel.index(linkmodel.rowCount()-1, 0)
        boxIndex = editor.currentIndex()
        value = editor.model().record(boxIndex).value(0)
        ok = linkmodel.setData(index, value)
        return ok
        
    def filterInSubs(self):
        """Filters In Player combobox based on match and team selections.
        
        Players eligible for substitutions into match are lineup entries who meet all conditions:
            -- same match
            -- same team
            -- not starting
            -- not already subbed in
            
        """
        
        # suppress signals from inplayerSelect
        self.inplayerSelect.blockSignals(True)
        
        # get matchup from current text in matchSelect (main form)
        matchup = self.matchSelect.currentText()
       
        # get team name from current text in teamSelect (main form)
        teamName = self.teamSelect.currentText()
        
        # get player name from current text in inplayerSelect (main form)
        playerName = self.inplayerSelect.currentText()
        
        # lineup list model for combobox, reset filter on lineup list
        lineupListModel = self.inplayerSelect.model()
        lineupListModel.setFilter(QString())        
            
        # get lineup_id 
        lineupQuery = QSqlQuery()
        lineupQuery.exec_(QString("SELECT lineup_id FROM lineup_list WHERE player = %1").arg(playerName))
        if lineupQuery.isActive():
           lineupQuery.next()
           lineup_id = unicode(lineupQuery.value(0).toString())
        else:
           lineup_id = "-1"
           
        # get match_id by making a query on match_list with matchup
        matchQuery = QSqlQuery()
        matchQuery.prepare("SELECT match_id FROM match_list WHERE matchup = ?")
        matchQuery.addBindValue(QVariant(matchup))
        matchQuery.exec_()
        if matchQuery.next():
            match_id = matchQuery.value(0).toString()
        else:
            match_id = "-1"

        # get team_id by querying tbl_countries with team name
        teamQuery = QSqlQuery()
        teamQuery.prepare("SELECT country_id FROM tbl_countries WHERE cty_name = ?")
        teamQuery.addBindValue(QVariant(teamName))
        teamQuery.exec_()        
        if teamQuery.next():
            team_id = teamQuery.value(0).toString()
        else:
            team_id = "-1"
                
        # if there exists an entry, then find player name and set filter string for
        # Player combobox
        #
        #    -- filter players who can be subbed into match
        #    -- same match, same team, not starting, not already subbed in
        #    SELECT lineup_id FROM tbl_lineups WHERE lineup_id NOT IN
        #        (SELECT lineup_id FROM tbl_insubstitutions) AND 
        #        NOT lp_starting AND match_id = ? AND team_id = ?
        
        filterString = QString("lineup_id NOT IN "
                                   "(SELECT lineup_id FROM tbl_insubstitutions WHERE lineup_id <> %1) AND "
                                   "lineup_id IN (SELECT lineup_id from tbl_lineups WHERE "
                                   "lp_starting = 'false' AND match_id = %2 AND player_id IN "
                                   "(SELECT player_id FROM tbl_players WHERE country_id = %3))").arg(lineup_id).arg(match_id).arg(team_id)

        # filter Player combobox
        lineupListModel.setFilter(filterString)
        
        # set current index to item that matches data value
        self.inplayerSelect.setCurrentIndex(self.inplayerSelect.findText(playerName, Qt.MatchExactly))
        
        self.inplayerSelect.blockSignals(False)
        
    # Method: filterOutSubs
    #
    # Filter for Out Player combobox based on team selection and current index of combobox
    # Players who can be subbed out of a match        
    def filterOutSubs(self):
        """Filters Out Player combobox based on match and team selections.
        
        Players eligible for substitutions out of match are lineup entries who meet all conditions:
            -- same match
            -- same team
            -- starting OR (non-starter and already subbed in)
            -- not already subbed out
            
        """
        
        self.outplayerSelect.blockSignals(True)
        
        # get match_id from current text in matchSelect (main form)
        matchup = self.matchSelect.currentText()
       
        # get team_id from current text in teamSelect (main form)
        teamName = self.teamSelect.currentText()
        
        # get player name from current text in outplayerSelect (main form)
        playerName = self.outplayerSelect.currentText()

        # lineup list model for combobox, reset filter on lineup list
        lineupListModel = self.outplayerSelect.model()
        lineupListModel.setFilter(QString())
        
        # get lineup_id 
        lineupQuery = QSqlQuery()
        lineupQuery.prepare("SELECT lineup_id FROM lineup_list WHERE player = ?")
        lineupQuery.addBindValue(QVariant(playerName))
        lineupQuery.exec_()
        if lineupQuery.next():
           lineup_id = unicode(lineupQuery.value(0).toString())
        else:
           lineup_id = "-1"
           
        # get match_id by making a query on match_list with matchup
        matchQuery = QSqlQuery()
        matchQuery.prepare("SELECT match_id FROM match_list WHERE matchup = ?")
        matchQuery.addBindValue(QVariant(matchup))
        matchQuery.exec_()
        if matchQuery.next():
            match_id = matchQuery.value(0).toString()
        else:
            match_id = "-1"

        # get team_id by querying tbl_countries with team name
        teamQuery = QSqlQuery()
        teamQuery.prepare("SELECT country_id FROM tbl_countries WHERE cty_name = ?")
        teamQuery.addBindValue(QVariant(teamName))
        teamQuery.exec_()        
        if teamQuery.next():
            team_id = teamQuery.value(0).toString()
        else:
            team_id = "-1"        
                
        #    -- filter players who can be subbed out of match
        #    -- same match, same team, on lineup list, starting or already subbed in, not already subbed out
        #    SELECT player FROM tbl_lineups WHERE lineup_id NOT IN
        #        (SELECT lineup_id FROM tbl_outsubstitutions) AND lp_starting AND match_id = ? AND team_id = ?
        #    UNION
        #    SELECT player FROM tbl_lineups WHERE lineup_id IN
        #        (SELECT lineup_id FROM tbl_insubstitutions) AND NOT lp_starting AND match_id = ? AND team_id = ?

        filterString = QString("lineup_id NOT IN (SELECT lineup_id FROM tbl_outsubstitutions WHERE lineup_id <> %1) "
                               "AND lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE lp_starting = 'true' AND match_id = %2 AND player_id IN "
                                   "(SELECT player_id FROM tbl_players WHERE country_id = %3)) "
                               "OR (lineup_id IN (SELECT lineup_id FROM tbl_insubstitutions WHERE lineup_id <> %1) AND "
                               "lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE lp_starting = 'false' AND match_id = %2 AND player_id IN "
                                   "(SELECT player_id FROM tbl_players WHERE country_id = %3)))"
                               ).arg(lineup_id).arg(match_id).arg(team_id)
            
        # filter Player combobox
        lineupListModel.setFilter(filterString)

        # set current index to item that matches data value
        self.outplayerSelect.setCurrentIndex(self.outplayerSelect.findText(playerName, Qt.MatchExactly))
        
        self.outplayerSelect.blockSignals(False)

    def filterSubstitutionsAndTeams(self):
        """Filters Substitutions table from match selection."""
        
        # block signals from team combobox
        self.teamSelect.blockSignals(True)
        
        # clear filter
        self.model.setFilter(QString())
        
        # get current index
        currentIndex = self.matchSelect.currentIndex()
        
        # get match_id
        match_id = self.matchModel.record(currentIndex).value("match_id").toString()
        
        # filter substitutions of players from a specific match match (match_id)
        self.model.setFilter(QString("subs_id IN (SELECT subs_id FROM tbl_insubstitutions WHERE lineup_id IN "
                                                  "(SELECT lineup_id FROM tbl_lineups WHERE match_id = %1))").arg(match_id))
        self.mapper.toFirst()        
        
        # after subs_id populates, refresh subforms
        subs_id = self.subsID_display.text()
        self.refreshSubForms(subs_id)        
        
        # filter teams involved in match
        teamModel = self.teamSelect.model()
        teamModel.setFilter(QString())
        teamModel.setFilter(QString("country_id IN "
            "(SELECT country_id FROM tbl_hometeams WHERE match_id = %1 "
            "UNION SELECT country_id FROM tbl_awayteams WHERE match_id = %1)").arg(match_id))
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
            self.subtimeEdit.setValidator(QIntValidator(0, Constants.MAX_MINUTES, self))
        elif phaseText == "Group":
            self.grpRoundSelect.setEnabled(True)
            self.subtimeEdit.setValidator(QIntValidator(0, Constants.MAX_MINUTES, self))
        elif phaseText == "Knockout":
            self.koRoundSelect.setEnabled(True)
            self.subtimeEdit.setValidator(QIntValidator(0, Constants.MAX_KO_MINUTES, self))
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
        minutes = self.subtimeEdit.text().toInt()[0]
        if (minutes and not (minutes % 45)) or (minutes > 90 and not (minutes % 15)):
            widget.setEnabled(True)
        else:
            widget.setDisabled(True)

class SwitchEntryDlg(QDialog, ui_switchentry.Ui_SwitchEntryDlg):
    """Implements position switch data entry dialog, and accesses and writes to SwitchPositions table.
    
    This dialog accepts data on position switch events during a match. It is primarily focused on
    tracking forced changes of in-field players due to an expulsion of a goalkeeper, but it can
    track tactical position changes as well.
   """
   
    ID, LINEUP_ID, POS_ID, TIME, STIME = range(5)
    
    def __init__(self, parent=None):
        super(SwitchEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define local parameters
        CMP_ID = RND_ID = TM_ID = 0
        MATCHDAY_NAME= POS = 1
        TEAM = 2
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
            self.teamSelect, self.playerSelect, self.newPositionSelect
        )
        
        self.upperFormWidgets = (
            self.compSelect, self.phaseSelect
        )
        
        self.lowerFormWidgets = (
            self.playerSelect, self.newPositionSelect, self.switchtimeEdit
        )
        
        self.phaseWidgets = (
            self.lgRoundSelect, self.koRoundSelect, self.koMatchdaySelect, self.groupSelect, 
            self.grpRoundSelect, self.grpMatchdaySelect                             
        )

        #
        # Define comboboxes used to filter Position Switches table
        # Ensure that user only sees Position Switches for specific match
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
        self.teamModel.setTable("tbl_countries")
        self.teamModel.setSort(TEAM,  Qt.AscendingOrder)
        self.teamModel.select()
        self.teamSelect.setModel(self.teamModel)
        self.teamSelect.setModelColumn(self.teamModel.fieldIndex("cty_name"))
        self.teamSelect.setCurrentIndex(-1)        

        #
        # Match combobox
        # Instantiate an object here, specific details will
        # be set upon selection of Competition Phase
        #
        
        self.matchModel = QSqlTableModel(self)

        #
        # Define Switch Positions data entry
        #
        
        # underlying database model (tbl_switchpositions)
        # because of foreign keys, instantiate QSqlRelationalTableModel and define relations to it        
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_switchpositions")
        self.model.setRelation(SwitchEntryDlg.LINEUP_ID, QSqlRelation("lineup_list", "lineup_id", "player"))
        self.model.setRelation(SwitchEntryDlg.POS_ID, QSqlRelation("positions_list", "position_id", "position_name"))
        self.model.setSort(SwitchEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        switchDelegate = GenericDelegate(self)
        switchDelegate.insertColumnDelegate(SwitchEntryDlg.LINEUP_ID, SwitchPlayerComboBoxDelegate(self))
        self.mapper.setItemDelegate(switchDelegate)        

        # relation model for Player combobox
        self.playerModel = self.model.relationModel(SwitchEntryDlg.LINEUP_ID)
        self.playerModel.setSort(SORT_NAME,  Qt.AscendingOrder)
        self.playerSelect.setModel(self.playerModel)
        self.playerSelect.setModelColumn(self.playerModel.fieldIndex("player"))
        self.playerSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.playerSelect, SwitchEntryDlg.LINEUP_ID)

        # relation model for Positions combobox
        self.positionModel = self.model.relationModel(SwitchEntryDlg.POS_ID)
        self.positionModel.setSort(POS, Qt.AscendingOrder)
        self.newPositionSelect.setModel(self.positionModel)
        self.newPositionSelect.setModelColumn(self.positionModel.fieldIndex("position_name"))
        self.newPositionSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.newPositionSelect, SwitchEntryDlg.POS_ID)        
        
        # map other widgets on form
        self.mapper.addMapping(self.switchID_display, SwitchEntryDlg.ID)
        self.mapper.addMapping(self.switchtimeEdit, SwitchEntryDlg.TIME)
        self.mapper.addMapping(self.stoppageEdit, SwitchEntryDlg.STIME)

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
        
        # disable add, save, and delete entry buttons
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
        
        self.connect(self.matchSelect, SIGNAL("currentIndexChanged(int)"), self.filterSwitchesAndTeams)      
        self.connect(self.teamSelect, SIGNAL("currentIndexChanged(int)"), self.filterPlayers)                
        self.connect(self.switchtimeEdit, SIGNAL("editingFinished()"),  lambda: self.enableStoppageTime(self.stoppageEdit))        
        
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
        
        # enable Delete button
        self.enableWidget(self.deleteEntry)
        
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
            
        self.teamSelect.blockSignals(True)
        self.mapper.setCurrentIndex(row)
        
        # disable buttons and no widgets if no records in database
        if not self.model.rowCount():
            self.deleteEntry.setDisabled(True)
            self.saveEntry.setDisabled(True)
            
            self.switchID_display.setText(QString())
            for widget in self.selectWidgets:
                widget.setDisabled(True)
                widget.setCurrentIndex(-1)
            self.compSelect.setEnabled(True)
            
            self.switchtimeEdit.setDisabled(True)
            self.switchtimeEdit.setText(QString())
            self.stoppageEdit.setText("0")
        else:
            self.refreshTeamBox()
            
        self.teamSelect.blockSignals(False)
        
        # enable stoppage time field if there is an entry
        if self.stoppageEdit.text() == "0":
            self.stoppageEdit.setDisabled(True)
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
        editorList = (self.switchtimeEdit, self.stoppageEdit)
        columnList = (SwitchEntryDlg.TIME, SwitchEntryDlg.STIME)
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.text() != self.model.data(index).toString():
                return True
                
        # combobox fields
        editorList = (self.playerSelect, self.newPositionSelect)
        columnList = (SwitchEntryDlg.LINEUP_ID, SwitchEntryDlg.POS_ID)
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
        query.exec_(QString("SELECT MAX(switch_id) FROM tbl_switchpositions"))
        if query.next():
            maxSwitchID = query.value(0).toInt()[0]
            if not maxSwitchID:
                switch_id = Constants.MinSwitchID
            else:
                switch_id = QString()
                switch_id.setNum(maxSwitchID+1)                  
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        
        # assign value to switchID field
        self.switchID_display.setText(switch_id)
        
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
        for widget in (self.teamSelect, self.playerSelect, self.newPositionSelect):
            widget.setCurrentIndex(-1)
        
        # set default stoppage time, clear match time
        self.stoppageEdit.setText("0")
        self.switchtimeEdit.setText(QString())
        
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
        """Filters Players combobox down to players in match lineup for selected team, and enable remaining data widgets.
        
        Players eligible for substitutions out of match are lineup entries who meet all conditions:
            -- same match
            -- same team
            -- starting OR (non-starter and already subbed in)
            -- not already subbed out
                    
        """
        self.playerSelect.blockSignals(True)
        
        # get current matchup from current text in matchSelect (main form)
        matchup = self.matchSelect.currentText()
                
        # get current team from current text in teamSelect (main form)
        teamName = self.teamSelect.currentText()
        
        # get player name from current text in playerSelect (main form)
        playerName = self.playerSelect.currentText()
        
        # lineup list model for combobox, reset filter on lineup list
        lineupListModel = self.playerSelect.model()
        lineupListModel.setFilter(QString())
        
        # get lineup_id by making a query on lineup_list with player name
        lineupQuery = QSqlQuery()
        lineupQuery.prepare("SELECT lineup_id FROM lineup_list WHERE player = ?")
        lineupQuery.addBindValue(QVariant(playerName))
        lineupQuery.exec_()
        if lineupQuery.next():
           lineup_id = unicode(lineupQuery.value(0).toString())
        else:
           lineup_id = "-1"
        
        # get match_id by making a query on match_list with matchup
        matchQuery = QSqlQuery()
        matchQuery.prepare("SELECT match_id FROM match_list WHERE matchup = ?")
        matchQuery.addBindValue(QVariant(matchup))
        matchQuery.exec_()
        if matchQuery.next():
            match_id = matchQuery.value(0).toString()
        
        # get team_id by querying tbl_countries with team name
        team_id = "-1"
        teamQuery = QSqlQuery()
        teamQuery.prepare("SELECT country_id FROM tbl_countries WHERE cty_name = ?")
        teamQuery.addBindValue(QVariant(teamName))
        teamQuery.exec_()
        if teamQuery.next():
            team_id = teamQuery.value(0).toString()
        
        #    -- filter players who can be subbed out of match
        #    -- same match, same team, on lineup list, starting or already subbed in, not already subbed out
        #    SELECT player FROM tbl_lineups WHERE lineup_id NOT IN
        #        (SELECT lineup_id FROM tbl_outsubstitutions) AND lp_starting AND match_id = ? AND team_id = ?
        #    UNION
        #    SELECT player FROM tbl_lineups WHERE lineup_id IN
        #        (SELECT lineup_id FROM tbl_insubstitutions) AND NOT lp_starting AND match_id = ? AND team_id = ?
        
        filterString = QString("lineup_id NOT IN (SELECT lineup_id FROM tbl_outsubstitutions WHERE lineup_id <> %1) "
                               "AND lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE lp_starting = 'true' AND match_id = %2 AND player_id IN "
                                   "(SELECT player_id FROM tbl_players WHERE country_id = %3)) "
                               "OR (lineup_id IN (SELECT lineup_id FROM tbl_insubstitutions WHERE lineup_id <> %1) AND "
                               "lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE lp_starting = 'false' AND match_id = %2 AND player_id IN "
                                   "(SELECT player_id FROM tbl_players WHERE country_id = %3)))"
                               ).arg(lineup_id).arg(match_id).arg(team_id)
        
        # filter Players combobox
        lineupListModel.setFilter(filterString)
                
        # enable comboboxes if not enabled already
        self.playerSelect.setEnabled(True)
        self.newPositionSelect.setEnabled(True)
        self.switchtimeEdit.setEnabled(True)
        # enable stoppage time field if there is an entry
        if self.stoppageEdit.text() == "0":
            self.stoppageEdit.setEnabled(False)
        else:
            self.stoppageEdit.setEnabled(True)        
        
        # set current index to -1
        self.playerSelect.setCurrentIndex(-1)        
        self.playerSelect.blockSignals(False)

    def filterSwitchesAndTeams(self):
        """Filters SwitchPositions table from match selection."""

        # block signals from team combobox
        self.teamSelect.blockSignals(True)
        
        # clear filter
        self.model.setFilter(QString())
        
        # get current index
        currentIndex = self.matchSelect.currentIndex()
        
        # get match_id
        match_id = self.matchModel.record(currentIndex).value("match_id").toString()
        
        # filter position switches of players who were in lineup for match (match_id)
        self.model.setFilter(QString("tbl_switchpositions.lineup_id IN (SELECT lineup_id FROM lineup_list WHERE matchup IN "
                                                    "(SELECT matchup FROM match_list WHERE match_id = %1))").arg(match_id))
        self.mapper.toFirst()        
        
        # filter teams involved in match
        teamModel = self.teamSelect.model()
        teamModel.setFilter(QString())
        teamModel.setFilter(QString("country_id IN "
            "(SELECT country_id FROM tbl_hometeams WHERE match_id = %1 "
            "UNION SELECT country_id FROM tbl_awayteams WHERE match_id = %1)").arg(match_id))
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
            self.switchtimeEdit.setValidator(QIntValidator(0, Constants.MAX_MINUTES, self))
        elif phaseText == "Group":
            self.grpRoundSelect.setEnabled(True)
            self.switchtimeEdit.setValidator(QIntValidator(0, Constants.MAX_MINUTES, self))
        elif phaseText == "Knockout":
            self.koRoundSelect.setEnabled(True)
            self.switchtimeEdit.setValidator(QIntValidator(0, Constants.MAX_KO_MINUTES, self))
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
        minutes = self.switchtimeEdit.text().toInt()[0]
        if (minutes and not (minutes % 45)) or (minutes > 90 and not (minutes % 15)):
            widget.setEnabled(True)
        else:
            widget.setDisabled(True)
