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

"""Contains custom and generic delegates used by various dialogs of FMRD tool.

Classes:
AwayMgrComboBoxDelegate -- delegate for Away Manager combobox
AwayTeamComboBoxDelegate -- delegate for Away Team combobox
CheckBoxDelegate -- delegate for CheckBox widgets
CountryComboBoxDelegate -- delegate for Country comboboxes
EventPlayerComboBoxDelegate -- delegate for Player combobox in Match Events dialogs
EventTeamComboBoxDelegate -- delegate for Team combobox in Match Events dialogs
GenericDelegate -- container class for array of custom delegates
GoalPlayerComboBoxDelegate -- delegate for Player combobox in Goals dialog
HomeMgrComboBoxDelegate -- delegate for Home Manager combobox
HomeTeamComboBoxDelegate -- delegate for Home Team combobox
LineupPlayerComboBoxDelegate -- delegate for Player combobox in Lineup dialog
LineupPositionComboBoxDelegate -- delegate for Position combobox in Lineup dialog
LineupTeamDisplayDelegate -- delegate for Team combobox in Lineup dialog
MgrConfedComboBoxDelegate -- delegate for Confederation combobox in Manager dialog
NullLineEditDelegate -- delegate for handling NULLs in LineEdit widgets
PlyrConfedComboBoxDelegate -- delegate for Confederation combobox in Player dialog
RefConfedComboBoxDelegate -- delegate for Confederation combobox in Referee dialog
SubInComboBoxDelegate -- delegate for Players (In) combobox in Substitutions dialog
SubOutComboBoxDelegate -- delegate for Players (Out) combobox in Substitutions dialog
SwitchPlayerComboBoxDelegate -- delegate for Players combobox in Switch Positions dialog
VenConfedComboBoxDelegate -- delegate for Confederation combobox in Venues dialog
WeatherComboBoxDelegate -- delegate for Weather Conditions combobox in Environments dialog

Templates:
ConfedComboBoxDelegateTemplate -- template class for Confederation comboboxes in Personnel dialogs
MgrComboBoxDelegateTemplate -- template class for Manager comboboxes in Match dialog
TeamComboBoxDelegateTemplate -- template class for Team comboboxes in Match dialog

"""

class NullLineEditDelegate(QSqlRelationalDelegate):
    """Implements custom delegate for LineEdit widgets.  
    
    Converts empty strings to NULL for use in databases.
    
    Inherits QSqlRelationalDelegate.
    
    """
    def __init__(self, parent=None):
        """Constructor to NullLineEditDelegate class."""
        super(NullLineEditDelegate, self).__init__(parent)
        
    def setEditorData(self, editor, index):
        """Writes current data from model into editor.  If data is NULL, sets currentText to an empty string.
        
        Arguments:
            editor -- LineEdit widget
            index -- current index of database table model
            
        """
        rawData = index.data(Qt.DisplayRole)
        if rawData.isNull():
            value = QString()
        else:
            value = rawData.toString()
        editor.setText(value)
        
    def setModelData(self, editor, model, index):
        """Writes current text from editor to current entry in database model. If current text is empty, writes NULL to model record.
        
        Arguments:
            editor -- LineEdit widget
            model -- underlying database table model
            index -- current index of database table model
            
        """
        textline = editor.text()
        textline.trimmed()
        model.setData(index, QVariant((QVariant.String)) if textline.length() == 0 else textline)
        
        
class EventTeamComboBoxDelegate(QSqlRelationalDelegate):
    """Implements custom delegate template for Team ComboBox in Match Event dialogs.
    
    Inherits QSqlRelationalDelegate.
    
    """
    
    def __init__(self, parent=None):
        """Constructor for EventTeamComboBoxDelegate class."""
        super(EventTeamComboBoxDelegate, self).__init__(parent)
        
        # get current matchup
        self.matchSelect = parent.matchSelect
        
    def setEditorData(self, editor, index):
        """Writes current data from model into editor. 
        
        Filters contents of combobox so that only options are the two competing teams in the match.
        
        Arguments:
            editor -- ComboBox widget
            index -- current index of database table model
            
        """
        # goals model
        eventModel = index.model()
        
        # team model, reset filter on team model
        teamModel = editor.model()
        teamModel.setFilter(QString())

        # current matchup
        matchup = self.matchSelect.currentText()
        
        # get match_id by making a query on match_list
        query = QSqlQuery()
        query.prepare("SELECT match_id FROM match_list WHERE matchup = ?")
        query.addBindValue(QVariant(matchup))
        query.exec_()
        if query.next():
            match_id = query.value(0).toString()

        # filter team combobox
        # result: home and away teams for specific match
        teamQueryString = QString("team_id IN"
            "(SELECT team_id FROM tbl_hometeams WHERE match_id = %1"
            "UNION SELECT team_id FROM tbl_awayteams WHERE match_id = %1)").arg(match_id)
        teamModel.setFilter(teamQueryString)
        
        # get team name from goals model
        teamText = eventModel.data(index, Qt.DisplayRole).toString()
            
        # set current index of team combobox
        editor.setCurrentIndex(editor.findText(teamText, Qt.MatchExactly))


class EventPlayerComboBoxDelegate(QSqlRelationalDelegate):
    """Implements custom delegate template for Player ComboBox in Match Event dialogs.
    
    Filters player combobox on match and team.
    
    Inherits QSqlRelationalDelegate.
    
    """
    
    def __init__(self, parent=None):
        """Constructor for EventPlayerComboBoxDelegate class."""
        super(EventPlayerComboBoxDelegate, self).__init__(parent)

        # get match select combobox object
        self.matchSelect = parent.matchSelect
    
    def setEditorData(self, editor, index):
        """Writes current data from model into editor. 
        
        Filters contents of combobox so that only options are the players in the 
        match lineup for the same team and match.
        
        Arguments:
            editor -- ComboBox widget
            index -- current index of database table model
            
        """
