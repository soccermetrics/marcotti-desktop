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
from FmrdLib import Constants
from FmrdLib.CustomDelegates import *
from FmrdLib.CustomModels import *

"""Contains classes that implement match event entry forms to main tables of FMRD. 

Classes:
goalEntryDlg -- data entry to Goals table
penaltyEntryDlg -- data entry to Penalties table
offenseEntryDlg -- data entry to Offenses table
subsEntryDlg -- data entry to Substitutions table
switchEntryDlg -- data entry to Switch Positions table
"""

# goalEntryDlg: Goal entry dialog (run of play)
class goalEntryDlg(QDialog, ui_goalentry.Ui_goalEntryDlg):
    """Implements goal data entry dialog, and accesses and writes to Goals table.
    
    This dialog accepts data on goals scored in the run of play. Penalty kick events
    are handled in the penaltyEntryDlg class.  Goals are attributed to a team but can
    be scored by any player in the match lineup, thus own goals can be recorded.
    
    """
    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID, TEAM_ID, LINEUP_ID, BODY_ID, PLAY_ID, TIME, STIME = range(7)

    def __init__(self, parent=None):
        """Constructor for goalEntryDlg class."""
        super(goalEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        MCH_ID = CMP_ID = RND_ID = 0
        TEAM = PLAY = BODY = 1
        SORT_NAME = 7

        #
        # Define comboboxes used to filter Goals table
        # Ensure that user only sees Goals for specific match
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
        # Define Goals data entry
        #
        
        # 
        # underlying database model (tbl_goals)
        # because of foreign keys, instantiate QSqlRelationalTableModel and define relations to it        
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_goals")
        self.model.setRelation(goalEntryDlg.TEAM_ID, QSqlRelation("tbl_teams", "team_id", "tm_name"))
        self.model.setRelation(goalEntryDlg.LINEUP_ID, QSqlRelation("lineup_list", "lineup_id", "player"))
        self.model.setRelation(goalEntryDlg.BODY_ID, QSqlRelation("tbl_goalstrikes", "gtstype_id", "gts_desc"))
        self.model.setRelation(goalEntryDlg.PLAY_ID, QSqlRelation("tbl_goalevents", "gtetype_id", "gte_desc"))
        self.model.setSort(goalEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        goalDelegate = GenericDelegate(self)
        goalDelegate.insertColumnDelegate(goalEntryDlg.TEAM_ID, EventTeamComboBoxDelegate(self))
        goalDelegate.insertColumnDelegate(goalEntryDlg.LINEUP_ID, GoalPlayerComboBoxDelegate(self))
        self.mapper.setItemDelegate(goalDelegate)        

        # set up Team combobox
        self.teamModel = self.model.relationModel(goalEntryDlg.TEAM_ID)
        self.teamModel.setSort(TEAM, Qt.AscendingOrder)
        self.teamSelect.setModel(self.teamModel)
        self.teamSelect.setModelColumn(self.teamModel.fieldIndex("tm_name"))
        self.teamSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.teamSelect, goalEntryDlg.TEAM_ID)
        
        # set up Player combobox
        self.playerModel = self.model.relationModel(goalEntryDlg.LINEUP_ID)
        self.playerModel.setSort(SORT_NAME,  Qt.AscendingOrder)
        self.playerSelect.setModel(self.playerModel)
        self.playerSelect.setModelColumn(self.playerModel.fieldIndex("player"))
        self.playerSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.playerSelect, goalEntryDlg.LINEUP_ID)

        # relation model for Goal Type combobox
        self.goaltypeModel = self.model.relationModel(goalEntryDlg.BODY_ID)
        self.goaltypeModel.setSort(BODY, Qt.AscendingOrder)
        self.goaltypeSelect.setModel(self.goaltypeModel)
        self.goaltypeSelect.setModelColumn(self.goaltypeModel.fieldIndex("gts_desc"))
        self.goaltypeSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.goaltypeSelect, goalEntryDlg.BODY_ID)        
        
        # relation model for Goal Event combobox
        self.goaleventModel = self.model.relationModel(goalEntryDlg.PLAY_ID)
        self.goaleventModel.setSort(PLAY, Qt.AscendingOrder)
        self.goaleventSelect.setModel(self.goaleventModel)
        self.goaleventSelect.setModelColumn(self.goaleventModel.fieldIndex("gte_desc"))
        self.goaleventSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.goaleventSelect, goalEntryDlg.PLAY_ID)        

        # map other widgets on form
        self.mapper.addMapping(self.goalID_display, goalEntryDlg.ID)
        self.mapper.addMapping(self.goaltimeEdit, goalEntryDlg.TIME)
        self.mapper.addMapping(self.stoppageEdit, goalEntryDlg.STIME)
        
        #
        # Disable data entry boxes
        #
        
        # disable all comboboxes and line edits 
        # EXCEPT competition combobox upon opening
        self.roundSelect.setDisabled(True)
        self.matchSelect.setDisabled(True)
        
        self.teamSelect.setDisabled(True)
        self.playerSelect.setDisabled(True)
        self.goaleventSelect.setDisabled(True)
        self.goaltypeSelect.setDisabled(True)
        self.goaltimeEdit.setDisabled(True)
        self.stoppageEdit.setDisabled(True)
        
        # disable navigation buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        
        # disable add and delete entry buttons
        self.addEntry.setDisabled(True)
        self.deleteEntry.setDisabled(True)
        
        #
        # Signals/Slots configuration
        #
        
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(goalEntryDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(goalEntryDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(goalEntryDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(goalEntryDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)        
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        
        self.connect(self.compSelect, SIGNAL("currentIndexChanged(int)"), lambda: self.enableAndFilterRounds(self.roundSelect))
        self.connect(self.roundSelect, SIGNAL("currentIndexChanged(int)"),  lambda: self.enableAndFilterMatches(self.matchSelect))
        self.connect(self.matchSelect, SIGNAL("currentIndexChanged(int)"), self.filterGoals)
        self.connect(self.goaltimeEdit, SIGNAL("textChanged()"),  lambda: self.enableStoppageTime(self.stoppageEdit))
   
   
    def accept(self):
        """Submits changes to database and closes window."""
        self.mapper.submit()
        QDialog.accept(self)
   
    def saveRecord(self, where):
        """Submits changes to database, navigates through form, and resets subforms."""
        row = self.mapper.currentIndex()
        self.mapper.submit()
        
        if where == goalEntryDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == goalEntryDlg.PREV:
            row -= 1
            if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)   
            if row == 0:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
        elif where == goalEntryDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row == self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
        elif where == goalEntryDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
            
        self.mapper.setCurrentIndex(row)

    def deleteRecord(self):
        """Deletes record from database upon user confirmation."""
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

    def addRecord(self):
        """Adds new record at end of entry list."""
        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(goal_id) FROM tbl_goals"))
        if query.next():
            maxGoalID= query.value(0).toInt()[0]
            if not maxGoalID:
                goal_id = Constants.MinGoalID
            else:
                self.mapper.submit()
                goal_id= QString()
                goal_id.setNum(maxGoalID+1)                  
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        
        # assign value to goalID field
        self.goalID_display.setText(goal_id)
        
        # disable navigation button
        self.prevEntry.setEnabled(True)
        self.firstEntry.setEnabled(True)
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)        
        
        # enable data entry widgets if table is non-empty
        self.teamSelect.setEnabled(True)
        self.playerSelect.setEnabled(True)
        self.goaleventSelect.setEnabled(True)
        self.goaltypeSelect.setEnabled(True)
        self.goaltimeEdit.setEnabled(True)
        
        # disable stoppage time edit box upon opening
        # set default stoppage time
        # clear match time
        self.stoppageEdit.setDisabled(True)
        self.stoppageEdit.setText("0")
        self.goaltimeEdit.setText(QString())

    def filterGoals(self):
        """Sets filter for Goals table based on Match selection."""
        
        # enable add/delete entry buttons
        self.addEntry.setEnabled(True)
        self.deleteEntry.setEnabled(True)

        # clear filter
        self.model.setFilter(QString())
        
        # get current index
        currentIndex = self.matchSelect.currentIndex()
        
        # get match_id
        match_id = self.matchModel.record(currentIndex).value("match_id").toString()
        
        # filter goals to those scored by players who were in the lineup for the match (match_id)
        self.model.setFilter(QString("player IN (SELECT player FROM lineup_list WHERE matchup IN "
                                                    "(SELECT matchup FROM match_list WHERE match_id = %1))").arg(match_id))
        self.mapper.toFirst()        
        
        # enable add/delete buttons
        self.addEntry.setEnabled(True)
        self.deleteEntry.setEnabled(True)

        # enable navigation buttons and data entry widgets if table is non-empty
        if self.model.rowCount():
            self.teamSelect.setEnabled(True)
            self.playerSelect.setEnabled(True)
            self.goaleventSelect.setEnabled(True)
            self.goaltypeSelect.setEnabled(True)
            self.goaltimeEdit.setEnabled(True)
            
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
 

    # Method: enableStoppageTime
    #
    # Enable stoppage time widget if minutes elapsed are nonzero and divisible by 45
    #       OR minutes elapsed exceed 90 and are divisible by 15 (handle extra time period)
    def enableStoppageTime(self, widget):
        """Enables stoppage time widget. 
        
        Enables widget if one of the following conditions are met:
            (1) minutes elapsed are nonzero and divisible by 45
            (2) minutes elapsed exceed 90 and are divisible by 15
        Argument:
        widget -- data widget object (stoppageEdit)
        
        """
        minutes = self.goaltimeEdit.text().toInt()[0]
        if (minutes and not (minutes % 45)) or (minutes > 90 and not (minutes % 15)):
            widget.setEnabled(True)


class penaltyEntryDlg(QDialog, ui_penaltyentry.Ui_penaltyEntryDlg):
    """Implements penalty kick data entry dialog, and accesses and writes to Penalties table.
    
    This dialog accepts data on penalty kick events during a match.
   """
    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID, LINEUP_ID, FOUL_ID, OUTCOME_ID, TIME, STIME = range(6)
    
    def __init__(self, parent=None):
        """Constructor for penaltyEntryDlg class."""
        super(penaltyEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        CMP_ID = RND_ID = MCH_ID = TM_ID = 0
        TEAM = FOUL = OUTCOME = 1
        SORT_NAME = 7

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
        self.model.setRelation(penaltyEntryDlg.LINEUP_ID, QSqlRelation("lineup_list", "lineup_id", "player"))
        self.model.setRelation(penaltyEntryDlg.FOUL_ID, QSqlRelation("tbl_fouls", "foul_id", "foul_desc"))
        self.model.setRelation(penaltyEntryDlg.OUTCOME_ID, QSqlRelation("tbl_penoutcomes", "penoutcome_id", "po_desc"))
        self.model.setSort(penaltyEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        penaltyDelegate = GenericDelegate(self)
        penaltyDelegate.insertColumnDelegate(penaltyEntryDlg.LINEUP_ID, EventPlayerComboBoxDelegate(self))
        self.mapper.setItemDelegate(penaltyDelegate)        

        # set up Player combobox
        self.playerModel = self.model.relationModel(penaltyEntryDlg.LINEUP_ID)
        self.playerModel.setSort(SORT_NAME,  Qt.AscendingOrder)
        self.playerSelect.setModel(self.playerModel)
        self.playerSelect.setModelColumn(self.playerModel.fieldIndex("player"))
        self.playerSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.playerSelect, penaltyEntryDlg.LINEUP_ID)

        # relation model for Foul combobox
        self.foulModel = self.model.relationModel(penaltyEntryDlg.FOUL_ID)
        self.foulModel.setSort(FOUL, Qt.AscendingOrder)
        self.foulSelect.setModel(self.foulModel)
        self.foulSelect.setModelColumn(self.foulModel.fieldIndex("foul_desc"))
        self.foulSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.foulSelect, penaltyEntryDlg.FOUL_ID)        
        
        # relation model for Penalty Outcome combobox
        self.outcomeModel = self.model.relationModel(penaltyEntryDlg.OUTCOME_ID)
        self.outcomeModel.setSort(OUTCOME, Qt.AscendingOrder)
        self.penoutcomeSelect.setModel(self.outcomeModel)
        self.penoutcomeSelect.setModelColumn(self.outcomeModel.fieldIndex("po_desc"))
        self.penoutcomeSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.penoutcomeSelect, penaltyEntryDlg.OUTCOME_ID)        

        # map other widgets on form
        self.mapper.addMapping(self.penaltyID_display, penaltyEntryDlg.ID)
        self.mapper.addMapping(self.pentimeEdit, penaltyEntryDlg.TIME)
        self.mapper.addMapping(self.stoppageEdit, penaltyEntryDlg.STIME)
        
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
        
        # disable add and delete entry buttons
        self.addEntry.setDisabled(True)
        self.deleteEntry.setDisabled(True)
        
        #
        # Signals/Slots configuration
        #
        
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(penaltyEntryDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(penaltyEntryDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(penaltyEntryDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(penaltyEntryDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)        
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        
        self.connect(self.compSelect, SIGNAL("currentIndexChanged(int)"), lambda: self.enableAndFilterRounds(self.roundSelect))
        self.connect(self.roundSelect, SIGNAL("currentIndexChanged(int)"),  lambda: self.enableAndFilterMatches(self.matchSelect))
        self.connect(self.matchSelect, SIGNAL("currentIndexChanged(int)"), self.filterPenaltiesAndTeams)
        self.connect(self.teamSelect, SIGNAL("currentIndexChanged(int)"), self.enablePlayerData)        
        self.connect(self.pentimeEdit, SIGNAL("textChanged()"),  lambda: self.enableStoppageTime(self.stoppageEdit))

    def accept(self):
        """Submits changes to database and closes window."""
        ok = self.mapper.submit()
        QDialog.accept(self)
   
    def saveRecord(self, where):
        """Submits changes to database, navigates through form, and resets subforms."""
        row = self.mapper.currentIndex()
        self.mapper.submit()
        
        if where == penaltyEntryDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == penaltyEntryDlg.PREV:
            row -= 1
            if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)   
            if row == 0:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
        elif where == penaltyEntryDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row == self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
        elif where == penaltyEntryDlg.LAST:
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

    def deleteRecord(self):
        """Deletes record from database upon user confirmation."""
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

    def addRecord(self):
        """Adds new record at end of entry list."""        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(penalty_id) FROM tbl_penalties"))
        if query.next():
            maxPenaltyID = query.value(0).toInt()[0]
            if not maxPenaltyID:
                penalty_id = Constants.MinPenaltyID
            else:
                self.mapper.submit()
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

    def enablePlayerData(self):
        """Enables player, offense, and card comboboxes if not enabled already."""
        
        self.playerSelect.setEnabled(True)
        self.foulSelect.setEnabled(True)
        self.penoutcomeSelect.setEnabled(True)
        self.pentimeEdit.setEnabled(True)

    def filterPenaltiesAndTeams(self):
        """Filters Penalties table to display all entries from selected match, and filters Teams combobox down to the two participants."""
        
        # enable add/delete entry buttons
        self.addEntry.setEnabled(True)
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
        minutes = self.goaltimeEdit.text().toInt()[0]
        if (minutes and not (minutes % 45)) or (minutes > 90 and not (minutes % 15)):
            widget.setEnabled(True)


class offenseEntryDlg(QDialog, ui_offenseentry.Ui_offenseEntryDlg):
    """Implements bookable offense data entry dialog, and accesses and writes to Offenses table.
    
    This dialog accepts data on disciplinary incidents during a match.
   """

    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID, LINEUP_ID, FOUL_ID, CARD_ID, TIME, STIME = range(6)

    def __init__(self, parent=None):
        """Constructor for offenseEntryDlg class."""
        super(offenseEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        CMP_ID = RND_ID = MCH_ID = TM_ID = 0
        TEAM = FOUL = CARD = 1
        SORT_NAME = 7

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
        # Define Offenses data entry
        #
        
        # 
        # underlying database model (tbl_offenses)
        # because of foreign keys, instantiate QSqlRelationalTableModel and define relations to it        
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_offenses")
        self.model.setRelation(offenseEntryDlg.LINEUP_ID, QSqlRelation("lineup_list", "lineup_id", "player"))
        self.model.setRelation(offenseEntryDlg.FOUL_ID, QSqlRelation("tbl_fouls", "foul_id", "foul_desc"))
        self.model.setRelation(offenseEntryDlg.CARD_ID, QSqlRelation("tbl_cards", "card_id", "card_type"))
        self.model.setSort(offenseEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        foulDelegate = GenericDelegate(self)
        foulDelegate.insertColumnDelegate(offenseEntryDlg.LINEUP_ID, EventPlayerComboBoxDelegate(self))
        self.mapper.setItemDelegate(foulDelegate)        

        # set up Player combobox
        self.playerModel = self.model.relationModel(offenseEntryDlg.LINEUP_ID)
        self.playerModel.setSort(SORT_NAME,  Qt.AscendingOrder)
        self.playerSelect.setModel(self.playerModel)
        self.playerSelect.setModelColumn(self.playerModel.fieldIndex("player"))
        self.playerSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.playerSelect, offenseEntryDlg.LINEUP_ID)

        # relation model for Foul combobox
        self.foulModel = self.model.relationModel(offenseEntryDlg.FOUL_ID)
        self.foulModel.setSort(FOUL, Qt.AscendingOrder)
        self.foulSelect.setModel(self.foulModel)
        self.foulSelect.setModelColumn(self.foulModel.fieldIndex("foul_desc"))
        self.foulSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.foulSelect, offenseEntryDlg.FOUL_ID)        
        
        # relation model for Card combobox
        self.cardModel = self.model.relationModel(offenseEntryDlg.CARD_ID)
        self.cardModel.setSort(CARD, Qt.AscendingOrder)
        self.cardSelect.setModel(self.cardModel)
        self.cardSelect.setModelColumn(self.cardModel.fieldIndex("card_type"))
        self.cardSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.cardSelect, offenseEntryDlg.CARD_ID)        

        # map other widgets on form
        self.mapper.addMapping(self.offenseID_display, offenseEntryDlg.ID)
        self.mapper.addMapping(self.foultimeEdit, offenseEntryDlg.TIME)
        self.mapper.addMapping(self.stoppageEdit, offenseEntryDlg.STIME)
        
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
        self.cardSelect.setDisabled(True)
        self.foultimeEdit.setDisabled(True)
        self.stoppageEdit.setDisabled(True)
        
        # disable navigation buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        
        # disable add and delete entry buttons
        self.addEntry.setDisabled(True)
        self.deleteEntry.setDisabled(True)
        
        #
        # Signals/Slots configuration
        #
        
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(offenseEntryDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(offenseEntryDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(offenseEntryDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(offenseEntryDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)        
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)        
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        
        self.connect(self.compSelect, SIGNAL("currentIndexChanged(int)"), lambda: self.enableAndFilterRounds(self.roundSelect))
        self.connect(self.roundSelect, SIGNAL("currentIndexChanged(int)"),  lambda: self.enableAndFilterMatches(self.matchSelect))
        self.connect(self.matchSelect, SIGNAL("currentIndexChanged(int)"), self.filterOffensesAndTeams)
        self.connect(self.teamSelect, SIGNAL("currentIndexChanged(int)"), self.filterPlayers)
        self.connect(self.foultimeEdit, SIGNAL("textChanged()"),  lambda: self.enableStoppageTime(self.stoppageEdit))

    def accept(self):
        """Submits changes to database and closes window."""
        ok = self.mapper.submit()
        QDialog.accept(self)
   
    def saveRecord(self, where):
        """Submits changes to database, navigates through form, and resets subforms."""
        row = self.mapper.currentIndex()
        
        ok = self.mapper.submit()
        if not ok:
            print self.model.lastError().text()
        
        if where == offenseEntryDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == offenseEntryDlg.PREV:
            row -= 1
            if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)   
            if row == 0:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
        elif where == offenseEntryDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row == self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
        elif where == offenseEntryDlg.LAST:
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

    def deleteRecord(self):
        """Deletes record from database upon user confirmation."""
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

    def addRecord(self):
        """Adds new record at end of entry list."""
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(offense_id) FROM tbl_offenses"))
        if query.next():
            maxOffenseID = query.value(0).toInt()[0]
            if not maxOffenseID:
                offense_id = Constants.MinOffenseID
            else:
                self.mapper.submit()
                offense_id = QString()
                offense_id.setNum(maxOffenseID+1)       
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)

        # assign value to goalID field
        self.offenseID_display.setText(offense_id)
        
        # disable navigation button
        self.prevEntry.setEnabled(True)
        self.firstEntry.setEnabled(True)
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)        
        
        # set Team combobox to blank item
        self.teamSelect.setEnabled(True)
        self.teamSelect.setCurrentIndex(-1)
        
        # disable stoppage time edit box upon opening
        # set default stoppage time
        # clear match time
        self.stoppageEdit.setDisabled(True)
        self.stoppageEdit.setText("0")
        self.foultimeEdit.setText(QString())

    def filterOffensesAndTeams(self):
        """Filters Offenses table down to entries from selected match, and filters Teams combobox down to both participants."""
