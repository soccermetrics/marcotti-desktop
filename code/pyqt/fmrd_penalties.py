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

class PenaltyEntryDlg(QDialog, ui_penaltyentry.Ui_PenaltyEntryDlg):
    """Implements penalty kick data entry dialog, and accesses and writes to Penalties table.
    
    This dialog accepts data on penalty kick events during a match.
   """
   
    ID, LINEUP_ID, FOUL_ID, OUTCOME_ID, TIME, STIME = range(6)
    
    def __init__(self, parent=None):
        """Constructor for PenaltyEntryDlg class."""
        super(PenaltyEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        CMP_ID = RND_ID = MCH_ID = TM_ID = 0
        TEAM = FOUL = OUTCOME = 1
        SORT_NAME = 4

        #
        # Define comboboxes used to filter Penalty table
        # Ensure that user only sees Penalties for specific match
        #
        
        # Competition combobox
        self.compModel = QSqlTableModel(self)
        self.compModel.setTable("tbl_competitions")
        self.compModel.setSort(CMP_ID, Qt.AscendingOrder)
        self.compModel.select()
        self.compSelect.setModel(self.compModel)
        self.compSelect.setModelColumn(self.compModel.fieldIndex("comp_name"))
        self.compSelect.setCurrentIndex(-1)
        
        # Round combobox
        self.roundModel = QSqlTableModel(self)
        self.roundModel.setTable("tbl_rounds")
        self.roundModel.setSort(RND_ID, Qt.AscendingOrder)
        self.roundModel.select()
        self.roundSelect.setModel(self.roundModel)
        self.roundSelect.setModelColumn(self.roundModel.fieldIndex("round_desc"))
        self.roundSelect.setCurrentIndex(-1)
        
        # Match combobox
        self.matchModel = QSqlTableModel(self)
        self.matchModel.setTable("match_list")
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
        # Define Penalties data entry
        #
        
        # 
        # underlying database model (tbl_goals)
        # because of foreign keys, instantiate QSqlRelationalTableModel and define relations to it        
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_penalties")
        self.model.setRelation(PenaltyEntryDlg.LINEUP_ID, QSqlRelation("lineup_list", "lineup_id", "player"))
        self.model.setRelation(PenaltyEntryDlg.FOUL_ID, QSqlRelation("tbl_fouls", "foul_id", "foul_desc"))
        self.model.setRelation(PenaltyEntryDlg.OUTCOME_ID, QSqlRelation("tbl_penoutcomes", "penoutcome_id", "po_desc"))
        self.model.setSort(PenaltyEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        penaltyDelegate = GenericDelegate(self)
        penaltyDelegate.insertColumnDelegate(PenaltyEntryDlg.LINEUP_ID, EventPlayerComboBoxDelegate(self))
        self.mapper.setItemDelegate(penaltyDelegate)        

        # set up Player combobox
        self.playerModel = self.model.relationModel(PenaltyEntryDlg.LINEUP_ID)
        self.playerModel.setSort(SORT_NAME,  Qt.AscendingOrder)
        self.playerSelect.setModel(self.playerModel)
        self.playerSelect.setModelColumn(self.playerModel.fieldIndex("player"))
        self.playerSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.playerSelect, PenaltyEntryDlg.LINEUP_ID)

        # relation model for Foul combobox
        self.foulModel = self.model.relationModel(PenaltyEntryDlg.FOUL_ID)
        self.foulModel.setSort(FOUL, Qt.AscendingOrder)
        self.foulSelect.setModel(self.foulModel)
        self.foulSelect.setModelColumn(self.foulModel.fieldIndex("foul_desc"))
        self.foulSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.foulSelect, PenaltyEntryDlg.FOUL_ID)        
        
        # relation model for Penalty Outcome combobox
        self.outcomeModel = self.model.relationModel(PenaltyEntryDlg.OUTCOME_ID)
        self.outcomeModel.setSort(OUTCOME, Qt.AscendingOrder)
        self.penoutcomeSelect.setModel(self.outcomeModel)
        self.penoutcomeSelect.setModelColumn(self.outcomeModel.fieldIndex("po_desc"))
        self.penoutcomeSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.penoutcomeSelect, PenaltyEntryDlg.OUTCOME_ID)        

        # map other widgets on form
        self.mapper.addMapping(self.penaltyID_display, PenaltyEntryDlg.ID)
        self.mapper.addMapping(self.pentimeEdit, PenaltyEntryDlg.TIME)
        self.mapper.addMapping(self.stoppageEdit, PenaltyEntryDlg.STIME)
        
        #
        # Disable data entry boxes
        #
        
        # disable all comboboxes and line edits 
        # EXCEPT competition combobox upon opening
        self.roundSelect.setDisabled(True)
        self.matchSelect.setDisabled(True)
        
        self.teamSelect.setDisabled(True)
        self.playerSelect.setDisabled(True)
        self.foulSelect.setDisabled(True)
        self.penoutcomeSelect.setDisabled(True)
        self.pentimeEdit.setDisabled(True)
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
        
        self.connect(self.compSelect, SIGNAL("currentIndexChanged(int)"), lambda: self.enableAndFilterRounds(self.roundSelect))
        self.connect(self.roundSelect, SIGNAL("currentIndexChanged(int)"),  lambda: self.enableAndFilterMatches(self.matchSelect))
        self.connect(self.matchSelect, SIGNAL("currentIndexChanged(int)"), self.filterPenaltiesAndTeams)
        self.connect(self.teamSelect, SIGNAL("currentIndexChanged(int)"), self.filterPlayers)        
        self.connect(self.pentimeEdit, SIGNAL("editingFinished()"),  lambda: self.enableStoppageTime(self.stoppageEdit))

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
        
        # enable stoppage time field if there is an entry
        if self.stoppageEdit.text() == "0":
            self.stoppageEdit.setEnabled(False)
        else:
            self.stoppageEdit.setEnabled(True)        
        
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
        """
        # line edit fields
        editorList = (self.pentimeEdit, self.stoppageEdit)
        columnList = (PenaltyEntryDlg.TIME, PenaltyEntryDlg.STIME)
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.text() != self.model.data(index).toString():
                return True
                
        # combobox fields
        editorList = (self.playerSelect, self.foulSelect, self.penoutcomeSelect)
        columnList = (PenaltyEntryDlg.LINEUP_ID, PenaltyEntryDlg.FOUL_ID, PenaltyEntryDlg.OUTCOME_ID)
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
        query.exec_(QString("SELECT MAX(penalty_id) FROM tbl_penalties"))
        if query.next():
            maxPenaltyID = query.value(0).toInt()[0]
            if not maxPenaltyID:
                penalty_id = Constants.MinPenaltyID
            else:
                penalty_id = QString()
                penalty_id.setNum(maxPenaltyID+1)                  
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        
        # assign value to goalID field
        self.penaltyID_display.setText(penalty_id)
        
        # disable navigation button
        self.prevEntry.setEnabled(True)
        self.firstEntry.setEnabled(True)
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)        
        
        # enable Team combobox
        # set Team combobox to blank item
        self.teamSelect.setEnabled(True)
        self.teamSelect.setCurrentIndex(-1)        
        
        # disable stoppage time edit box upon opening
        # set default stoppage time
        # clear match time
        self.stoppageEdit.setDisabled(True)
        self.stoppageEdit.setText("0")
        self.pentimeEdit.setText(QString())

    def refreshTeamBox(self):
        """Sets index of team box so that it corresponds with selected player."""
#        print "Calling refreshTeamBox()"
        
        compName = self.compSelect.currentText()
        roundName = self.roundSelect.currentText()
        playerName = self.playerSelect.currentText()
        
#        print "Competition: %s" % compName
#        print "Round: %s" % roundName
#        print "Player: %s" % playerName
        
        # look for team name
        query = QSqlQuery()
        query.prepare("SELECT team FROM lineup_list WHERE player = ? AND "
                               "matchup IN (SELECT matchup FROM match_list WHERE competition = ? AND matchday = ?)")
        query.addBindValue(QVariant(playerName))
        query.addBindValue(QVariant(compName))
        query.addBindValue(QVariant(roundName))
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
                
        # enable comboboxes if not enabled already
        self.playerSelect.setEnabled(True)
        self.foulSelect.setEnabled(True)
        self.penoutcomeSelect.setEnabled(True)
        self.pentimeEdit.setEnabled(True)
        # enable stoppage time field if there is an entry
        if self.stoppageEdit.text() == "0":
            self.stoppageEdit.setEnabled(False)
        else:
            self.stoppageEdit.setEnabled(True)        
        
        # set current index to -1
        self.playerSelect.setCurrentIndex(-1)        
        self.playerSelect.blockSignals(False)

    def filterPenaltiesAndTeams(self):
        """Filters Penalties table to display all entries from selected match, and filters Teams combobox down to the two participants."""
        
        # enable add, save, and delete entry buttons
        self.addEntry.setEnabled(True)
        self.saveEntry.setEnabled(True)
        self.deleteEntry.setEnabled(True)

        # block signals from team combobox
        self.teamSelect.blockSignals(True)

        # clear filter
        self.model.setFilter(QString())
        
        # get current index
        currentIndex = self.matchSelect.currentIndex()
        
        # get match_id
        match_id = self.matchModel.record(currentIndex).value("match_id").toString()
        
        # filter penalties taken by players who were in lineup for match (match_id)
        self.model.setFilter(QString("player IN (SELECT player FROM lineup_list WHERE matchup IN "
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

        # enable navigation buttons and data entry widgets if table is non-empty
        if self.model.rowCount():
            self.teamSelect.setEnabled(True)
            self.playerSelect.setEnabled(True)
            self.foulSelect.setEnabled(True)
            self.penoutcomeSelect.setEnabled(True)
            self.pentimeEdit.setEnabled(True)
            
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            self.nextEntry.setEnabled(True)
            self.lastEntry.setEnabled(True)      

    def enableAndFilterRounds(self, widget):
        """Enables Rounds combobox and filters its contents based on Competition selection.
        
        Argument:
        widget -- data widget object (roundSelect)
        """
        widget.blockSignals(True)

        # enable widget if not enabled already
        if not widget.isEnabled():
            widget.setEnabled(True)
        
        # widget model
        widgetModel = widget.model()
        # Competitions model
        compModel = self.compModel
        
        # clear filter for widget model
        widgetModel.setFilter(QString())
        
        # get current index from Competition combobox
        # get competition ID
        currentIndex = self.compSelect.currentIndex()
        competition_id = compModel.record(currentIndex).value("competition_id").toString()
        
        # filter widget model on competition ID using match_list table
        # therefore we only access matchdays currently entered in database
        widgetModel.setFilter(QString("round_id IN "
                "(SELECT round_id FROM match_list WHERE competition_id = %1)").arg(competition_id))
        
        # set current index of widget to -1
        widget.setCurrentIndex(-1)
        widget.blockSignals(False)
                
    def enableAndFilterMatches(self, widget):
        """Enables Match combobox and filters its contents based on matchday (Rounds) selection.
        
        Argument:
        widget -- data widget object (matchSelect)
        """
        widget.blockSignals(True)
        
        # enable widget if not enabled already        
        if not widget.isEnabled():
            widget.setEnabled(True)
            
        # widget model
        widgetModel = widget.model()
        # Rounds model
        roundModel = self.roundModel
        compModel = self.compModel
        
        # clear filter for widget model
        widgetModel.setFilter(QString())
        
        # get current index from Rounds combobox
        # get round ID
        currentIndex = self.roundSelect.currentIndex()
        round_id = roundModel.record(currentIndex).value("round_id").toString()
        
        # get current index from Competition combobox
        # get competition ID
        currentIndex = self.compSelect.currentIndex()
        competition_id = compModel.record(currentIndex).value("competition_id").toString()
        
        # filter widget model on round ID and competition ID
        widgetModel.setFilter(QString("round_id = %1 AND competition_id = %2").arg(round_id, competition_id))
 
        # set current index of widget to -1
        widget.setCurrentIndex(-1)
        widget.blockSignals(False)
 
    def enableStoppageTime(self, widget):
        """Enables stoppage time widget. 
        
        Enables widget if one of the following conditions are met:
            (1) minutes elapsed are nonzero and divisible by 45
            (2) minutes elapsed exceed 90 and are divisible by 15
        Argument:
        widget -- data widget object (stoppageEdit)
        
        """
        minutes = self.pentimeEdit.text().toInt()[0]
        if (minutes and not (minutes % 45)) or (minutes > 90 and not (minutes % 15)):
            widget.setEnabled(True)
        else:
            widget.setDisabled(True)


class PenShootoutEntryDlg(QDialog, ui_penshootoutentry.Ui_PenShootoutEntryDlg):
    """Implements penalty shootout data entry dialog, and accesses and writes to PenaltyShootouts and PenShootoutOpeners tables.
    
   """
   
    def __init__(self, parent=None):
        super(PenShootoutEntryDlg, self).__init__(parent)
        self.setupUi(self)
    
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
#        row = self.mapper.currentIndex()
#        if self.isDirty(row):
#            if MsgPrompts.SaveDiscardOptionPrompt(self):
#                if not self.mapper.submit():
#                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
        QDialog.accept(self)