#        print "Calling setEditorData() in EventPlayerComboBoxDelegate"
        
        editor.blockSignals(True)
        
        # event model
        eventModel = index.model()
        
        # lineup list model for combobox, reset filter on lineup list
        lineupListModel = editor.model()
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
        else:
            match_id = "-1"
        
        # get player name from model
        playerName = eventModel.data(index).toString()
        
        # make query on lineup_list to find lineup_id associated with player
        lineupQuery = QSqlQuery()
        lineupQuery.prepare("SELECT lineup_id FROM lineup_list WHERE player = ?")
        lineupQuery.addBindValue(QVariant(playerName))
        lineupQuery.exec_()
        if lineupQuery.next():
            lineup_id = lineupQuery.value(0).toString()
        else:
            lineup_id = "-1"
       
        # make query on tbl_lineups to find team
        teamQuery = QSqlQuery()
        teamQuery.prepare("SELECT team_id FROM tbl_lineups WHERE lineup_id = ?")
        teamQuery.addBindValue(QVariant(lineup_id))
        teamQuery.exec_()        
        if teamQuery.next():
            team_id = teamQuery.value(0).toString()
        else:
            team_id = "-1"        
        
        # filter lineup list model by match_id
        lineupListModel.setFilter(QString("lineup_id IN "
                                                          "(SELECT lineup_id FROM tbl_lineups WHERE match_id = %1 AND team_id = %2)").arg(match_id, team_id))

        # set current index in player combobox by searching for player name
        editor.setCurrentIndex(editor.findText(playerName, Qt.MatchExactly))
        
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        """Maps selected index in editor to its model field, and writes to the current entry in the database table.
        
        Arguments:
            editor -- ComboBox widget
            model -- underlying database table model
            index -- current index of database table model
            
        """
#        print "Calling setModelData() of EventPlayerComboBoxDelegate"
        
        boxIndex = editor.currentIndex()
        value = editor.model().record(boxIndex).value("lineup_id")
                
        ok = model.setData(index, value)
        if not ok:
            print "Insertion error"


class SwitchPlayerComboBoxDelegate(QSqlRelationalDelegate):
    """Implements custom delegate template for Player ComboBox in Switch Position dialogs.
    
    Ensure that players in starting match lineup for same team who have not 
    already been substituted, and non-starting players who have been 
    substituted in, are listed in combobox.
    
    Inherits QSqlRelationalDelegate.
    
    """
    
    def __init__(self, parent=None):
        """Constructor for SwitchPlayerComboBoxDelegate class."""
        super(SwitchPlayerComboBoxDelegate, self).__init__(parent)

        # get match select combobox object
        self.matchSelect = parent.matchSelect
    
    def setEditorData(self, editor, index):
        """Writes current data from model into editor. 
        
        Filters contents of combobox so that only options are the eligible players in the 
        match lineup for the same team and match.
        
        Arguments:
            editor -- ComboBox widget
            index -- current index of database table model
            
        """
#        print "Calling setEditorData() in SwitchPlayerComboBoxDelegate"
        
        editor.blockSignals(True)
        
        # event model
        eventModel = index.model()
        
        # lineup list model for combobox, reset filter on lineup list
        lineupListModel = editor.model()
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
        else:
            match_id = "-1"
        
        # get player name from model
        playerName = eventModel.data(index).toString()
        
        # make query on lineup_list to find player name
        playerQuery = QSqlQuery()
        playerQuery.prepare("SELECT lineup_id FROM lineup_list WHERE player = ?")
        playerQuery.addBindValue(QVariant(playerName))
        playerQuery.exec_()
        if playerQuery.next():
           lineup_id = playerQuery.value(0).toString()
        else:
           lineup_id = "-1"
           
       # make query on tbl_lineups to find team associated with player
        teamQuery = QSqlQuery()
        teamQuery.prepare("SELECT team_id FROM tbl_lineups WHERE lineup_id = ?")
        teamQuery.addBindValue(QVariant(lineup_id))
        teamQuery.exec_()        
        if teamQuery.next():
            team_id = teamQuery.value(0).toString()
        else:
            team_id = "-1"        
        
        filterString = QString("lineup_id NOT IN (SELECT lineup_id FROM tbl_outsubstitutions WHERE lineup_id <> %1) "
                               "AND lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE lp_starting AND match_id = %2 AND team_id = %3) "
                               "OR (lineup_id IN (SELECT lineup_id FROM tbl_insubstitutions WHERE lineup_id <> %1) AND "
                               "lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE NOT lp_starting AND match_id = %2 AND team_id = %3))"
                               ).arg(lineup_id).arg(match_id).arg(team_id)

        # filter Player combobox
        lineupListModel.setFilter(filterString)

        # set current index in player combobox by searching for player name
        editor.setCurrentIndex(editor.findText(playerName, Qt.MatchExactly))        
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        """Maps selected index in editor to its model field, and writes to the current entry in the database table.
        
        Arguments:
            editor -- ComboBox widget
            model -- underlying database table model
            index -- current index of database table model
            
        """
#        print "Calling setModelData() of SwitchPlayerComboBoxDelegate"
        
        boxIndex = editor.currentIndex()
        value = editor.model().record(boxIndex).value("lineup_id")
                
        ok = model.setData(index, value)
        if not ok:
            print "Insertion error"


