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

"""Contains generic classes that implement specialized models for use in FMRD tools.

Classes:
SqlRelationalProxyModel - proxy model for SQL relational table models
LinkingSqlModel -- base editable linking table model

GroupLinkingModel -- implement GroupMatches table
KnockoutLinkingModel -- implement KnockoutMatches table
LeagueLinkingModel -- implement LeagueMatches table
ManagerLinkingModel -- implement HomeManagers and AwayManagers tables
ShootoutLinkingModel -- implement ShootoutOpeners table
SubstituteLinkingModel -- implement InSubstitutions and OutSubstitutions tables
TeamLinkingModel -- implement HomeTeams and AwayTeams tables
WeatherLinkingModel -- implement KickoffWeather, HalftimeWeather, and FulltimeWeather tables

"""

class SqlRelationalProxyModel(QSortFilterProxyModel):
    """Proxy model for SQL relational table models (QSqlRelationalTableModel).
    
    Assumes that source model is a QSqlRelationalTableModel object and calls
    its relational methods.
    
    Inherits QSortFilterProxyModel.
    """
    
    def __init__(self, parent=None):
        """Constructor for SqlRelationalProxyModel class."""
        super(SqlRelationalProxyModel, self).__init__(parent)
    
    def setRelation(self, column, relation):
        """Sets the relation between the column and the foreign table.
        
        Calls setRelation() method in source model.
        """
        self.sourceModel().setRelation(column, relation)
        
    def relationModel(self, column):
        """Returns the model object related to the column.
        
        Calls relationModel() method in source model.
        """
        return self.sourceModel().relationModel(column)
        
    def relation(self, column):
        """Returns the QSqlRelation object related to the column.
        
        Calls relation() method in source model.
        """
        return self.sourceModel().relation(column)
        

class LinkingSqlModel(QSqlQueryModel):
    """Base editable linking table model."""
    
    def __init__(self, parent=None):
        """Constructor for LinkingSqlModel class."""
        super(LinkingSqlModel, self).__init__(parent)
        
    def flags(self, index):
        """Defines item flags for index.  Make all columns besides first in database table editable. """
        flags = QSqlQueryModel.flags(index)
        if index.column() != 0:
            flags |= Qt.ItemIsEditable
        
        return flags
    
    def setID(self, value):
        """Sets match_id member of class."""
        self.primary_id = value
    
    def setData(self, index, value):
        """Sets role data at index with value.  Calls setCompositeKey()."""
        ok = False
        ok = self.setCompositeKey(index,  self.primary_id, value.toString())
        self.refresh()
        return ok
        
    def delete(self, primary_id):
        """Deletes row with primary_id from the linking model.
        
        This function always returns False; must be implemented by subclass.
        Arguments:
            primary_id - key ID in linking table
        """
        return False
       
    def setCompositeKey(self, index, primary_id, secondary_id):
        """Inserts or updates entry in database.
        This method returns false in class definition, must be implemented by subclass.
        
        """
        return False


