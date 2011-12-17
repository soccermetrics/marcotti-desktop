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

"""Contains classes that implement penalty-related entry forms to main tables of FMRD. 

Classes:
PenaltyEntryDlg -- data entry to Penalties table
PenShootoutEntryDlg -- data entry to Penalty Shootouts and Penalty Openers tables
"""


class PenShootoutEntryDlg(QDialog, ui_penshootoutentry.Ui_PenShootoutEntryDlg):
    """Implements penalty shootout data entry dialog, and accesses and writes to PenaltyShootouts and PenShootoutOpeners tables.
    
   """
    ID, LINEUP_ID, ROUND_ID, OUTCOME_ID = range(4)
    
    def __init__(self, parent=None):
        super(PenShootoutEntryDlg, self).__init__(parent)
        self.setupUi(self)
    
        RND_ID = MCH_ID = 0
        MATCHDAY_NAME= TEAM = OUTCOME = OPENER = 1
        SORT_NAME = 4
    
        CMP_ID,  COMP_NAME = range(2)        
        KO_ROUND, KO_MATCHDAY = range(1, 3)
        
        # define lists of comboboxes
        self.selectWidgets = (
            self.compSelect, self.koRoundSelect, self.koMatchdaySelect, 
            self.matchSelect, self.penFirstSelect, self.roundSelect,  
            self.teamSelect, self.playerSelect,  self.penoutcomeSelect
        )
        
        self.lowerFormWidgets = (
            self.teamSelect, self.playerSelect,  self.penoutcomeSelect
        )

        #
        # Define comboboxes used to filter Penalty Shootouts table
        # Ensure that user only sees Penalty Shootouts for specific knockout match
        #
        
        # Competition combobox
        self.compModel = QSqlTableModel(self)
        self.compModel.setTable("tbl_competitions")
        self.compModel.setSort(CMP_ID, Qt.AscendingOrder)
        self.compModel.select()
        self.compSelect.setModel(self.compModel)
        self.compSelect.setModelColumn(self.compModel.fieldIndex("comp_name"))
        self.compSelect.setCurrentIndex(-1)

        # Knockout Rounds combobox
        knockoutRoundModel = QSqlTableModel(self)
        knockoutRoundModel.setTable("tbl_knockoutrounds")
        knockoutRoundModel.setSort(RND_ID, Qt.AscendingOrder)
        knockoutRoundModel.select()
        self.koRoundSelect.setModel(knockoutRoundModel)
        self.koRoundSelect.setModelColumn(knockoutRoundModel.fieldIndex("koround_desc"))
        self.koRoundSelect.setCurrentIndex(-1)
        
        # Matchdays (Knockout phase) combobox
        knockoutMatchdayModel = QSqlTableModel(self)
        knockoutMatchdayModel.setTable("tbl_matchdays")
        knockoutMatchdayModel.setSort(MATCHDAY_NAME, Qt.AscendingOrder)
        knockoutMatchdayModel.select()
        self.koMatchdaySelect.setModel(knockoutMatchdayModel)
        self.koMatchdaySelect.setModelColumn(knockoutMatchdayModel.fieldIndex("matchday_desc"))
        self.koMatchdaySelect.setCurrentIndex(-1)
        
        # Knockout Phase matches
        self.matchModel = QSqlTableModel(self)
        self.matchModel.setTable("knockout_match_list")
        self.matchModel.setSort(MCH_ID,  Qt.AscendingOrder)
        self.matchModel.select()
        self.matchSelect.setModel(self.matchModel)
        self.matchSelect.setModelColumn(self.matchModel.fieldIndex("matchup"))
        self.matchSelect.setCurrentIndex(-1)

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
        # Definitions for PenShootoutOpeners linking table
        #
        
        # Combobox for Team shooting first
        self.openerTeamModel = QSqlTableModel(self)
        self.openerTeamModel.setTable("tbl_teams")
        self.openerTeamModel.setSort(TEAM, Qt.AscendingOrder)
        self.openerTeamModel.select()
        self.penFirstSelect.setModel(self.openerTeamModel)
        self.penFirstSelect.setModelColumn(self.openerTeamModel.fieldIndex("tm_name"))
        self.penFirstSelect.setCurrentIndex(-1)
        
        # Linking table model and mapper definition
        self.penOpenerModel = ShootoutLinkingModel("tbl_penshootoutopeners", self)
        self.penOpenerMapper = QDataWidgetMapper(self)
        self.penOpenerMapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.penOpenerMapper.setModel(self.penOpenerModel)
        penOpenerDelegate = GenericDelegate(self)
        penOpenerDelegate.insertColumnDelegate(OPENER, ShootoutOpenerComboBoxDelegate(self))
        self.penOpenerMapper.setItemDelegate(penOpenerDelegate)
        self.penOpenerMapper.addMapping(self.penFirstSelect, OPENER)
        self.penOpenerMapper.toFirst()

        #
        # Define Penalty Shootouts data entry
        #
        
        # 
        # underlying database model (tbl_penaltyshootouts)
        # because of foreign keys, instantiate QSqlRelationalTableModel and define relations to it        
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_penaltyshootouts")
        self.model.setRelation(PenShootoutEntryDlg.LINEUP_ID, QSqlRelation("lineup_list", "lineup_id", "player"))
        self.model.setRelation(PenShootoutEntryDlg.ROUND_ID, QSqlRelation("tbl_rounds", "round_id", "round_desc"))
        self.model.setRelation(PenShootoutEntryDlg.OUTCOME_ID, QSqlRelation("tbl_penoutcomes", "penoutcome_id", "po_desc"))
        self.model.setSort(PenShootoutEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()

        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        penaltyDelegate = GenericDelegate(self)
        penaltyDelegate.insertColumnDelegate(PenShootoutEntryDlg.LINEUP_ID, ShootoutPlayerComboBoxDelegate(self))
        penaltyDelegate.insertColumnDelegate(PenShootoutEntryDlg.ROUND_ID, ShootoutRoundComboBoxDelegate(self))
        self.mapper.setItemDelegate(penaltyDelegate)        
        
        # Player combobox
        self.playerModel = self.model.relationModel(PenShootoutEntryDlg.LINEUP_ID)
        self.playerModel.setSort(SORT_NAME,  Qt.AscendingOrder)
        self.playerSelect.setModel(self.playerModel)
        self.playerSelect.setModelColumn(self.playerModel.fieldIndex("player"))
        self.playerSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.playerSelect, PenShootoutEntryDlg.LINEUP_ID)
        
        # Shootout Round combobox
        self.roundModel = self.model.relationModel(PenShootoutEntryDlg.ROUND_ID)
        self.roundModel.setSort(RND_ID,  Qt.AscendingOrder)
        self.roundSelect.setModel(self.roundModel)
        self.roundSelect.setModelColumn(self.roundModel.fieldIndex("round_desc"))
        self.roundSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.roundSelect, PenShootoutEntryDlg.ROUND_ID)
        
        # Penalty Outcome combobox
        self.outcomeModel = self.model.relationModel(PenShootoutEntryDlg.OUTCOME_ID)
        self.outcomeModel.setSort(OUTCOME, Qt.AscendingOrder)
        self.penoutcomeSelect.setModel(self.outcomeModel)
        self.penoutcomeSelect.setModelColumn(self.outcomeModel.fieldIndex("po_desc"))
        self.penoutcomeSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.penoutcomeSelect, PenShootoutEntryDlg.OUTCOME_ID)        
        
        # map other widgets on form
        self.mapper.addMapping(self.shootoutID_display, PenShootoutEntryDlg.ID)
        
        #
        # Disable data entry boxes
        #
        
        # disable all comboboxes and line edits 
        # EXCEPT competition combobox upon opening
        
        for widget in self.selectWidgets:
            widget.setDisabled(True)
        self.compSelect.setEnabled(True)

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
        
        self.connect(self.compSelect, SIGNAL("currentIndexChanged(int)"), self.enableAndFilterKnockoutRounds)
        self.connect(self.koRoundSelect, SIGNAL("currentIndexChanged(int)"), self.enableAndFilterMatchdays)
        self.connect(self.koMatchdaySelect, SIGNAL("currentIndexChanged(int)"), self.enableAndFilterMatches)
        self.connect(self.matchSelect, SIGNAL("currentIndexChanged(int)"), self.filterShootouts)
        self.connect(self.penFirstSelect, SIGNAL("currentIndexChanged(int)"), self.enableAndFilterShootoutRounds)
        self.connect(self.roundSelect, SIGNAL("currentIndexChanged(int)"), self.enableAndFilterTeams)
        self.connect(self.teamSelect, SIGNAL("currentIndexChanged(int)"), self.enableAndFilterPlayers)