class SubOutComboBoxDelegate(QStyledItemDelegate):
    """ Implements custom delegate template for Out Substitutions combobox.
    
     Ensure that players in starting match lineup for same team who have not 
     already been substituted, and non-starting players who have been 
     substituted in, are listed in combobox.
     
     Inherits QStyledItemDelegate.

    """
    
    def __init__(self, parent=None):
        """Constructor for SubOutComboBoxDelegate class."""
#        print "Calling init() of SubOutComboBoxDelegate"
        super(SubOutComboBoxDelegate, self).__init__(parent)
        
        self.match = parent.matchSelect
        self.team = parent.teamSelect        
        
    def setEditorData(self, editor, index):
        """Writes current data from model into editor. 
        
        Filters contents of combobox so that only options are the players eligible
        to be substituted out who are in the match lineup for the same team and match.
        
        Arguments:
            editor -- ComboBox widget
            index -- current index of database table model
            
        """
#        print "Calling setEditorData() of SubOutComboBoxDelegate"       
        
        editor.blockSignals(True)
        
        # linking table
        subsLinkingModel = index.model()

        # get match_id from current text in matchSelect (main form)
        matchup = self.match.currentText()
       
        # lineup list model for combobox, reset filter on lineup list
        lineupListModel = editor.model()
        lineupListModel.setFilter(QString())

        # get match_id by making a query on match_list with matchup
        matchQuery = QSqlQuery()
        matchQuery.prepare("SELECT match_id FROM match_list WHERE matchup = ?")
        matchQuery.addBindValue(QVariant(matchup))
        matchQuery.exec_()
        if matchQuery.next():
            match_id = matchQuery.value(0).toString()
        else:
            match_id = "-1"

        # get lineup_id from linking model
        # if there exists an entry, then find player name and set filter string for
        # Player combobox
        #
        #    -- filter players who can be subbed out of match
        #    -- same match, same team, on lineup list, starting or already subbed in, not already subbed out
        #    SELECT player FROM tbl_lineups WHERE lineup_id NOT IN
        #        (SELECT lineup_id FROM tbl_outsubstitutions) AND lp_starting AND match_id = ? AND team_id = ?
        #    UNION
        #    SELECT player FROM tbl_lineups WHERE lineup_id IN
        #        (SELECT lineup_id FROM tbl_insubstitutions) AND NOT lp_starting AND match_id = ? AND team_id = ?

#        print "Index: %d" % index.row()
        if index.row() == -1:
            # no entry --> invalid index
            playerName = "-1"
            lineup_id = "-1"
            team_id = "-1"
        else:
            # entry --> valid index
            lineup_id = subsLinkingModel.record(index.row()).value("lineup_id").toString()
            
            # make query on lineup_list to find player name
            playerQuery = QSqlQuery()
            playerQuery.exec_(QString("SELECT player FROM lineup_list WHERE lineup_id = %1").arg(lineup_id))
            if playerQuery.isActive():
               playerQuery.next()
               playerName = unicode(playerQuery.value(0).toString())
            else:
               playerName = "-1"
               
           # make query on tbl_lineups to find team associated with player
            teamQuery = QSqlQuery()
            teamQuery.prepare("SELECT team_id FROM tbl_lineups WHERE lineup_id = ?")
            teamQuery.addBindValue(QVariant(lineup_id))
            teamQuery.exec_()        
            if teamQuery.next():
                team_id = teamQuery.value(0).toString()
            else:
                team_id = "-1"        
   
#        print "Current (OUT) match ID: %s" % match_id   
#        print "Current (OUT) lineup ID: %s" % lineup_id
#        print "Current (OUT) team ID: %s" % team_id
#        print "Current (OUT) player: %s" % playerName
        
        filterString = QString("lineup_id NOT IN (SELECT lineup_id FROM tbl_outsubstitutions WHERE lineup_id <> %1) "
                               "AND lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE lp_starting AND match_id = %2 AND team_id = %3) "
                               "OR (lineup_id IN (SELECT lineup_id FROM tbl_insubstitutions WHERE lineup_id <> %1) AND "
                               "lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE NOT lp_starting AND match_id = %2 AND team_id = %3))"
                               ).arg(lineup_id).arg(match_id).arg(team_id)

        # filter Player combobox
        lineupListModel.setFilter(filterString)

        # set current index to item that matches data value
        editor.setCurrentIndex(editor.findText(playerName, Qt.MatchExactly))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        """Maps selected index in editor to its model field, and writes to the current entry in the database table.
        
        Arguments:
            editor -- ComboBox widget
            model -- underlying database table model
            index -- current index of database table model
            
        """
#        print "Calling setModelData() of SubOutComboBoxDelegate"
        
        boxIndex = editor.currentIndex()
        value = editor.model().record(boxIndex).value("lineup_id")
        
        model.setData(index, value)
        

class SubInComboBoxDelegate(QStyledItemDelegate):
    """ Implements custom delegate template for In Substitutions combobox.
     Ensure that players in match lineup for same team, who are not 
     starting players and have not already been substituted, are listed 
     in combobox.
    
    Inherits QStyledItemDelegate.
    
    """
    
    def __init__(self, parent=None):
        """Constructor for SubInComboBoxDelegate class."""
#        print "Calling init() of SubInComboBoxDelegate"
        super(SubInComboBoxDelegate, self).__init__(parent)
        
        self.match = parent.matchSelect
        self.team = parent.teamSelect
        
    def setEditorData(self, editor, index):
        """Writes current data from model into editor. 
        
        Filters contents of combobox so that only options are the players eligible 
        to be substituted out who are in the match lineup for the same team and match.
        
        Arguments:
            editor -- ComboBox widget
            index -- current index of database table model
            
        """