class GroupLinkingModel(LinkingSqlModel):
    """Implements linking model for matches played in the group phase of a football competition.
    
    Argument:
    tbl_name - SQL table name
        
    """
    
    def __init__(self, tbl_name, parent=None):
        """Constructor for GroupLinkingModel class."""
        super(GroupLinkingModel, self).__init__(parent)
        
        self.table = tbl_name
        self.primary_id = parent.matchID_display.text()
        self.grpround_id = QString()
        self.group_id = QString()
        self.round_id = QString()
        self.calls = 0
        self.setQuery(QString("SELECT match_id, grpround_id, group_id, round_id FROM %1 WHERE match_id = %2"
                              ).arg(self.table).arg(self.primary_id))
        
    def refresh(self):
        """Refreshes query model."""
        self.setQuery(QString("SELECT match_id, grpround_id, group_id, round_id FROM %1 WHERE match_id = %2"
                              ).arg(self.table).arg(self.primary_id))
    
    def resetID(self):
        """Resets member variables in class."""
        self.grpround_id = QString()
        self.group_id = QString()
        self.round_id = QString()
        self.calls = 0
        
    def setData(self, index, value):
        """Sets role data at index with value.  Calls setXXX().
        
        This function must be called in order of the fields defined
        in the database table.        
        """
        if self.calls == 0:
            self.grpround_id = value
            self.calls += 1
        elif self.calls == 1:
            self.group_id = value
            self.calls += 1
        elif self.calls == 2:
            self.round_id = value
            self.calls += 1
        return True

    def submit(self):
        """Inserts new row into database if no prior record exists.  
        
        Updates row if record already exists..
        """
        insertString = QString("INSERT INTO %1 (match_id, grpround_id, group_id, round_id) VALUES (?,?,?,?)").arg(self.table)
        
        # test for already existing record in table
        query = QSqlQuery()
        query.prepare(QString("SELECT COUNT(*) FROM %1 WHERE match_id = ?").arg(self.table))
        query.addBindValue(self.primary_id)
        query.exec_()
        if query.next():
            if query.value(0).toInt()[0]:
                # update current record
                updateQuery = QSqlQuery()
                varList = (self.grpround_id, self.group_id, self.round_id)
                fieldList = ("grpround_id", "group_id", "round_id")
                for field,  var in zip(fieldList, varList):
                    updateString = QString("UPDATE %1 SET %2 = ? WHERE match_id = ?").arg(self.table, field)
                    updateQuery.prepare(updateString)
                    updateQuery.addBindValue(var)
                    updateQuery.addBindValue(self.primary_id)
                    updateQuery.exec_()
                self.resetID()
                return
                
        # no prior record...insert new row
        insertQuery = QSqlQuery()
        insertQuery.prepare(insertString)
        insertQuery.addBindValue(self.primary_id)
        insertQuery.addBindValue(self.grpround_id)
        insertQuery.addBindValue(self.group_id)
        insertQuery.addBindValue(self.round_id)
        ok = insertQuery.exec_()
        
        self.resetID()

        
    def delete(self, match_id):    
        """Deletes entry in database.
        
        Argument:
            match_id - primary key ID that links to Matches table
            
        """
        deleteString = QString("DELETE FROM %1 WHERE match_id = ?").arg(self.table)
        
        deleteQuery = QSqlQuery()
        deleteQuery.prepare(deleteString)
        deleteQuery.addBindValue(match_id)
        return deleteQuery.exec_()


