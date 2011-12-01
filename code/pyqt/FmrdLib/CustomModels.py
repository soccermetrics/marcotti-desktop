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
#        print "Calling init() in LinkingSqlModel"
        
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
#        print "Calling setData() in LinkingSqlModel"
#        print "%d  %d" % (index.row(),  index.column())
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
#        print "Calling base setCompositeKey()"
        return False


class GroupLinkingModel(LinkingSqlModel):
    """Implements linking model for matches played in the group phase of a football competition.
    
    Argument:
    tbl_name - SQL table name
        
    """
    
    def __init__(self, tbl_name, parent=None):
        """Constructor for GroupLinkingModel class."""
        super(GroupLinkingModel, self).__init__(parent)
#        print "Calling init() in GroupLinkingModel"
        
        self.table = tbl_name
        self.primary_id = parent.matchID_display.text()
        self.grpround_id = "0"
        self.group_id = "0"
        self.round_id = "0"
        self.setQuery(QString("SELECT match_id, grpround_id, group_id, round_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
        
    def refresh(self):
        """Refreshes query model."""
        self.setQuery(QString("SELECT match_id, grpround_id, group_id, round_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
    
    def resetID(self):
        """Resets member variables in class."""
        self.grpround_id = "0"
        self.group_id = "0"
        self.round_id = "0"
        
    def setData(self, index, value):
        """Sets role data at index with value.  Calls setXXX()."""
        if index.row() == -1:
            # setup for new row insertion
            ok = True
            if index.column() == 1:
                self.grpround_id = value
            elif index.column() == 2:
                self.group_id = value
            elif index.column() == 3:
                self.round_id = value
        elif index.row() == 0:
            # update into existing row
            if index.column() == 1:
                ok = self.setGroupRoundID(value)
            elif index.column() == 2:
                ok = self.setGroupID(value)
            elif index.column() == 3:
                ok = self.setRoundID(value)
        return ok

    def setGroupRoundID(self, grpround_id):
        """Sets group round ID key in GroupMatches table."""
        updateString = QString("UPDATE %1 SET grpround_id = ? WHERE match_id = ?").arg(self.table)
        updateQuery = QSqlQuery()
        updateQuery.prepare(updateString)
        updateQuery.addBindValue(grpround_id)
        updateQuery.addBindValue(self.primary_id)
        return updateQuery.exec_()
        
    def setGroupID(self, group_id):
        """Sets group ID key in GroupMatches table."""
        updateString = QString("UPDATE %1 SET group_id = ? WHERE match_id = ?").arg(self.table)
        updateQuery = QSqlQuery()
        updateQuery.prepare(updateString)
        updateQuery.addBindValue(group_id)
        updateQuery.addBindValue(self.primary_id)
        return updateQuery.exec_()

    def setRoundID(self, round_id):
        """Sets round ID key in GroupMatches table."""
        updateString = QString("UPDATE %1 SET round_id = ? WHERE match_id = ?").arg(self.table)
        updateQuery = QSqlQuery()
        updateQuery.prepare(updateString)
        updateQuery.addBindValue(round_id)
        updateQuery.addBindValue(self.primary_id)
        return updateQuery.exec_()
        
    def submit(self):
        """Inserts new row into database if no prior record exists.  
        
        Row updates are handled by setGroupRoundID(), setGroupID(), setRoundID().
        """
        insertString = QString("INSERT INTO %1 (match_id, grpround_id, group_id, round_id) VALUES (?,?,?,?)").arg(self.table)
        
        # test for already existing record in table
        query = QSqlQuery()
        query.prepare(QString("SELECT COUNT(*) FROM %1 WHERE match_id = ?").arg(self.table))
        query.addBindValue(self.primary_id)
        query.exec_()
        if query.isActive():
            query.next()
            numMatches = query.value(0).toInt()[0]
            if not numMatches:
                # no prior record...insert new row
                insertQuery = QSqlQuery()
                insertQuery.prepare(insertString)
                insertQuery.addBindValue(self.primary_id)
                insertQuery.addBindValue(self.grpround_id)
                insertQuery.addBindValue(self.group_id)
                insertQuery.addBindValue(self.round_id)
                ok = insertQuery.exec_()
                
                self.resetID()
        else:
            ok = False
        return ok
        
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
#        print "Calling init() in KnockoutLinkingModel"
        
        self.table = tbl_name
        self.primary_id = parent.matchID_display.text()
        self.koround_id = "0"
        self.matchday_id = "0"
        self.setQuery(QString("SELECT match_id, koround_id, matchday_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
        
    def refresh(self):
        """Refreshes query model."""
        self.setQuery(QString("SELECT match_id, koround_id, matchday_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
    
    def resetID(self):
        """Resets member variables in class."""
        self.koround_id = "0"
        self.matchday_id = "0"
        
    def setData(self, index, value):
        """Sets role data at index with value.  Calls setCompositeKey()."""
        if index.row() == -1:
            # setup for new row insertion
            ok = True
            if index.column() == 1:
                self.koround_id = value
            elif index.column() == 2:
                self.matchday_id = value
        elif index.row() == 0:
            # update into existing row
            if index.column() == 1:
                ok = self.setKnockoutID(value)
            elif index.column() == 2:
                ok = self.setMatchdayID(value)
        return ok

    def setKnockoutID(self, koround_id):
        """Sets knockout ID key in KnockoutMatches table."""
        updateString = QString("UPDATE %1 SET koround_id = ? WHERE match_id = ?").arg(self.table)
        updateQuery = QSqlQuery()
        updateQuery.prepare(updateString)
        updateQuery.addBindValue(koround_id)
        updateQuery.addBindValue(self.primary_id)
        return updateQuery.exec_()
        
    def setMatchdayID(self, matchday_id):
        """Sets matchday ID key in KnockoutMatches table."""
        updateString = QString("UPDATE %1 SET matchday_id = ? WHERE match_id = ?").arg(self.table)
        updateQuery = QSqlQuery()
        updateQuery.prepare(updateString)
        updateQuery.addBindValue(matchday_id)
        updateQuery.addBindValue(self.primary_id)
        return updateQuery.exec_()
        
    def submit(self):
        """Inserts new row into database if no prior record exists.  
        
        Row updates are handled by setKnockoutID() and setMatchdayID().
        """
        insertString = QString("INSERT INTO %1 (match_id, koround_id, matchday_id) VALUES (?,?,?)").arg(self.table)
        
        # test for already existing record in table
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) FROM tbl_knockoutmatches WHERE match_id = ?")
        query.addBindValue(self.primary_id)
        query.exec_()
        if query.isActive():
            query.next()
            numMatches = query.value(0).toInt()[0]
            if not numMatches:
                # no prior record...insert new row
                insertQuery = QSqlQuery()
                insertQuery.prepare(insertString)
                insertQuery.addBindValue(self.primary_id)
                insertQuery.addBindValue(self.koround_id)
                insertQuery.addBindValue(self.matchday_id)
                ok = insertQuery.exec_()
                
                self.resetID()
        else:
            ok = False
        return ok
        
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
#        print "Calling init() in LeagueLinkingModel"
        
        self.table = tbl_name
        self.primary_id = parent.matchID_display.text()
        self.setQuery(QString("SELECT match_id, round_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
        
    def refresh(self):
        """Refreshes query model."""
        self.setQuery(QString("SELECT match_id, round_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
        
    def setCompositeKey(self, index, match_id, round_id):
        """Inserts or updates entry in database."""
#        print "Calling setCompositeKey() in LeagueLinkingModel"
        # setup SQL statements
        insertString = QString("INSERT INTO %1 (match_id, round_id) VALUES (?,?)").arg(self.table)
        updateString = QString("UPDATE %1 SET round_id = ? WHERE enviro_id = ?").arg(self.table)
        
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
            print "Error with entry Query"
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
#        print "Calling init() in WeatherLinkingModel"
        
        self.table = tbl_name
        self.primary_id = parent.enviroID_display.text()
        self.setQuery(QString("SELECT enviro_id, weather_id FROM %1 WHERE enviro_id = %2").arg(self.table).arg(self.primary_id))
        
    def refresh(self):
        """Refreshes query model."""
        self.setQuery(QString("SELECT enviro_id, weather_id FROM %1 WHERE enviro_id = %2").arg(self.table).arg(self.primary_id))
        
    def setCompositeKey(self, index, enviro_id, weather_id):
        """Inserts or updates entry in database."""
#        print "Calling setCompositeKey() in WeatherLinkingModel"
        # setup SQL statements
        insertString = QString("INSERT INTO %1 (enviro_id, weather_id) VALUES (?,?)").arg(self.table)
        updateString = QString("UPDATE %1 SET weather_id = ? WHERE enviro_id = ?").arg(self.table)
        
        if index.row() == -1:
#            print "No entries of ID %s in linking table" % enviro_id
            # insert into table if no existing match_id record in linking table
            insertQuery = QSqlQuery()
            insertQuery.prepare(insertString)
            insertQuery.addBindValue(enviro_id)
            insertQuery.addBindValue(weather_id)
            return insertQuery.exec_()
        elif index.row() == 0:
#            print "Entry of ID %s in linking table" % enviro_id
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
#        print "Calling init() in TeamLinkingModel"
        
        self.table = tbl_name
        self.primary_id = parent.matchID_display.text()
        self.setQuery(QString("SELECT match_id, team_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
        
    def refresh(self):
        """Refreshes query model."""
        self.setQuery(QString("SELECT match_id, team_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
     
    def setCompositeKey(self, index,  match_id, team_id):
        """Inserts or updates entry in database."""
#        print "Calling setCompositeKey() in TeamLinkingModel"
        # setup SQL statements
        insertString = QString("INSERT INTO %1 (match_id,team_id) VALUES (?,?)").arg(self.table)
        updateString = QString("UPDATE %1 SET team_id = ? WHERE match_id = ?").arg(self.table)
        
        if index.row() == -1:
#            print "No entries of ID %s in linking table" % match_id
            # insert into table if no existing match_id record in linking table
            insertQuery = QSqlQuery()
            insertQuery.prepare(insertString)
            insertQuery.addBindValue(match_id)
            insertQuery.addBindValue(team_id)
            return insertQuery.exec_()
        elif index.row() == 0:
#            print "Entry of ID %s in linking table" % match_id
            # update into table if there exists match_id record in linking table
            updateQuery = QSqlQuery()
            updateQuery.prepare(updateString)
            updateQuery.addBindValue(team_id)
            updateQuery.addBindValue(match_id)
            return updateQuery.exec_()
        else:
            # any other failure, return False
#            print "Error with entry Query"
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
#        print "Calling init() in SubstituteLinkingModel"
        
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
#        print "Calling setCompositeKey() in SubstituteLinkingModel"
        # set up SQL statements
        insertString = QString("INSERT INTO %1 (subs_id,lineup_id) VALUES (?,?)").arg(self.table)
        updateString = QString("UPDATE %1 SET lineup_id = ? WHERE subs_id = ?").arg(self.table)
        
        if index.row() == -1:
#            print "No entries of ID %s in linking table" % subs_id
            # insert into table if no existing subs_id record in linking table
            insertQuery = QSqlQuery()
            insertQuery.prepare(insertString)
            insertQuery.addBindValue(subs_id)
            insertQuery.addBindValue(lineup_id)
            return insertQuery.exec_()
        elif index.row() == 0:
#            print "Entry of ID %s in linking table" % subs_id
            # update into table if there exists subs_id record in linking table
            updateQuery = QSqlQuery()
            updateQuery.prepare(updateString)
            updateQuery.addBindValue(subs_id)
            updateQuery.addBindValue(lineup_id)
            return updateQuery.exec_()
        else:
            # any other failure, return False
            print "Error with entry Query"
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
#        print "Calling init() in ManagerLinkingModel"

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
#        print "Calling setCompositeKey() in ManagerLinkingModel"
        # set up SQL statements
        insertString = QString("INSERT INTO %1 (match_id,manager_id) VALUES (?,?)").arg(self.table)
        updateString = QString("UPDATE %1 SET manager_id = ? WHERE match_id = ?").arg(self.table)
        
        if index.row() == -1:
#            print "No entries of ID %s in linking table" % match_id
            # insert into table if no existing match_id record in linking table
            insertQuery = QSqlQuery()
            insertQuery.prepare(insertString)
            insertQuery.addBindValue(match_id)
            insertQuery.addBindValue(manager_id)
            return insertQuery.exec_()
        elif index.row() == 0:
#            print "Entry of ID %s in linking table" % match_id
            # update into table if there exists match_id record in linking table
            updateQuery = QSqlQuery()
            updateQuery.prepare(updateString)
            updateQuery.addBindValue(manager_id)
            updateQuery.addBindValue(match_id)
            return updateQuery.exec_()
        else:
            # any other failure, return False
            print "Error with entry Query"
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