#        print "Calling setEditorData() of SubInComboBoxDelegate"   
        
        editor.blockSignals(True)
        
        # linking table
        subsLinkingModel = index.model()

        # get match_id from current text in matchSelect (main form)
        matchup = self.match.currentText()
       
        # lineup list model for combobox, reset filter on lineup list
        lineupListModel = editor.model()
        lineupListModel.setFilter(QString())        
            
        # get match_id by making a query on match_list with matchup
        matchQuery = QSqlQuery()
        matchQuery.prepare("SELECT match_id FROM match_list WHERE matchup = ?")
        matchQuery.addBindValue(QVariant(matchup))
        matchQuery.exec_()
        if matchQuery.next():
            match_id = matchQuery.value(0).toString()
        else:
            match_id = "-1"

        # get lineup_id from linking model
        # if there exists an entry, then find player name and set filter string for
        # Player combobox
        #
        #    -- filter players who can be subbed into match
        #    -- same match, same team, not starting, not already subbed in
        #    SELECT lineup_id FROM tbl_lineups WHERE lineup_id NOT IN
        #        (SELECT lineup_id FROM tbl_insubstitutions) AND 
        #        NOT lp_starting AND match_id = ? AND team_id = ?
        
#        print "Index: %d" % index.row()
        if index.row() == -1:
            # no entry --> invalid index
            playerName = "-1"
            lineup_id = "-1"
            team_id = "-1"
        else:
            # entry --> valid index
            lineup_id = subsLinkingModel.record(index.row()).value("lineup_id").toString()            
            
            # make query on lineup_list to find player name
            query = QSqlQuery()
            query.exec_(QString("SELECT player FROM lineup_list WHERE lineup_id = %1").arg(lineup_id))
            if query.isActive():
               query.next()
               playerName = unicode(query.value(0).toString())
            else:
               playerName = "-1"
               
           # make query on tbl_lineups to find team associated with player
            teamQuery = QSqlQuery()
            teamQuery.prepare("SELECT team_id FROM tbl_lineups WHERE lineup_id = ?")
            teamQuery.addBindValue(QVariant(lineup_id))
            teamQuery.exec_()        
            if teamQuery.next():
                team_id = teamQuery.value(0).toString()
            else:
                team_id = "-1"        

#        print "Current (IN) match ID: %s" % match_id
#        print "Current (IN) lineup ID: %s" % lineup_id
#        print "Current (IN) team ID: %s" % team_id
#        print "Current (IN) player: %s" % playerName
        
        filterString = QString("lineup_id NOT IN "
                                   "(SELECT lineup_id FROM tbl_insubstitutions WHERE lineup_id <> %1) AND "
                                   "lineup_id IN (SELECT lineup_id from tbl_lineups WHERE "
                                   "NOT lp_starting AND match_id = %2 AND team_id = %3)").arg(lineup_id).arg(match_id).arg(team_id)

        # filter Player combobox
        lineupListModel.setFilter(filterString)

#        print editor.findText(playerName, Qt.MatchExactly)

        # set current index to item that matches data value
        editor.setCurrentIndex(editor.findText(playerName, Qt.MatchExactly))
        editor.blockSignals(False)
        
    def setModelData(self, editor, model, index):
        """Maps selected index in editor to its model field, and writes to the current entry in the database table.
        
        Arguments:
            editor -- ComboBox widget
            model -- underlying database table model
            index -- current index of database table model
            
        """
#        print "Calling setModelData() of SubInComboBoxDelegate"
        
        boxIndex = editor.currentIndex()
        value = editor.model().record(boxIndex).value("lineup_id")
        
        model.setData(index, value)
        

class GoalPlayerComboBoxDelegate(QSqlRelationalDelegate):
    """ Implements custom delegate template for Player ComboBox in Goal dialogs.
    
     This is handled differently from other Match Event dialogs because of 
     possibility of own goals, so cannot filter by team_id.
    
    Inherits QSqlRelationalDelegate.
    
    """    
    
    def __init__(self, parent=None):
        """Constructor for GoalPlayerComboBoxDelegate class."""
        super(GoalPlayerComboBoxDelegate, self).__init__(parent)

        # get current matchup
        self.matchSelect = parent.matchSelect
        
    def setEditorData(self, editor, index):
        """Writes current data from model into editor. 
        
        Filters contents of combobox so that only options are the players in the 
        match lineup for the same match.
        
        Arguments:
            editor -- ComboBox widget
            index -- current index of database table model
            
        """
        
        # goals model
        goalModel = index.model()
        
        # lineup list model for combobox, reset filter on lineup list
        lineupListModel = editor.model()
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
        else:
            match_id = "-1"
            
        # filter lineup list model by match_id
        lineupListModel.setFilter(QString("lineup_id IN (SELECT lineup_id FROM tbl_lineups WHERE match_id = %1)").arg(match_id))

        # get player from goals model
        playerText = goalModel.data(index, Qt.DisplayRole).toString()
        
        # set current index in player combobox by searching for player name
        editor.setCurrentIndex(editor.findText(playerText, Qt.MatchExactly))


class LineupTeamDisplayDelegate(QSqlRelationalDelegate):
    """ Implements custom delegate template for Team LineEdit display in Lineup dialog.
    
     Responsible for mapping displayed team name to team ID for insertion in Lineup table.
    
    Inherits QSqlRelationalDelegate.
    
    """   

    def __init__(self, parent=None):
        """Constructor for LineupTeamDisplayDelegate class.
        
        Argument:
        parent - parent class (default None)
        
        """
        super(LineupTeamDisplayDelegate, self).__init__(parent)
        self.teamName = parent.teamName
        
    def setEditorData(self, editor, index):
        """Writes team name into editor. 
        
        Arguments:
            editor -- ComboBox widget
            index -- current index of database table model
            
        """
        editor.setText(self.teamName)
        
    def setModelData(self, editor, model, index):
        """Maps team name to ID number in Teams model, and writes ID to the current entry in the database table.
        
        Arguments:
            editor -- ComboBox widget
            model -- underlying database table model
            index -- current index of database table model
            
        """
