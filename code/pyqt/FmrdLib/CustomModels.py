#!/usr/bin/env python
#
#    Football Match Result Database (FMRD)
#    Desktop-based data entry tool
#
#    Contains generic classes that implement specialized models for
#    use in FMRD tools.
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

class LinkingSqlModel(QSqlQueryModel):
    
    def __init__(self, parent=None):
        super(LinkingSqlModel, self).__init__(parent)
        print "Calling init() in LinkingSqlModel"
        
    # Method: flags
    # 
    # Define item flags for index.  Make second element in table record editable.
    def flags(self, index):
        
        flags = QSqlQueryModel.flags(index)
        if index.column() == 1:
            flags |= Qt.ItemIsEditable
        
        return flags
    
    # Method: setID
    #
    # Set match_id member of class.
    def setID(self, value):
        self.primary_id = value
    
    # Method: setData
    #
    # Set role data at index with value.  Calls setCompositeKey().
    def setData(self, index, value):
        
        ok = False
        print "Calling setData() in LinkingSqlModel"
        print "%d  %d" % (index.row(),  index.column())
        ok = self.setCompositeKey(index,  self.primary_id, value.toString())
        self.refresh()
        return ok
       
    # Method: setCompositeKey
    # 
    # Insert or update operation to database.
    # This method returns false in class definition,
    # must be implemented by subclass
    def setCompositeKey(self, index,  primary_id, secondary_id):
        print "Calling base setCompositeKey()"
        return False
        
class WeatherLinkingModel(LinkingSqlModel):

    def __init__(self, tbl_name, parent=None):
        super(WeatherLinkingModel, self).__init__(parent)
        print "Calling init() in WeatherLinkingModel"
        
        self.table = tbl_name
        self.primary_id = parent.enviroID_display.text()
        self.setQuery(QString("SELECT enviro_id, weather_id FROM %1 WHERE enviro_id = %2").arg(self.table).arg(self.primary_id))
        
    # Method: refresh
    #
    # Refresh query model
    def refresh(self):
        self.setQuery(QString("SELECT enviro_id, weather_id FROM %1 WHERE enviro_id = %2").arg(self.table).arg(self.primary_id))
        
    def setCompositeKey(self, index, enviro_id, weather_id):
        print "Calling setCompositeKey() in WeatherLinkingModel"
        # setup SQL statements
        insertString = QString("INSERT INTO %1 (enviro_id, weather_id) VALUES (?,?)").arg(self.table)
        updateString = QString("UPDATE %1 SET weather_id = ? WHERE enviro_id = ?").arg(self.table)
        
        if index.row() == -1:
            print "No entries of ID %s in linking table" % enviro_id
            # insert into table if no existing match_id record in linking table
            insertQuery = QSqlQuery()
            insertQuery.prepare(insertString)
            insertQuery.addBindValue(enviro_id)
            insertQuery.addBindValue(weather_id)
            return insertQuery.exec_()
        elif index.row() == 0:
            print "Entry of ID %s in linking table" % enviro_id
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
        
class TeamLinkingModel(LinkingSqlModel):
    
    def __init__(self, tbl_name, parent=None):
        super(TeamLinkingModel, self).__init__(parent)
        print "Calling init() in TeamLinkingModel"
        
        self.table = tbl_name
        self.primary_id = parent.matchID_display.text()
        self.setQuery(QString("SELECT match_id, team_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
        
    # Method: refresh
    #
    # Refresh query model
    def refresh(self):
        self.setQuery(QString("SELECT match_id, team_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
     
    def setCompositeKey(self, index,  match_id, team_id):
        
        print "Calling setCompositeKey() in TeamLinkingModel"
        # setup SQL statements
        insertString = QString("INSERT INTO %1 (match_id,team_id) VALUES (?,?)").arg(self.table)
        updateString = QString("UPDATE %1 SET team_id = ? WHERE match_id = ?").arg(self.table)
        
        if index.row() == -1:
            print "No entries of ID %s in linking table" % match_id
            # insert into table if no existing match_id record in linking table
            insertQuery = QSqlQuery()
            insertQuery.prepare(insertString)
            insertQuery.addBindValue(match_id)
            insertQuery.addBindValue(team_id)
            return insertQuery.exec_()
        elif index.row() == 0:
            print "Entry of ID %s in linking table" % match_id
            # update into table if there exists match_id record in linking table
            updateQuery = QSqlQuery()
            updateQuery.prepare(updateString)
            updateQuery.addBindValue(team_id)
            updateQuery.addBindValue(match_id)
            return updateQuery.exec_()
        else:
            # any other failure, return False
            print "Error with entry Query"
            return False    
            

class SubstituteLinkingModel(LinkingSqlModel):
    
    def __init__(self, tbl_name, parent=None):
        super(SubstituteLinkingModel, self).__init__(parent)
        print "Calling init() in SubstituteLinkingModel"
        
        self.table = tbl_name
        self.primary_id = parent.subsID_display.text()
        self.setQuery(QString("SELECT subs_id, lineup_id FROM %1 WHERE subs_id = %2").arg(self.table).arg(self.primary_id))
     
    def refresh(self):
        self.setQuery(QString("SELECT subs_id, lineup_id FROM %1 WHERE subs_id = %2").arg(self.table).arg(self.primary_id))
     
    def setCompositeKey(self, index, subs_id, lineup_id):
        
        print "Calling setCompositeKey() in SubstituteLinkingModel"
        # set up SQL statements
        insertString = QString("INSERT INTO %1 (subs_id,lineup_id) VALUES (?,?)").arg(self.table)
        updateString = QString("UPDATE %1 SET lineup_id = ? WHERE subs_id = ?").arg(self.table)
        
        if index.row() == -1:
            print "No entries of ID %s in linking table" % subs_id
            # insert into table if no existing subs_id record in linking table
            insertQuery = QSqlQuery()
            insertQuery.prepare(insertString)
            insertQuery.addBindValue(subs_id)
            insertQuery.addBindValue(lineup_id)
            return insertQuery.exec_()
        elif index.row() == 0:
            print "Entry of ID %s in linking table" % subs_id
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


class ManagerLinkingModel(LinkingSqlModel):
    
    def __init__(self, tbl_name, parent=None):
        super(ManagerLinkingModel, self).__init__(parent)
        print "Calling init() in ManagerLinkingModel"

        self.table = tbl_name
        self.primary_id = parent.matchID_display.text()
        self.setQuery(QString("SELECT match_id, manager_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))

    # Method: refresh
    #
    # Refresh query model
    def refresh(self):
        self.setQuery(QString("SELECT match_id, manager_id FROM %1 WHERE match_id = %2").arg(self.table).arg(self.primary_id))
     
    def setCompositeKey(self, index, match_id, manager_id):
        
        print "Calling setCompositeKey() in ManagerLinkingModel"
        # set up SQL statements
        insertString = QString("INSERT INTO %1 (match_id,manager_id) VALUES (?,?)").arg(self.table)
        updateString = QString("UPDATE %1 SET manager_id = ? WHERE match_id = ?").arg(self.table)
        
        if index.row() == -1:
            print "No entries of ID %s in linking table" % match_id
            # insert into table if no existing match_id record in linking table
            insertQuery = QSqlQuery()
            insertQuery.prepare(insertString)
            insertQuery.addBindValue(match_id)
            insertQuery.addBindValue(manager_id)
            return insertQuery.exec_()
        elif index.row() == 0:
            print "Entry of ID %s in linking table" % match_id
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