#        self.connect(self.penFirstSelect, SIGNAL("currentIndexChanged(int)"), lambda: self.enableWidget(self.roundSelect))
#        self.connect(self.roundSelect, SIGNAL("currentIndexChanged(int)"), lambda: self.enableWidget(self.teamSelect))
#        self.connect(self.teamSelect, SIGNAL("currentIndexChanged(int)"), lambda: self.enableWidget(self.playerSelect))
        self.connect(self.playerSelect, SIGNAL("currentIndexChanged(int)"), lambda: self.enableWidget(self.penoutcomeSelect))

    def accept(self):
        """Submits changes to database and closes window upon confirmation from user.
        
        Submits record to Shootout Openers table only if mapper is at first entry."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if MsgPrompts.SaveDiscardOptionPrompt(self):
                if not self.mapper.submit():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                else:
                    if row == 0:
                        self.updateLinkingTable(self.penOpenerMapper, self.penFirstSelect)
        QDialog.accept(self)

    def addRecord(self):
        """Adds new record at end of entry list.
        
        Enables Rounds combobox.
        
        """
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if self.isDirty(row):
                if MsgPrompts.SaveDiscardOptionPrompt(self):
                    if not self.mapper.submit():
                        MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                    else:
                        if row == 0:
                            self.updateLinkingTable(self.penOpenerMapper, self.penFirstSelect)
                else:
                    self.mapper.revert()
                    return
        
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(penshootout_id) FROM tbl_penaltyshootouts"))
        if query.next():
            maxShootoutID= query.value(0).toInt()[0]
            if not maxShootoutID:
                shootout_id = Constants.MinShootoutID
            else:
                shootout_id= QString()
                shootout_id.setNum(maxShootoutID+1)       
                
        row = self.model.rowCount()
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        
        # assign value to shootoutID field
        self.shootoutID_display.setText(shootout_id)
        
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
        
        # if on first record:
        #   - enable Opener combobox
        if row == 0:
            self.enableWidget(self.penFirstSelect) 
        else:
            self.disableWidget(self.penFirstSelect) 
            
        # enable roundSelect
        # disable remaining form widgets
        for widget in self.lowerFormWidgets:
            widget.setDisabled(True)
            widget.setCurrentIndex(-1)
        self.enableWidget(self.roundSelect)        
        
    def refreshTeamBox(self):
        """Sets index of team box so that it corresponds with selected player."""
        
        row = self.mapper.currentIndex()
        
        compName = self.compSelect.currentText()
        playerName = self.model.record(row).value("player").toString()
        roundName = self.koRoundSelect.currentText()
        matchdayName = self.koMatchdaySelect.currentText()
        
        # set team filter
        self.enableAndFilterTeams(playerName)
        
        # look for team name
        query = QSqlQuery()
        query.prepare("SELECT team FROM lineup_list WHERE player = ? AND "
                               "matchup IN (SELECT matchup FROM knockout_match_list WHERE competition = ? AND round = ? AND game = ?)")
        query.addBindValue(QVariant(playerName))
        query.addBindValue(QVariant(compName))
        query.addBindValue(QVariant(roundName))
        query.addBindValue(QVariant(matchdayName))
        query.exec_()
        if query.next():
            teamName = query.value(0).toString()
        else:
            teamName = "-1"
        
        currentIndex = self.teamSelect.findText(teamName, Qt.MatchExactly)
        self.teamSelect.setCurrentIndex(currentIndex)
        
    def deleteRecord(self):
        """Deletes record from database upon user confirmation."""
        # save match_id corresponding to selected match
        # this will be used to remove record in linking table if all parent records deleted
        matchIndex = self.matchSelect.currentIndex()
        match_id = self.matchModel.record(matchIndex).value("match_id").toString()
        
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
        
        # if no records in database:
        #   - disable buttons 
        #   - disable all dropboxes except Competition
        #   - delete corresponding record in Shootout Openers linking table
        # If one record in database:
        #   - 
        if not self.model.rowCount():
            self.penOpenerModel.delete(match_id)
            self.deleteEntry.setDisabled(True)
            self.saveEntry.setDisabled(True)
            for widget in self.selectWidgets:
                widget.setDisabled(True)
                widget.setCurrentIndex(-1)
            self.enableWidget(self.compSelect)
        else:
            self.refreshTeamBox()
            if self.model.rowCount() == 1:
                self.enableWidget(self.penFirstSelect)
            
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
        editorList = (self.shootoutID_display, )
        columnList = (PenShootoutEntryDlg.ID, )
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.text() != self.model.data(index).toString():
                return True
        
        # combobox fields
        editorList = (self.playerSelect, self.roundSelect, self.penoutcomeSelect)
        columnList = (PenShootoutEntryDlg.LINEUP_ID, 
                              PenShootoutEntryDlg.ROUND_ID, PenShootoutEntryDlg.OUTCOME_ID)
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.currentText() != self.model.data(index).toString():
                return True
                    
        return False
        
    def saveRecord(self, where):
        """"Submits changes to database, navigates through form, and resets subforms."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if MsgPrompts.SaveDiscardOptionPrompt(self):
                if not self.mapper.submit():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                else:
                    self.updateLinkingTable(self.penOpenerMapper, self.penFirstSelect)
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
        self.refreshTeamBox()
        
        # enable Delete button if at least one record
        if self.model.rowCount():
            self.deleteEntry.setEnabled(True)
        # if on first record:
        # - enable Opener combobox
        # - refresh linking table
        if row == 0:
            self.enableWidget(self.penFirstSelect)
            self.refreshSubForm()
        else:
            self.disableWidget(self.penFirstSelect)

    def updateLinkingTable(self, mapper, editor):
        """Updates current record or inserts new record in custom linking table.
        
        Arguments:
        mapper -- mapper object associated with data widget and data model
        editor -- data widget object
        """
        # database table associated with mapper
        # get current index of model
        linkModel = mapper.model()
        index = linkModel.index(linkModel.rowCount()-1, 0)
        
        boxIndex = editor.currentIndex()
        value = editor.model().record(boxIndex).value(0)
        ok = linkModel.setData(index, value)
        return ok
        
    def refreshSubForm(self):
        """Sets match ID for Penalty Openers linking model and refreshes model and mapper."""
        matchIndex = self.matchSelect.currentIndex()
        match_id = self.matchModel.record(matchIndex).value("match_id").toString()
        self.penOpenerModel.setID(match_id)
        self.penOpenerModel.refresh()
        self.penOpenerMapper.toFirst()
        
    def enableWidget(self, widget):
        """Enables widget passed in function parameter, if not already enabled."""
        if not widget.isEnabled():
            widget.setEnabled(True)
            
    def disableWidget(self, widget):
        """Disables widget passed in function parameter, if not already disabled."""
        if widget.isEnabled():
            widget.setDisabled(True)

    def getShootoutRotation(self, round_id):
        """Determine 11-round rotation in which current shootout round is a member."""
        minRoundID = int(Constants.MinRoundID)
        startRotationID = minRoundID

        # get maximum Round ID
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(round_id) FROM tbl_rounds"))
        if query.next():
            maxRoundID = query.value(0).toInt()[0]
        
        if round_id < minRoundID:
            if minRoundID + Constants.MAX_TEAM_STARTERS > maxRoundID:
                endRotationID = maxRoundID + 1
            else:
                endRotationID = minRoundID + Constants.MAX_TEAM_STARTERS
        else:
            while round_id not in range(startRotationID, startRotationID+Constants.MAX_TEAM_STARTERS):
                startRotationID += Constants.MAX_TEAM_STARTERS
            endRotationID = startRotationID + Constants.MAX_TEAM_STARTERS
        rotationList = range(startRotationID, endRotationID)

        return rotationList
        
    def getAvailableRounds(self, match_id):
        """Returns rounds that have not had maximum participation in Penalty Shootout table.
        
        Argument:
            match_id -- match ID from knockout_match_list
        """
        roundIDList = []
        roundstr = QString()
        
        # define min/max round ID in table
        minRoundID = int(Constants.MinRoundID)
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(round_id) FROM tbl_rounds"))
        if query.next():
            maxRoundID = query.value(0).toInt()[0]
            
        # loop through round ID
        # if round referenced less than twice in table, add it to list
        for round_id in range(minRoundID, maxRoundID+1):
            roundQuery = QSqlQuery()
            roundstr.setNum(round_id)
            roundQuery.exec_(QString("SELECT COUNT(*) FROM tbl_penaltyshootouts WHERE round_id = %1 "
                                "AND lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE match_id = %2)").arg(roundstr, match_id))
            if roundQuery.next():
                if roundQuery.value(0).toInt()[0] < Constants.MAX_PARTICIPATION:
                    roundIDList.append(round_id)
                    
        return roundIDList
        
    def getAvailableTeams(self, match_id, round_id):
        """Returns teams whose players have yet to participate in shootout round."""
        teamList = []
        
        # query participating teams in match, save results to list
        teamQuery = QSqlQuery()
        teamQuery.exec_(QString("SELECT team_id FROM tbl_teams where team_id IN"
            "(SELECT team_id FROM tbl_hometeams WHERE match_id = %1"
            "UNION SELECT team_id FROM tbl_awayteams WHERE match_id = %1)").arg(match_id))
        while teamQuery.next():
            teamList.append(teamQuery.value(0).toInt()[0])
            
        # count number of players in team lineup who have participated in specific round of penalty shootout
        countQuery = QSqlQuery()
        countQuery.prepare("SELECT COUNT(*) FROM tbl_penaltyshootouts WHERE round_id = ? "
                                "AND lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE match_id = ? AND team_id = ?)")
        # loop through list of teams
        for team_id in teamList:
            countQuery.addBindValue(QVariant(round_id))
            countQuery.addBindValue(QVariant(match_id))
            countQuery.addBindValue(QVariant(team_id))
            countQuery.exec_()
            if countQuery.next():
                if countQuery.value(0).toInt()[0]:
                    teamList.remove(team_id)
                    
        return teamList
        
    def getEligiblePlayers(self, match_id, team_id):
        """Returns list of players who are eligible to participate in penalty shootout.
        
        The list contains players who meet the following two criteria:
            (1) Starting players on the same team who have not been substituted out of the match.
            (2) Non-starting players on the same team who have been substituted into the match.
        """
        eligibleList = []
        
        lineupQuery = QSqlQuery()
        eligibleQueryString = QString("SELECT lineup_id FROM tbl_lineups WHERE "
                "lineup_id NOT IN (SELECT lineup_id FROM tbl_outsubstitutions) "
                "AND lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE lp_starting AND match_id = %1 AND team_id = %2) "
                "OR (lineup_id IN (SELECT lineup_id FROM tbl_insubstitutions) AND "
                "lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE NOT lp_starting AND match_id = %1 AND team_id = %2))"
                ).arg(match_id).arg(team_id)  
        lineupQuery.prepare(eligibleQueryString)
        lineupQuery.exec_()
        while lineupQuery.next():
            eligibleList.append(lineupQuery.value(0).toInt()[0])
            
        return eligibleList
        
    def getUsedPlayers(self, match_id, team_id, round_id):
        """Returns players who have already participated in current rotation (11 round period) of penalty shootout. """
        usedList = []
        
        # get rotation that contains current shootout round
        rotationList = self.getShootoutRotation(round_id)
        
        participateQuery = QSqlQuery()
        participateQuery.prepare(QString("SELECT lineup_id FROM tbl_lineups WHERE match_id = %1 AND team_id = %2 "
                                 "AND lineup_id IN (SELECT lineup_id FROM tbl_penaltyshootouts WHERE round_id = ?)").arg(match_id, team_id))
        for round_id in rotationList:
            participateQuery.addBindValue(round_id)
            participateQuery.exec_()
            while participateQuery.next():
                usedList.append(participateQuery.value(0).toInt()[0])
                
        return usedList
        
    def enableAndFilterPlayers(self):
        """Enables Players combobox and filters its contents based on players eligible to participate in penalty shootout.
        
        The following players are listed in the combobox:
            (1) Starting players on the same team who have not been substituted out of the match.
            (2) Non-starting players on the same team who have been substituted into the match.
            (3) Players in groups (1) and (2) who have not been selected in a full rotation (11 rounds) 
                  of the penalty shootout.
        """
        row = self.mapper.currentIndex()
        
        # get current index from match combobox
        matchIndex = self.matchSelect.currentIndex()
        match_id = self.matchModel.record(matchIndex).value("match_id").toInt()[0]
        
        # get current index from team combobox
        teamIndex = self.teamSelect.currentIndex()
        team_id = self.teamModel.record(teamIndex).value("team_id").toInt()[0]
        
        # get current index from shootout round combobox
        roundIndex = self.roundSelect.currentIndex()
        round_id = self.roundModel.record(roundIndex).value("round_id").toInt()[0]
        
        # get current player name
        playerName = self.model.record(row).value("player").toString()
        
        # block signals from player combobox
        self.playerSelect.blockSignals(True)

        # enable playerSelect combobox if not enabled already
        self.enableWidget(self.playerSelect)
        # get set of team players eligible to participate in penalty shootout
        teamEligibleSet = set(self.getEligiblePlayers(match_id, team_id))
        # get available players for current rotation of shootout round
        playersUsedList = self.getUsedPlayers(match_id, team_id, round_id)
        availableList = list(teamEligibleSet.difference(playersUsedList))
        
        # include player in current record
        if playerName:
            lineupQuery = QSqlQuery()
            lineupQuery.prepare("SELECT lineup_id FROM lineup_list WHERE player = ? "
                "AND matchup IN (SELECT matchup FROM knockout_match_list WHERE match_id = ?)")
            lineupQuery.addBindValue(QVariant(playerName))
            lineupQuery.addBindValue(QVariant(match_id))
            lineupQuery.exec_()
            if lineupQuery.next():
                lineup_id = lineupQuery.value(0).toInt()[0]
            availableList.append(lineup_id)
            availableList = list(set(availableList))
            
        # filter players available for shootout
        self.playerModel.setFilter(QString())
        filterString = "lineup_id IN (" + ",".join((str(n) for n in availableList)) + ")"
        self.playerModel.setFilter(filterString)
        self.playerModel.select()
        # reset playerSelect index
        if playerName:
            self.playerSelect.setCurrentIndex(self.playerSelect.findText(playerName, Qt.MatchExactly))
        else:
            self.playerSelect.setCurrentIndex(-1)    
        
        # unblock signals from player combobox
        self.playerSelect.blockSignals(False)

    def enableAndFilterTeams(self, player=None):
        """Enables Teams combobox and filters its contents based on competing teams in selected match."""
        
        # get current index of match combobox
        currentIndex = self.matchSelect.currentIndex()
        match_id = self.matchModel.record(currentIndex).value("match_id").toString()
        
        # get current index of shootout round combobox
        roundIndex = self.roundSelect.currentIndex()
        round_id = self.roundModel.record(roundIndex).value("round_id").toString()
        
        # block signals from team combobox
        self.teamSelect.blockSignals(True)

        # enable teamSelect combobox if not enabled already
        self.enableWidget(self.teamSelect)
        # get available teams for shootout round
        teamList = self.getAvailableTeams(match_id, round_id)
        # if player name has been passed, get its team_id and add it to list
        if player:
            teamQuery = QSqlQuery()
            teamQuery.prepare("SELECT team_id FROM tbl_teams WHERE tm_name IN "
            "(SELECT team FROM lineup_list WHERE player = ? AND matchup IN "
            "(SELECT matchup FROM knockout_match_list WHERE match_id = ?))")
            teamQuery.addBindValue(player)
            teamQuery.addBindValue(match_id)
            teamQuery.exec_()
            if teamQuery.next():
                team_id = teamQuery.value(0).toInt()[0]
            teamList.append(team_id)
            teamList = list(set(teamList))
            
        # filter teams involved in match
        self.teamModel.setFilter(QString())
        baseFilterString = QString("team_id IN (SELECT team_id FROM tbl_hometeams WHERE match_id = %1"
            "UNION SELECT team_id FROM tbl_awayteams WHERE match_id = %1) ").arg(match_id)
        augFilterString = "AND team_id IN (" + ",".join((str(n) for n in teamList)) + ")"
        teamFilterString = baseFilterString + augFilterString
        self.teamModel.setFilter(baseFilterString)
        
        # reset teamSelect index
        self.teamSelect.setCurrentIndex(-1)    
        
        # unblock signals from team combobox
        self.teamSelect.blockSignals(False)

    def enableAndFilterShootoutRounds(self):
        """Enables Shootout Rounds combobox and filters its contents based on participation in penalty shootout.
        
        Also enable Add button in form."""
        
        row = self.mapper.currentIndex()
        
        # get current match_id of selected match
        currentIndex = self.matchSelect.currentIndex()
        match_id = self.matchModel.record(currentIndex).value("match_id").toString()

        # shootout round in current record of penalty shootout model
        roundName = self.model.record(row).value("round_desc").toString()
        
        # enable Add button
        self.enableWidget(self.addEntry)
        
        # block signals from rounds combobox
        self.roundSelect.blockSignals(True)
        
        # flush shootout round filter
        self.roundModel.setFilter(QString())
        
        # get available rounds in shootout
        roundList = self.getAvailableRounds(match_id)
        # if there is a valid record, get round_id and add it to roundList
        if roundName:
            roundQuery = QSqlQuery()
            roundQuery.prepare(QString("SELECT round_id FROM tbl_rounds WHERE round_desc = ?"))
            roundQuery.addBindValue(roundName)
            roundQuery.exec_()
            if roundQuery.next():
                round_id = roundQuery.value(0).toInt()[0]
            roundList.append(round_id)
            roundList = list(set(roundList))
            
        # create filter on shootout rounds
        roundFilterString = "round_id IN (" + ",".join((str(n) for n in roundList)) + ")"
        self.roundModel.setFilter(roundFilterString)
        
        # unblock signals from rounds combobox
        self.roundSelect.blockSignals(False)

    def filterOpeners(self):
        """Filters Teams combobox to the pair participating in the selected football match."""
        
        matchIndex = self.matchSelect.currentIndex()
        match_id = self.matchModel.record(matchIndex).value("match_id").toString()
        
        # flush team model (opening team in shootout)
        self.openerTeamModel.setFilter(QString())
        
        # team filter
        teamQueryString = QString("team_id IN"
            "(SELECT team_id FROM tbl_hometeams WHERE match_id = %1"
            "UNION SELECT team_id FROM tbl_awayteams WHERE match_id = %1)").arg(match_id)
        self.openerTeamModel.setFilter(teamQueryString)
        # reset index to -1
        self.penFirstSelect.setCurrentIndex(-1)
        
    def filterShootouts(self):
        """Filters Penalty Shootouts table to display all entries from selected match."""
        
        # clear filter
        self.model.setFilter(QString())
        
        matchIndex = self.matchSelect.currentIndex()
        match_id = self.matchModel.record(matchIndex).value("match_id").toString()
        
        # filter penalty shootouts taken by players who were in lineup for match (match_id)
        self.model.setFilter(QString("tbl_penaltyshootouts.lineup_id IN (SELECT lineup_id FROM lineup_list WHERE matchup IN "
                                                    "(SELECT matchup FROM match_list WHERE match_id = %1))").arg(match_id))
        self.mapper.toFirst()       
        self.refreshSubForm()
        # refresh team select box
        self.refreshTeamBox()
        
        # enable Add Record button
        self.enableWidget(self.addEntry)
        
        # enable penFirstSelect if no records in filtered table
        if self.model.rowCount() == 0:
            self.penFirstSelect.blockSignals(True)
            self.filterOpeners()
            self.enableWidget(self.penFirstSelect)
            self.penFirstSelect.blockSignals(False)
            # disable lower form widgets
            for widget in self.lowerFormWidgets:
                self.disableWidget(widget)
            # disable navigation buttons
            for widget in (self.firstEntry, self.prevEntry, self.nextEntry, self.lastEntry):
                self.disableWidget(widget)
            # disable Add, Save, Delete buttons
            for widget in (self.addEntry, self.deleteEntry, self.saveEntry):
                self.disableWidget(widget)
        else:
            # enable penFirstSelect at first record
            self.enableWidget(self.penFirstSelect)
            # disable First/Prev nav buttons
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            # enable Next/Last nav buttons if multiple records
            if self.model.rowCount() > 1:
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)                        
            # enable Save/Delete buttons
            self.saveEntry.setEnabled(True)
            self.deleteEntry.setEnabled(True)
            # enable lower form widgets
            self.roundSelect.setEnabled(True)
            for widget in self.lowerFormWidgets:
                widget.setEnabled(True)
                
    def enableAndFilterKnockoutRounds(self):
        """Enables Knockout Rounds combobox and filters its contents based on Competition selections.
        
        Argument:
        phaseText -- name of selected Competition Phase (phaseSelect)
        """
        # Competitions model
        compModel = self.compModel
        # get text from current index of Competition combobox
        compName = self.compSelect.currentText()
        
        self.koRoundSelect.blockSignals(True)
        
        # enable Knockout Rounds combobox
        self.enableWidget(self.koRoundSelect)
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

    def enableAndFilterMatchdays(self):
        """Enables Matchdays combobox and filters its contents based on selections in Competition and Knockout Round fields."""
        
        # Competition model
        compModel = self.compModel
        # get text from current index of Competition combobox
        compName = self.compSelect.currentText()
        
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
        
        # Competition model
        compModel = self.compModel
        # get text from current index of Competition combobox
        compName = self.compSelect.currentText()
        # get text from current index of Knockout Rounds combobox
        roundName = self.koRoundSelect.currentText()
        # get text from current index of Matchdays combobox
        matchdayName = self.koMatchdaySelect.currentText()
        
        self.matchSelect.blockSignals(True)
        
        # enable matchSelect combobox if not enabled already    
        self.enableWidget(self.matchSelect)
        # reset Match model filter
        self.matchModel.setFilter(QString())
        # filter match model on competition, round, and matchday names
        self.matchModel.setFilter(QString("competition = '%1' AND round = '%2' AND \
        game = '%3'").arg(compName, roundName, matchdayName))
        self.matchSelect.setCurrentIndex(-1)
        self.matchSelect.blockSignals(False)