#        print "Calling setModelData() of LineupTeamDisplayDelegate"
        # get team name
        teamName = editor.text()
        # get team ID from tbl_teams
        query = QSqlQuery()
        query.prepare("SELECT team_id FROM tbl_teams WHERE tm_name = ?")
        query.addBindValue(QVariant(teamName))
        query.exec_()        
        if query.next():
            teamID = query.value(0).toString()
        else:
            teamID = "-1"
        
        model.setData(index, QVariant(teamID))


class LineupPlayerComboBoxDelegate(QSqlRelationalDelegate):
    """ Implements custom delegate template for Player ComboBox in Lineup dialog.
    
    Filters combobox to list of players not already selected for match.  Also set
    index of combobox to correct index.
    
    Inherits QSqlRelationalDelegate.
    
    """    

    def __init__(self, parent=None):
        """Constructor for LineupPlayerComboBoxDelegate class."""
        super(LineupPlayerComboBoxDelegate, self).__init__(parent)
        self.matchID_display = parent.matchID_display

    def setEditorData(self, editor, index):
        """Writes current data from model into editor. 
        
        Filters contents of combobox so that only options are the players not already
        selected for the match.
        
        Arguments:
            editor -- ComboBox widget
            index -- current index of database table model
            
        """
        lineupModel = index.model()
        playerModel = editor.model()
        
        # block signals from player combobox so that EnableWidget() is not called multiple times
        editor.blockSignals(True)
        
        # clear filters        
        playerModel.setFilter(QString())
        
        # get match_id and lineup_id
        match_id = self.matchID_display.text()
        lineup_id = lineupModel.record(index.row()).value("lineup_id").toString()
        
        # filter out player_id already in tbl_lineups for match_id
        # (exclusive of current lineup_id)
        if lineup_id.isEmpty():
            playerModel.setFilter(QString("player_id NOT IN "
                "(SELECT player_id FROM tbl_lineups WHERE match_id = %1)").arg(match_id))
        else:
            playerModel.setFilter(QString("player_id NOT IN "
                "(SELECT player_id FROM tbl_lineups WHERE match_id = %1 AND lineup_id <> %2)").arg(match_id, lineup_id))
            
        # get corresponding player name
        playerText =  lineupModel.data(index, Qt.DisplayRole).toString()

        # set current index 
        editor.setCurrentIndex(editor.findText(playerText, Qt.MatchExactly))
        
        # unblock signals from player combobox
        editor.blockSignals(False)


class LineupPositionComboBoxDelegate(QSqlRelationalDelegate):
    """ Implements custom delegate template for Position ComboBox in Lineup dialog.
    
     Set currentIndex of Position ComboBox to default player position.  If player undefined
     make currentIndex = -1.
    
    Inherits QSqlRelationalDelegate.   
    
    """
    
    def __init__(self, parent=None):
        """Constructor for LineupPositionComboBoxDelegate class."""
        super(LineupPositionComboBoxDelegate, self).__init__(parent)

    def setEditorData(self, editor, index):
        """Writes current data from model into editor. 
        
        Arguments:
            editor -- ComboBox widget
            index -- current index of database table model
            
        """
        lineupModel = index.model()
        
#        print "Calling setEditorData() of LineupPositionComboBoxDelegate"

        # if position not already defined in model, get default position from Player entry
        positionText = lineupModel.data(index, Qt.DisplayRole).toString()
#        print "Position in match: %s" % positionText
        
        # look for position name and set index
        editor.setCurrentIndex(editor.findText(positionText, Qt.MatchExactly))


class CheckBoxDelegate(QSqlRelationalDelegate):
    """ Implements custom delegate template for CheckBox widgets.
    
     Set CheckBox state according to Boolean value of flag in table, and write
     Boolean value to database.
    
    Inherits QSqlRelationalDelegate.
    
    """

    def __init__(self, parent=None):
        """Constructor for CheckBoxDelegate class."""
        super(CheckBoxDelegate, self).__init__(parent)

    def setEditorData(self, editor, index):
        """Writes current data from model into editor. Sets checkbox status from Boolean value.
        
        Arguments:
            editor -- ComboBox widget
            index -- current index of database table model
        
        """
        editor.setChecked(index.model().data(index, Qt.DisplayRole).toBool())

    def setModelData(self, editor, model, index):
        """Maps checkbox value in editor to its model field, and writes to the current entry in the database table.
        
        Arguments:
            editor -- ComboBox widget
            model -- underlying database table model
            index -- current index of database table model
            
        """        
        model.setData(index, QVariant(editor.isChecked()))