#        print "Calling filterOffensesAndTeams()"
        # enable add/delete entry buttons
        self.addEntry.setEnabled(True)
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
        if self.model.rowCount() > 0:
            self.teamSelect.setEnabled(True)            
            self.playerSelect.setEnabled(True)
            self.foulSelect.setEnabled(True)
            self.cardSelect.setEnabled(True)
            self.foultimeEdit.setEnabled(True)
            
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            self.nextEntry.setEnabled(True)
            self.lastEntry.setEnabled(True)      

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
        self.cardSelect.setEnabled(True)
        self.foultimeEdit.setEnabled(True)
        self.stoppageEdit.setEnabled(True)
        
        # set current index to -1
        self.playerSelect.setCurrentIndex(-1)        
        self.playerSelect.blockSignals(False)

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
        minutes = self.goaltimeEdit.text().toInt()[0]
        if (minutes and not (minutes % 45)) or (minutes > 90 and not (minutes % 15)):
            widget.setEnabled(True)


class subsEntryDlg(QDialog, ui_subsentry.Ui_subsEntryDlg):
    """Implements substitutions data entry dialog, and accesses and writes to Substitutions table and In(Out)Substitutions linking tables.
    
    This dialog accepts data on substitution events during a match. 
   """
    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID, TIME, STIME = range(3)
    
    def __init__(self, parent=None):
        """Constructor for subsEntryDlg class."""
        super(subsEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define local parameters
        CMP_ID = RND_ID = MCH_ID = TM_ID = 0
        TEAM = IN_ID = OUT_ID = 1
        SORT_NAME = 7
        
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
        # Define Substitutions data entry
        #
        
        # define underlying database model (tbl_substitutions)
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_substitutions")
        self.model.setSort(subsEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.subsID_display, subsEntryDlg.ID)
        self.mapper.addMapping(self.subtimeEdit, subsEntryDlg.TIME)
        self.mapper.addMapping(self.stoppageEdit, subsEntryDlg.STIME)

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
        self.inplayerMapper.setSubmitPolicy(QDataWidgetMapper.AutoSubmit)
        self.inplayerMapper.setModel(self.inplayerModel)
        inplayerDelegate = GenericDelegate(self)
        inplayerDelegate.insertColumnDelegate(IN_ID, SubInComboBoxDelegate(self))
        self.inplayerMapper.setItemDelegate(inplayerDelegate)
        self.inplayerMapper.addMapping(self.inplayerSelect, IN_ID)
        self.inplayerMapper.toFirst()
        
        # out substitution mapper
        self.outplayerMapper = QDataWidgetMapper(self)
        self.outplayerMapper.setSubmitPolicy(QDataWidgetMapper.AutoSubmit)
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
        self.roundSelect.setDisabled(True)
        self.matchSelect.setDisabled(True)
        
        self.teamSelect.setDisabled(True)
        self.inplayerSelect.setDisabled(True)
        self.outplayerSelect.setDisabled(True)
        self.subtimeEdit.setDisabled(True)
        self.stoppageEdit.setDisabled(True)
        
        # disable navigation buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        
        # disable add and delete entry buttons
        self.addEntry.setDisabled(True)
        self.deleteEntry.setDisabled(True)
        
        #
        # Signals/Slots configuration
        #

        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(subsEntryDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(subsEntryDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(subsEntryDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(subsEntryDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
#        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)           
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        
        self.connect(self.compSelect, SIGNAL("currentIndexChanged(int)"), lambda: self.enableAndFilterRounds(self.roundSelect))
        self.connect(self.roundSelect, SIGNAL("currentIndexChanged(int)"),  lambda: self.enableAndFilterMatches(self.matchSelect))        
        self.connect(self.matchSelect, SIGNAL("currentIndexChanged(int)"), self.filterSubstitutionsAndTeams)      
        self.connect(self.teamSelect, SIGNAL("currentIndexChanged(int)"), self.enablePlayerData)                
        self.connect(self.inplayerSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.updateLinkingTable(self.inplayerMapper, self.inplayerSelect))
        self.connect(self.outplayerSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.updateLinkingTable(self.outplayerMapper, self.outplayerSelect))
        self.connect(self.subtimeEdit, SIGNAL("textChanged()"),  lambda: self.enableStoppageTime(self.stoppageEdit))
 
    def accept(self):
        """Submits changes to database and closes window."""
        ok = self.mapper.submit()
        QDialog.accept(self)
   
    def saveRecord(self, where):
        """Submits changes to database, navigates through form, and resets subforms."""
        row = self.mapper.currentIndex()
        self.mapper.submit()
        
        if where == subsEntryDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == subsEntryDlg.PREV:
            row -= 1
            if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)   
            if row == 0:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
        elif where == subsEntryDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row == self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
        elif where == subsEntryDlg.LAST:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            row = self.model.rowCount() - 1
            
        self.teamSelect.blockSignals(True)
        
        self.mapper.setCurrentIndex(row)
        
        subs_id = self.subsID_display.text()
        self.refreshSubForms(subs_id)        

        self.refreshTeamBox()
        self.teamSelect.blockSignals(False)

    def addRecord(self):
        """Adds new record at end of entry list."""
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(subs_id) FROM tbl_substitutions"))
        if query.next():
            maxSubsID = query.value(0).toInt()[0]
            if not maxSubsID:
                subs_id = Constants.MinSubstitutionID
            else:
                self.mapper.submit()
                subs_id = QString()
                subs_id.setNum(maxSubsID+1)                  
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        
        # assign value to subsID field
        self.subsID_display.setText(subs_id)
        
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
        self.subtimeEdit.setText(QString())
        
        # refresh subforms
        self.refreshSubForms(subs_id)        

    def refreshTeamBox(self):
        """Sets index of team box so that it corresponds with selected player."""
#        print "Calling refreshTeamBox()"
        
        compName = self.compSelect.currentText()
        roundName = self.roundSelect.currentText()
        playerName = self.inplayerSelect.currentText()
        
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

    def enablePlayerData(self):
        """Enables player, offense, and card comboboxes if not enabled already."""
        # enable data entry widgets if table is non-empty
        self.inplayerSelect.setEnabled(True)
        self.outplayerSelect.setEnabled(True)
        self.subtimeEdit.setEnabled(True)
        
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

    def filterInSubs(self):
        """Filters In Player combobox based on match and team selections.
        
        Players eligible for substitutions into match are lineup entries who meet all conditions:
            -- same match
            -- same team
            -- not starting
            -- not already subbed in
            
        """
#        print "Calling filterInSubs()"
        
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

        # get team_id from tbl_teams
        teamQuery = QSqlQuery()
        teamQuery.prepare("SELECT team_id FROM tbl_teams WHERE tm_name = ?")
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
                                   "NOT lp_starting AND match_id = %2 AND team_id = %3)").arg(lineup_id).arg(match_id).arg(team_id)

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
#        print "Calling filterOutSubs()"
        
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

        # get team_id from tbl_teams
        teamQuery = QSqlQuery()
        teamQuery.prepare("SELECT team_id FROM tbl_teams WHERE tm_name = ?")
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
                               "AND lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE lp_starting AND match_id = %2 AND team_id = %3) "
                               "OR (lineup_id IN (SELECT lineup_id FROM tbl_insubstitutions WHERE lineup_id <> %1) AND "
                               "lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE NOT lp_starting AND match_id = %2 AND team_id = %3))"
                               ).arg(lineup_id).arg(match_id).arg(team_id)
            
        # filter Player combobox
        lineupListModel.setFilter(filterString)

        # set current index to item that matches data value
        self.outplayerSelect.setCurrentIndex(self.outplayerSelect.findText(playerName, Qt.MatchExactly))
        
        self.outplayerSelect.blockSignals(False)

    def filterSubstitutionsAndTeams(self):
        """Filters Substitutions table from match selection."""
        
        # enable add/delete entry buttons
        self.addEntry.setEnabled(True)
        self.deleteEntry.setEnabled(True)

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
            self.inplayerSelect.setEnabled(True)
            self.outplayerSelect.setEnabled(True)
            self.subtimeEdit.setEnabled(True)
            
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
        minutes = self.subtimeEdit.text().toInt()[0]
        if (minutes and not (minutes % 45)) or (minutes > 90 and not (minutes % 15)):
            widget.setEnabled(True)


# switchEntryDlg: Position switch entry dialog
class switchEntryDlg(QDialog, ui_switchentry.Ui_switchEntryDlg):
    """Implements position switch data entry dialog, and accesses and writes to SwitchPositions table.
    
    This dialog accepts data on position switch events during a match. It is primarily focused on
    tracking forced changes of in-field players due to an expulsion of a goalkeeper, but it can
    track tactical position changes as well.
   """
    FIRST,  PREV,  NEXT,  LAST = range(4)
    ID, LINEUP_ID, POS_ID, TIME, STIME = range(5)
    
    def __init__(self, parent=None):
        super(switchEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define local parameters
        CMP_ID = RND_ID = MCH_ID = TM_ID = 0
        TEAM = POS = 1
        SORT_NAME = 7
        
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
        # Define Switch Positions data entry
        #
        
        # underlying database model (tbl_switchpositions)
        # because of foreign keys, instantiate QSqlRelationalTableModel and define relations to it        
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_switchpositions")
        self.model.setRelation(switchEntryDlg.LINEUP_ID, QSqlRelation("lineup_list", "lineup_id", "player"))
        self.model.setRelation(switchEntryDlg.POS_ID, QSqlRelation("positions_list", "position_id", "position_name"))
        self.model.setSort(switchEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define mapper
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        switchDelegate = GenericDelegate(self)
        switchDelegate.insertColumnDelegate(switchEntryDlg.LINEUP_ID, SwitchPlayerComboBoxDelegate(self))
        self.mapper.setItemDelegate(switchDelegate)        

        # relation model for Player combobox
        self.playerModel = self.model.relationModel(switchEntryDlg.LINEUP_ID)
        self.playerModel.setSort(SORT_NAME,  Qt.AscendingOrder)
        self.playerSelect.setModel(self.playerModel)
        self.playerSelect.setModelColumn(self.playerModel.fieldIndex("player"))
        self.playerSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.playerSelect, switchEntryDlg.LINEUP_ID)

        # relation model for Positions combobox
        self.positionModel = self.model.relationModel(switchEntryDlg.POS_ID)
        self.positionModel.setSort(POS, Qt.AscendingOrder)
        self.newPositionSelect.setModel(self.positionModel)
        self.newPositionSelect.setModelColumn(self.positionModel.fieldIndex("position_name"))
        self.newPositionSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.newPositionSelect, switchEntryDlg.POS_ID)        
        
        # map other widgets on form
        self.mapper.addMapping(self.switchID_display, switchEntryDlg.ID)
        self.mapper.addMapping(self.switchtimeEdit, switchEntryDlg.TIME)
        self.mapper.addMapping(self.stoppageEdit, switchEntryDlg.STIME)

        #
        # Disable data entry boxes
        #
        
        # disable all comboboxes and line edits 
        # EXCEPT competition combobox upon opening
        self.roundSelect.setDisabled(True)
        self.matchSelect.setDisabled(True)
        
        self.teamSelect.setDisabled(True)
        self.playerSelect.setDisabled(True)
        self.newPositionSelect.setDisabled(True)
        self.switchtimeEdit.setDisabled(True)
        self.stoppageEdit.setDisabled(True)
        
        # disable navigation buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        
        # disable add and delete entry buttons
        self.addEntry.setDisabled(True)
        self.deleteEntry.setDisabled(True)
        
        #
        # Signals/Slots configuration
        #

        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(switchEntryDlg.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(switchEntryDlg.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(switchEntryDlg.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(switchEntryDlg.LAST))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)           
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        
        self.connect(self.compSelect, SIGNAL("currentIndexChanged(int)"), lambda: self.enableAndFilterRounds(self.roundSelect))
        self.connect(self.roundSelect, SIGNAL("currentIndexChanged(int)"),  lambda: self.enableAndFilterMatches(self.matchSelect))        
        self.connect(self.matchSelect, SIGNAL("currentIndexChanged(int)"), self.filterSwitchesAndTeams)      
        self.connect(self.teamSelect, SIGNAL("currentIndexChanged(int)"), self.filterPlayers)                
        self.connect(self.switchtimeEdit, SIGNAL("textChanged()"),  lambda: self.enableStoppageTime(self.stoppageEdit))        
        
    def accept(self):
        """Submits changes to database and closes window."""
        ok = self.mapper.submit()
        QDialog.accept(self)
   
    def saveRecord(self, where):
        """Submits changes to database, navigates through form, and resets subforms."""
        row = self.mapper.currentIndex()
        self.mapper.submit()
        
        if where == switchEntryDlg.FIRST:
            self.firstEntry.setDisabled(True)
            self.prevEntry.setDisabled(True)
            if not self.nextEntry.isEnabled():
                self.nextEntry.setEnabled(True)
                self.lastEntry.setEnabled(True)
            row = 0
        elif where == switchEntryDlg.PREV:
            row -= 1
            if not self.nextEntry.isEnabled():
                    self.nextEntry.setEnabled(True)
                    self.lastEntry.setEnabled(True)   
            if row == 0:
                self.firstEntry.setDisabled(True)
                self.prevEntry.setDisabled(True)                
        elif where == switchEntryDlg.NEXT:
            row += 1
            if not self.prevEntry.isEnabled():
                self.prevEntry.setEnabled(True)
                self.firstEntry.setEnabled(True)
            if row == self.model.rowCount() - 1:
                self.nextEntry.setDisabled(True)
                self.lastEntry.setDisabled(True)
        elif where == switchEntryDlg.LAST:
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
        
    def deleteRecord(self):
        """Deletes record from database upon user confirmation."""
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

    def addRecord(self):
        """Adds new record at end of entry list."""        
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            self.mapper.submit()
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(switch_id) FROM tbl_switchpositions"))
        if query.next():
            maxSwitchID = query.value(0).toInt()[0]
            if not maxSwitchID:
                switch_id = Constants.MinSwitchID
            else:
                self.mapper.submit()
                switch_id = QString()
                switch_id.setNum(maxSwitchID+1)                  
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        
        # assign value to switchID field
        self.switchID_display.setText(switch_id)
        
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
        self.switchtimeEdit.setText(QString())
        
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
        
    # Method: filterPlayers
    #
    # Enable player, offense, and card comboboxes if not enabled already
    #
    #  User will select players who have started (and not been substituted) 
    #  and non-starting players who have been substituted into the match.
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
        
        # get team_id by querying tbl_teams with team name
        team_id = "-1"
        teamQuery = QSqlQuery()
        teamQuery.prepare("SELECT team_id FROM tbl_teams WHERE tm_name = ?")
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
                               "AND lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE lp_starting AND match_id = %2 AND team_id = %3) "
                               "OR (lineup_id IN (SELECT lineup_id FROM tbl_insubstitutions WHERE lineup_id <> %1) AND "
                               "lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE NOT lp_starting AND match_id = %2 AND team_id = %3))"
                               ).arg(lineup_id).arg(match_id).arg(team_id)
        
        # filter Players combobox
        lineupListModel.setFilter(filterString)
                
        # enable comboboxes if not enabled already
        self.playerSelect.setEnabled(True)
        self.newPositionSelect.setEnabled(True)
        self.switchtimeEdit.setEnabled(True)
        
        # set current index to -1
        self.playerSelect.setCurrentIndex(-1)        
        self.playerSelect.blockSignals(False)

    def filterSwitchesAndTeams(self):
        """Filters SwitchPositions table from match selection."""
        # enable add/delete entry buttons
        self.addEntry.setEnabled(True)
        self.deleteEntry.setEnabled(True)

        # block signals from team combobox
        self.teamSelect.blockSignals(True)
        
        # clear filter
        self.model.setFilter(QString())
        
        # get current index
        currentIndex = self.matchSelect.currentIndex()
        
        # get match_id
        match_id = self.matchModel.record(currentIndex).value("match_id").toString()
        
        # filter position switches of players who were in lineup for match (match_id)
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
            self.newPositionSelect.setEnabled(True)
            self.switchtimeEdit.setEnabled(True)
            self.stoppageEdit.setEnabled(True)
            
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
        minutes = self.switchtimeEdit.text().toInt()[0]
        if (minutes and not (minutes % 45)) or (minutes > 90 and not (minutes % 15)):
            widget.setEnabled(True)
        