class KnockoutLinkingModel(LinkingSqlModel):
    """Implements linking model for matches played in the knockout phase of a football competition.
    
    Argument:
    tbl_name - SQL table name
        
    """
    
    def __init__(self, tbl_name, parent=None):
        """Constructor for LeagueLinkingModel class."""
        super(KnockoutLinkingModel, self).__init__(parent)
        
        self.table = tbl_name
        self.primary_id = parent.matchID_display.text()
        self.koround_id = QString()
        self.matchday_id = QString()
        self.calls = 0
        self.setQuery(QString("SELECT match_id, koround_id, matchday_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
        
    def refresh(self):
        """Refreshes query model."""
        self.setQuery(QString("SELECT match_id, koround_id, matchday_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
    
    def resetID(self):
        """Resets member variables in class."""
        self.koround_id = QString()
        self.matchday_id = QString()
        self.calls = 0
        
    def setData(self, index, value):
        """Sets role data at index with value.
        
        This function must be called in order of the fields defined
        in the database table.
        """
        if self.calls == 0:
            self.koround_id = value.toString()
            self.calls += 1
        elif self.calls == 1:
            self.matchday_id = value.toString()
            self.calls += 1
        return True

    def submit(self):
        """Inserts new row into database if no prior record exists.  
        
        Updates row if record already exists.
        """
        insertString = QString("INSERT INTO %1 (match_id, koround_id, matchday_id) VALUES (?,?,?)").arg(self.table)
        
        # test for already existing record in table
        query = QSqlQuery()
        query.prepare(QString("SELECT COUNT(*) FROM %1 WHERE match_id = ?").arg(self.table))
        query.addBindValue(self.primary_id)
        query.exec_()
        if query.next():
            if query.value(0).toInt()[0]:
                updateQuery = QSqlQuery()
                varList = (self.koround_id, self.matchday_id)
                fieldList = ("koround_id", "matchday_id")
                for field,  var in zip(fieldList, varList):
                    updateString = QString("UPDATE %1 SET %2 = ? WHERE match_id = ?").arg(self.table, field)
                    updateQuery.prepare(updateString)
                    updateQuery.addBindValue(var)
                    updateQuery.addBindValue(self.primary_id)
                    updateQuery.exec_()
                self.resetID()
                return
                
        insertQuery = QSqlQuery()
        insertQuery.prepare(insertString)
        insertQuery.addBindValue(self.primary_id)
        insertQuery.addBindValue(self.koround_id)
        insertQuery.addBindValue(self.matchday_id)
        insertQuery.exec_()
        self.resetID()

        
    def delete(self, match_id):    
        """Deletes entry in database.
        
        Argument:
            match_id - primary key ID that links to Matches table
            
        """
        deleteString = QString("DELETE FROM %1 WHERE match_id = ?").arg(self.table)
        
        deleteQuery = QSqlQuery()
        deleteQuery.prepare(deleteString)
        deleteQuery.addBindValue(match_id)
        return deleteQuery.exec_()
    
    
class LeagueLinkingModel(LinkingSqlModel):
    """Implements linking model for matches played in the league phase of a football competition.
    
    Argument:
    tbl_name - SQL table name
        
    """

    def __init__(self, tbl_name, parent=None):
        """Constructor for LeagueLinkingModel class."""
        super(LeagueLinkingModel, self).__init__(parent)
        
        self.table = tbl_name
        self.primary_id = parent.matchID_display.text()
        self.setQuery(QString("SELECT match_id, round_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
        
    def refresh(self):
        """Refreshes query model."""
        self.setQuery(QString("SELECT match_id, round_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
        
    def setCompositeKey(self, index, match_id, round_id):
        """Inserts or updates entry in database."""
        # setup SQL statements
        insertString = QString("INSERT INTO %1 (match_id, round_id) VALUES (?,?)").arg(self.table)
        updateString = QString("UPDATE %1 SET round_id = ? WHERE match_id = ?").arg(self.table)
        
        if index.row() == -1:
            # insert into table if no existing match_id record in linking table
            insertQuery = QSqlQuery()
            insertQuery.prepare(insertString)
            insertQuery.addBindValue(match_id)
            insertQuery.addBindValue(round_id)
            return insertQuery.exec_()
        elif index.row() == 0:
            # update into table if there exists match_id record in linking table
            updateQuery = QSqlQuery()
            updateQuery.prepare(updateString)
            updateQuery.addBindValue(round_id)
            updateQuery.addBindValue(match_id)
            return updateQuery.exec_()
        else:
            # any other failure, return False
            return False
        
    def delete(self, match_id):    
        """Deletes entry in database.
        
        Argument:
            match_id - primary key ID that links to Matches table
            
        """
        deleteString = QString("DELETE FROM %1 WHERE match_id = ?").arg(self.table)
        
        deleteQuery = QSqlQuery()
        deleteQuery.prepare(deleteString)
        deleteQuery.addBindValue(match_id)
        return deleteQuery.exec_()


class WeatherLinkingModel(LinkingSqlModel):
    """Implements linking models for weather conditions at different intervals of the match.
    
    Argument:
    tbl_name - SQL table name
    
    """
    
    def __init__(self, tbl_name, parent=None):
        """Constructor for WeatherLinkingModel class."""
        super(WeatherLinkingModel, self).__init__(parent)
        
        self.table = tbl_name
        self.primary_id = parent.enviroID_display.text()
        self.setQuery(QString("SELECT enviro_id, weather_id FROM %1 WHERE enviro_id = %2").arg(self.table).arg(self.primary_id))
        
    def refresh(self):
        """Refreshes query model."""
        self.setQuery(QString("SELECT enviro_id, weather_id FROM %1 WHERE enviro_id = %2").arg(self.table).arg(self.primary_id))
        
    def setCompositeKey(self, index, enviro_id, weather_id):
        """Inserts or updates entry in database."""
        # setup SQL statements
        insertString = QString("INSERT INTO %1 (enviro_id, weather_id) VALUES (?,?)").arg(self.table)
        updateString = QString("UPDATE %1 SET weather_id = ? WHERE enviro_id = ?").arg(self.table)
        
        if index.row() == -1:
            # insert into table if no existing match_id record in linking table
            insertQuery = QSqlQuery()
            insertQuery.prepare(insertString)
            insertQuery.addBindValue(enviro_id)
            insertQuery.addBindValue(weather_id)
            return insertQuery.exec_()
        elif index.row() == 0:
            # update into table if there exists match_id record in linking table
            updateQuery = QSqlQuery()
            updateQuery.prepare(updateString)
            updateQuery.addBindValue(weather_id)
            updateQuery.addBindValue(enviro_id)
            return updateQuery.exec_()
        else:
            # any other failure, return False
            print "Error with entry Query"
            return False
        
    def delete(self, enviro_id):    
        """Deletes entry in database.
        
        Argument:
            enviro_id - primary key ID that links to Environments table
            
        """
        deleteString = QString("DELETE FROM %1 WHERE enviro_id = ?").arg(self.table)
        
        deleteQuery = QSqlQuery()
        deleteQuery.prepare(deleteString)
        deleteQuery.addBindValue(enviro_id)
        return deleteQuery.exec_()
        
class TeamLinkingModel(LinkingSqlModel):
    """Implements linking models for home and away teams in a match.
    
    Argument:
    tbl_name - SQL table name
    
    """
    
    def __init__(self, tbl_name, parent=None):
        """Constructor for TeamLinkingModel class."""
        super(TeamLinkingModel, self).__init__(parent)
        
        self.table = tbl_name
        self.primary_id = parent.matchID_display.text()
        self.setQuery(QString("SELECT match_id, team_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
        
    def refresh(self):
        """Refreshes query model."""
        self.setQuery(QString("SELECT match_id, team_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
     
    def setCompositeKey(self, index,  match_id, team_id):
        """Inserts or updates entry in database."""
        # setup SQL statements
        insertString = QString("INSERT INTO %1 (match_id,team_id) VALUES (?,?)").arg(self.table)
        updateString = QString("UPDATE %1 SET team_id = ? WHERE match_id = ?").arg(self.table)
        
        if index.row() == -1:
            # insert into table if no existing match_id record in linking table
            insertQuery = QSqlQuery()
            insertQuery.prepare(insertString)
            insertQuery.addBindValue(match_id)
            insertQuery.addBindValue(team_id)
            return insertQuery.exec_()
        elif index.row() == 0:
            # update into table if there exists match_id record in linking table
            updateQuery = QSqlQuery()
            updateQuery.prepare(updateString)
            updateQuery.addBindValue(team_id)
            updateQuery.addBindValue(match_id)
            return updateQuery.exec_()
        else:
            # any other failure, return False
            return False    

    def delete(self, match_id):    
        """Deletes entry in database.
        
        Argument:
            match_id - primary key ID that links to Matches table
            
        """
        deleteString = QString("DELETE FROM %1 WHERE match_id = ?").arg(self.table)
        
        deleteQuery = QSqlQuery()
        deleteQuery.prepare(deleteString)
        deleteQuery.addBindValue(match_id)
        return deleteQuery.exec_()


class SubstituteLinkingModel(LinkingSqlModel):
    """Implements linking models for players substituted in and out of a match.
    
    Argument:
    tbl_name - SQL table name
    
    """
    
    def __init__(self, tbl_name, parent=None):
        """Constructor for SubstituteLinkingModel class."""
        super(SubstituteLinkingModel, self).__init__(parent)
        
        self.table = tbl_name
        self.primary_id = parent.subsID_display.text()
        self.setQuery(QString("SELECT subs_id, lineup_id FROM %1 WHERE subs_id = %2").arg(self.table).arg(self.primary_id))
     
    def refresh(self):
        """Refreshes query model."""
        self.setQuery(QString("SELECT subs_id, lineup_id FROM %1 WHERE subs_id = %2").arg(self.table).arg(self.primary_id))
     
    def setCompositeKey(self, index, subs_id, lineup_id):
        """Inserts or updates entry in database.
        
        Arguments:
        index - current index in model
        subs_id - primary key ID to Substitutions table
        lineup_id - secondary key ID in linking table
        
        """
        # set up SQL statements
        insertString = QString("INSERT INTO %1 (subs_id,lineup_id) VALUES (?,?)").arg(self.table)
        updateString = QString("UPDATE %1 SET lineup_id = ? WHERE subs_id = ?").arg(self.table)
        
        if index.row() == -1:
            # insert into table if no existing subs_id record in linking table
            insertQuery = QSqlQuery()
            insertQuery.prepare(insertString)
            insertQuery.addBindValue(subs_id)
            insertQuery.addBindValue(lineup_id)
            return insertQuery.exec_()
        elif index.row() == 0:
            # update into table if there exists subs_id record in linking table
            updateQuery = QSqlQuery()
            updateQuery.prepare(updateString)
            updateQuery.addBindValue(subs_id)
            updateQuery.addBindValue(lineup_id)
            return updateQuery.exec_()
        else:
            # any other failure, return False
            return False    
            
    def delete(self, subs_id):    
        """Deletes entry in database.
        
        Argument:
            subs_id - primary key ID that links to Substitutions table
            
        """
        deleteString = QString("DELETE FROM %1 WHERE subs_id = ?").arg(self.table)
        
        deleteQuery = QSqlQuery()
        deleteQuery.prepare(deleteString)
        deleteQuery.addBindValue(subs_id)
        return deleteQuery.exec_()


class ManagerLinkingModel(LinkingSqlModel):
    """Implements linking models for managers of home and away teams in a match.
    
    Argument:
    tbl_name - SQL table name
    
    """
    def __init__(self, tbl_name, parent=None):
        """Constructor for ManagerLinkingModel class."""
        super(ManagerLinkingModel, self).__init__(parent)

        self.table = tbl_name
        self.primary_id = parent.matchID_display.text()
        self.setQuery(QString("SELECT match_id, manager_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))

    def refresh(self):
        """Refreshes query model."""
        self.setQuery(QString("SELECT match_id, manager_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
     
    def setCompositeKey(self, index, match_id, manager_id):
        """Inserts or updates entry in database.
        
        Arguments:
        index - current index in model
        match_id - primary key ID to Matches table
        manager_id - secondary key ID in linking table
        
        """
        # set up SQL statements
        insertString = QString("INSERT INTO %1 (match_id,manager_id) VALUES (?,?)").arg(self.table)
        updateString = QString("UPDATE %1 SET manager_id = ? WHERE match_id = ?").arg(self.table)
        
        if index.row() == -1:
            # insert into table if no existing match_id record in linking table
            insertQuery = QSqlQuery()
            insertQuery.prepare(insertString)
            insertQuery.addBindValue(match_id)
            insertQuery.addBindValue(manager_id)
            return insertQuery.exec_()
        elif index.row() == 0:
            # update into table if there exists match_id record in linking table
            updateQuery = QSqlQuery()
            updateQuery.prepare(updateString)
            updateQuery.addBindValue(manager_id)
            updateQuery.addBindValue(match_id)
            return updateQuery.exec_()
        else:
            # any other failure, return False
            return False    

    def delete(self, match_id):    
        """Deletes entry in database.
        
        Argument:
            match_id - primary key ID that links to Matches table
            
        """
        deleteString = QString("DELETE FROM %1 WHERE match_id = ?").arg(self.table)
        
        deleteQuery = QSqlQuery()
        deleteQuery.prepare(deleteString)
        deleteQuery.addBindValue(match_id)
        return deleteQuery.exec_()

class ShootoutLinkingModel(LinkingSqlModel):
    """Implements linking model for teams shooting first in the penalty shootout at the end of a football match.
    
    Argument:
    tbl_name - SQL table name
        
    """

    def __init__(self, tbl_name, parent=None):
        """Constructor for ShootoutLinkingModel class."""
        super(ShootoutLinkingModel, self).__init__(parent)
        
        matchSelect = parent.matchSelect
        matchModel = matchSelect.model()
        
        self.table = tbl_name
        self.primary_id = matchModel.record(matchSelect.currentIndex()).value("match_id").toString()
        self.setQuery(QString("SELECT match_id, team_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
        
    def refresh(self):
        """Refreshes query model."""
        self.setQuery(QString("SELECT match_id, team_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
        
    def setCompositeKey(self, index, match_id, team_id):
        """Inserts or updates entry in database."""
        # setup SQL statements
        insertString = QString("INSERT INTO %1 (match_id, team_id) VALUES (?,?)").arg(self.table)
        updateString = QString("UPDATE %1 SET team_id = ? WHERE match_id = ?").arg(self.table)
        
        if index.row() == -1:
            # insert into table if no existing match_id record in linking table
            insertQuery = QSqlQuery()
            insertQuery.prepare(insertString)
            insertQuery.addBindValue(match_id)
            insertQuery.addBindValue(team_id)
            return insertQuery.exec_()
        elif index.row() == 0:
            # update into table if there exists match_id record in linking table
            updateQuery = QSqlQuery()
            updateQuery.prepare(updateString)
            updateQuery.addBindValue(team_id)
            updateQuery.addBindValue(match_id)
            return updateQuery.exec_()
        else:
            # any other failure, return False
            return False
        
    def delete(self, match_id):    
        """Deletes entry in database.
        
        Argument:
            match_id - primary key ID that links to Matches table
            
        """
        deleteString = QString("DELETE FROM %1 WHERE match_id = ?").arg(self.table)
        
        deleteQuery = QSqlQuery()
        deleteQuery.prepare(deleteString)
        deleteQuery.addBindValue(match_id)
        return deleteQuery.exec_()