class CountryComboBoxDelegate(QSqlRelationalDelegate):
    """ Implements custom delegate template for Country ComboBox.  
    
    Filters combobox to list of countries from same confederation (according to
    current index of Confederation combobox).  Also set index of combobox
    to correct index.  
    
    Inherits QSqlRelationalDelegate.
    
    """

    def __init__(self, parent=None):
        """Constructor for CountryComboBoxDelegate class."""
        super(CountryComboBoxDelegate, self).__init__(parent)
        
    def setEditorData(self, editor, index):
        """Writes current data from model into editor. 
        
        Filters contents of combobox so that only options are the countries
        from the same confederation.
        
        Arguments:
            editor -- ComboBox widget
            index -- current index of database table model
            
        """
        # get parent table and current location in table
        parentModel = index.model()
        
        # obtain country table from combobox
        countryModel = editor.model()
        
        # clear filters
        countryModel.setFilter(QString())
        countryModel.select()
        
        # search for country in Country combobox, return its index in list
        countryText = parentModel.data(index, Qt.DisplayRole).toString()        
        countryIndex = editor.findText(countryText, Qt.MatchExactly)
        
        # extract corresponding Confederation ID
        # filter combobox so that countries in list are from same confederation
        id = countryModel.record(countryIndex).value("confed_id").toString()
        countryModel.setFilter(QString("confed_id = %1").arg(id))
        
        # country's index in filtered combobox has changed, so search for country
        # and assign result to current index
        editor.setCurrentIndex(editor.findText(countryText, Qt.MatchExactly))
        
    def setModelData(self, editor, model, index):
        """Maps selected index in editor to its model field, and writes to the current entry in the database table.
        
        Arguments:
            editor -- ComboBox widget
            model -- underlying database table model
            index -- current index of database table model
            
        """
        # convert combobox selection to id number
        boxIndex = editor.currentIndex()
        value = editor.model().record(boxIndex).value("country_id")
               
        # call setData()
        ok = model.setData(index, value)

class ConfedComboBoxDelegateTemplate(QStyledItemDelegate):
    """ Implements custom delegate template for Confederation ComboBox.  
    
    Sets index of combobox to correct index.  This is used as a base class for 
    Confederation comboboxes in different dialogs.
    
    Inherits QStyledItemDelegate.
    
    """

    def __init__(self, parent=None):
        """Constructor for ConfedComboBoxDelegateTemplate class."""
        super(ConfedComboBoxDelegateTemplate, self).__init__(parent)
        
    def setEditorData(self, editor, index):
        """Uses current index and ID in Country combobox to set current index in Confederation editor. 
        
        Arguments:
            editor -- ComboBox widget
            index -- current index of database table model (not used)
            
        """        
        countryIndex = self.countryBox.currentIndex()
        countryModel = self.countryBox.model()
        id = countryModel.record(countryIndex).value("confed_id").toString()
        
        # make query on tbl_confederations to extract confederation name 
        # corresponding to confederation ID
        # there will only be one confederation in query result
        query = QSqlQuery()
        query.exec_(QString("SELECT confed_name FROM tbl_confederations WHERE confed_id = %1").arg(id))
        if query.isActive():
            query.next()
            confedStr = query.value(0).toString()
        else:
            confedStr = "-1"

        # search for confederation name in combobox, set index to current index
        editor.setCurrentIndex(editor.findText(confedStr, Qt.MatchExactly))


class WeatherComboBoxDelegate(QStyledItemDelegate):
    """Implements custom delegate for Weather Conditions ComboBox.
    
    Inherits QStyledItemDelegate.
    
    """
    
    def __init__(self, parent=None):
        """Constructor for WeatherComboBoxDelegate class."""
        super(WeatherComboBoxDelegate, self).__init__(parent)
#        print "Calling init() of WeatherComboBoxDelegate"
        
    def setEditorData(self, editor, index):
        """Writes current data from model into editor, or sets index to -1 if no record in model.
        
        Arguments:
            editor -- ComboBox widget
            index -- current index of database table model
            
        """
#        print "Calling setEditorData() of WeatherComboBoxDelegate"
        parentModel = index.model()
        
#        print "Index: %d" % index.row()
        if index.row() == -1:
            currentIndex = -1
        else:
            # if current index in model is nonzero, find weather_id from linking table
            weather_id = parentModel.record(index.row()).value("weather_id") .toString()
            # make query on tbl_weather to find team name
            query = QSqlQuery()
            query.exec_(QString("SELECT wx_conditiondesc FROM tbl_weather WHERE weather_id = %1").arg(weather_id))
            if query.next():
                wxCondition = unicode(query.value(0).toString())
            else:
               wxCondition = "-1"
            currentIndex = editor.findText(wxCondition, Qt.MatchExactly)
                        
        # set current index to item that matches data value
#        print "current Index = %d" % currentIndex
        editor.setCurrentIndex(currentIndex)
        
    def setModelData(self, editor, model, index):
        """Maps selected index in editor to its model field, and writes to the current entry in the database table.
        
        Arguments:
            editor -- ComboBox widget
            model -- underlying database table model
            index -- current index of database table model
            
        """
#        print "Calling setModelData() of WeatherComboBoxDelegate"
        
        # convert combobox selection to id number
        boxIndex = editor.currentIndex()
        value = editor.model().record(boxIndex).value("weather_id")
        
        # call setData()
        model.setData(index, value)


class TeamComboBoxDelegateTemplate(QStyledItemDelegate):
    """Implements custom delegate template for Home/Away Team ComboBoxes.  
    
    Sets index of combobox to correct index and filters combobox items.  This is used as a 
    base class for Team comboboxes in the Match Entrydialog.
    
    Inherits QStyledItemDelegate.
    
    """

    def __init__(self, parent=None):
        """Constructor for TeamComboBoxDelegateTemplate class."""
        super(TeamComboBoxDelegateTemplate, self).__init__(parent)
#        print "Calling init() of TeamComboBoxDelegateTemplate"
        
    def setEditorData(self, editor, index):
        """ Sets combobox index to correspond with current row in database model.
        
        Filters entry list in combobox to prevent possibility of selecting same team
        in home and away comboboxes.
        
        Arguments:
            editor -- ComboBox widget
            index -- current index of database table model
        
        """
#        print "Calling setEditorData() of TeamComboBoxDelegateTemplate"
        linkingModel = index.model()        
        teamModel = editor.model()
        
        editor.blockSignals(True)
        
        # flush filter on editor model
        teamModel.setFilter(QString())
        
#        print "Index: %d" % index.row()
        if index.row() == -1:
            teamName = "-1"
        else:
            # if current index in model is nonzero, find team_id from linking table
            team_id = linkingModel.record(index.row()).value("team_id") .toString()
            # make query on tbl_teams to find team name
            query = QSqlQuery()
            query.exec_(QString("SELECT tm_name FROM tbl_teams WHERE team_id = %1").arg(team_id))
            if query.next():
                teamName = unicode(query.value(0).toString())
            else:
               teamName = "-1"
            
        # if opposingBox enabled, get id that corresponds to current item selected
        # otherwise, set id to -1
        opposingModel_id = self.opposingModel.record(index.row()).value("team_id").toString()            
        
        # filter main Box so that opposingBox selection not included in main Box
        teamModel.setFilter(QString("team_id NOT IN (%1)").arg(opposingModel_id))
    
        # set current index to item that matches team name
        editor.setCurrentIndex(editor.findText(teamName, Qt.MatchExactly))
        
        editor.blockSignals(False)
        
    def setModelData(self, editor, model, index):
        """Maps selected index in editor to its model field, and writes to the current entry in the database table.
        
        Arguments:
            editor -- ComboBox widget
            model -- underlying database table model
            index -- current index of database table model
            
        """        
        # convert combobox selection to id number
        boxIndex = editor.currentIndex()
        value = editor.model().record(boxIndex).value("team_id")
        
        # call setData()
        model.setData(index, value)


class MgrComboBoxDelegateTemplate(QStyledItemDelegate):
    """ Implements custom delegate template for Home/Away Manager ComboBoxes.  
    
    Sets index of combobox to correct index and filters combobox items.  This is used as a 
    base class for Manager comboboxes in the Match Entrydialog.
    
    Inherits QStyledItemDelegate.
    
    """
    
    def __init__(self, parent=None):
        """Constructor for MgrComboBoxDelegateTemplate class."""
        super(MgrComboBoxDelegateTemplate, self).__init__(parent)
#        print "Calling init() of MgrComboBoxDelegateTemplate"        
        
    def setEditorData(self, editor, index):
        """Writes current data from model into editor. 
        
         Filters entry list in combobox to prevent possibility of selecting same manager
         in home and away comboboxes.
        
        Arguments:
            editor -- ComboBox widget
            index -- current index of database table model
            
        """
#        print "Calling setEditorData() of MgrComboBoxDelegateTemplate"       
        linkingModel = index.model()
        teamModel = editor.model()
        
        editor.blockSignals(True)
        
        # flush filter on editor model
        teamModel.setFilter(QString())

#        print "Index: %d" % index.row()
        if index.row() == -1:
            managerName = "-1"
        else:
            # if current index in model is valid, find manager_id from linking table
            manager_id = linkingModel.record(index.row()).value("manager_id") .toString()
            # make query on tbl_teams to find team name
            query = QSqlQuery()
            query.exec_(QString("SELECT full_name FROM managers_list WHERE manager_id = %1").arg(manager_id))
            if query.isActive():
               query.next()
               managerName = unicode(query.value(0).toString())
            else:
               managerName = "-1"

        # if opposingBox enabled, get id that corresponds to current item selected
        # otherwise, set id to -1
        opposingModel_id = self.opposingModel.record(index.row()).value("manager_id").toString()            
        
        # filter main Box so that opposingBox selection not included in main Box
        teamModel.setFilter(QString("manager_id NOT IN (%1)").arg(opposingModel_id))
            
        # find index in tbl_teams that corresponds to team_id
        editor.setCurrentIndex(editor.findText(managerName, Qt.MatchExactly))
        
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        """Maps selected index in editor to its model field, and writes to the current entry in the database table.
        
        Arguments:
            editor -- ComboBox widget
            model -- underlying database table model
            index -- current index of database table model
            
        """
        boxIndex = editor.currentIndex()
        value = editor.model().record(boxIndex).value("manager_id")
        
        model.setData(index, value)


class HomeTeamComboBoxDelegate(TeamComboBoxDelegateTemplate):
    """ Implements custom delegate for Home Team ComboBox in Match dialog.  
    
    Sets opposingModel member to model corresponding to away team combobox.
    
    Inherits TeamComboBoxDelegateTemplate.
    
    """    

    def __init__(self, parent=None):
        """Constructor for HomeTeamComboBoxDelegate class."""
        super(HomeTeamComboBoxDelegate, self).__init__(parent)
#        print "Calling init() in HomeTeamComboBoxDelegate"
        
        self.opposingModel = parent.awayteamModel


class AwayTeamComboBoxDelegate(TeamComboBoxDelegateTemplate):
    """ Implements custom delegate for Away Team ComboBox in Match dialog.  
    
    Sets opposingModel member to model corresponding to home team combobox.
    
    Inherits TeamComboBoxDelegateTemplate.
    
    """    
    
    def __init__(self, parent=None):
        """Constructor for AwayTeamComboBoxDelegate class."""
        super(AwayTeamComboBoxDelegate, self).__init__(parent)
#        print "Calling init() in AwayTeamComboBoxDelegate"

        self.opposingModel = parent.hometeamModel


class HomeMgrComboBoxDelegate(MgrComboBoxDelegateTemplate):
    """ Implements custom delegate for Home Manager ComboBox in Match dialog.  
    
    Sets opposingModel member to model corresponding to away manager combobox.
    
    Inherits MgrComboBoxDelegateTemplate.
    
    """    
    
    def __init__(self, parent=None):
        """Constructor for HomeMgrComboBoxDelegate class."""
        super(HomeMgrComboBoxDelegate, self).__init__(parent)
#        print "Calling init() in HomeMgrComboBoxDelegate"

        self.opposingModel = parent.awaymgrModel


class AwayMgrComboBoxDelegate(MgrComboBoxDelegateTemplate):
    """ Implements custom delegate for Away Manager ComboBox in Match dialog.  
    
    Sets opposingModel member to model corresponding to home manager combobox.
    
    Inherits MgrComboBoxDelegateTemplate.
    
    """    
    
    def __init__(self, parent=None):
        """Constructor for AwayMgrComboBoxDelegate class."""
        super(AwayMgrComboBoxDelegate, self).__init__(parent)
#        print "Calling init() in AwayMgrComboBoxDelegate"

        self.opposingModel = parent.homemgrModel


class MgrConfedComboBoxDelegate(ConfedComboBoxDelegateTemplate):
    """Implements custom delegate for Confederation ComboBox in Manager dialog.  
    
    Sets countryBox member to Country combobox in Manager dialog, 
    which is used to set index of Confederation combobox.
    
    Inherits ConfedComboBoxDelegateTemplate.
    
    """

    def __init__(self, parent=None):
        """Constructor for MgrConfedComboBoxDelegate class."""
        super(MgrConfedComboBoxDelegate, self).__init__(parent)
        
        self.countryBox = parent.mgrCountrySelect


class PlyrConfedComboBoxDelegate(ConfedComboBoxDelegateTemplate):
    """Implements custom delegate for Confederation ComboBox in Player dialog.  
    
    Sets countryBox member to Country combobox in Player dialog, 
    which is used to set index of Confederation combobox.
    
    Inherits ConfedComboBoxDelegateTemplate.
    
    """

    def __init__(self, parent=None):
        """Constructor for PlyrConfedComboBoxDelegate class."""
        super(PlyrConfedComboBoxDelegate, self).__init__(parent)
        
        self.countryBox = parent.plyrCountrySelect


class RefConfedComboBoxDelegate(ConfedComboBoxDelegateTemplate):
    """Implements custom delegate for Confederation ComboBox in Referee dialog.  
    
    Sets countryBox member to Country combobox in Referee dialog, 
    which is used to set index of Confederation combobox.
    
    Inherits ConfedComboBoxDelegateTemplate.
    
    """

    def __init__(self, parent=None):
        """Constructor for RefConfedComboBoxDelegate class."""
        super(RefConfedComboBoxDelegate, self).__init__(parent)
        
        self.countryBox = parent.refCountrySelect


class VenConfedComboBoxDelegate(ConfedComboBoxDelegateTemplate):
    """Implements custom delegate for Confederation ComboBox in Venues dialog.  
    
    Sets countryBox member to Country combobox in Venues dialog, 
    which is used to set index of Confederation combobox.
    
    Inherits ConfedComboBoxDelegateTemplate.
    
    """

    def __init__(self, parent=None):
        """Constructor for VenConfedComboBoxDelegate class."""
        super(VenConfedComboBoxDelegate, self).__init__(parent)
        
        self.countryBox = parent.venueCountrySelect


class GenericDelegate(QSqlRelationalDelegate):
    """Implements generic components of UI delegates.
    
    This class is designed to accommodate a list of custom column delegates. 
    Can implement either baseclass paint(), createEditor(), setEditorData() and
    setModelData() methods or custom methods if defined by the subclass.
    
    Source: "Rapid GUI Programming with Python and Qt" by Mark Summerfield, 
    Prentice-Hall, 2008, pg. 483-486.
    
    Inherits QSqlRelationalDelegate.
    
    """    

    def __init__(self, parent=None):
        """Constructor for GenericDelegate class.
        
        Defines delegates member as empty dictionary.  Keys will be column numbers.
        
        """
        super(GenericDelegate, self).__init__(parent)
        self.delegates = {}
        
    def insertColumnDelegate(self, column, delegate):
        """Inserts delegate and column number in delegate dictionary."""
        delegate.setParent(self)
        self.delegates[column] = delegate
        
    def removeColumnDelegate(self, column):
        """Removes delegate from delegate dictionary."""
        if column in self.delegates:
            del self.delegates[column]
            
    def paint(self, painter, option, index):
        """Calls either custom or baseclass paint methods for widget.
        
        Custom method is called if delegate is defined for the column.
        Base class method is called otherwise.
        
        """
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.paint(painter, option, index)
        else:
            QSqlRelationalDelegate.paint(self, painter, option, index)
            
    def createEditor(self, parent, option, index):
        """Calls either custom or baseclass editor creation methods for widget.
        
        Custom method is called if delegate is defined for the column.
        Base class method is called otherwise.
        
        """
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            return delegate.createEditor(parent, option, index)
        else:
            return QSqlRelationalDelegate.createEditor(self, parent, option, index)
            
    def setEditorData(self, editor, index):
        """Calls either custom or standard models to write data from database model to editor.
        
        Custom method is called if delegate is defined for the column.
        Base class method is called otherwise.
        
        """
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setEditorData(editor, index)
        else:
            QSqlRelationalDelegate.setEditorData(self, editor, index)
            
    def setModelData(self, editor, model, index):
        """Calls either custom or standard methods to write data from editor to database model.
        
        Custom method is called if delegate is defined for the column.
        Base class method is called otherwise.
        
        """
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setModelData(editor, model, index)
        else:
            QSqlRelationalDelegate.setModelData(self, editor, model, index)