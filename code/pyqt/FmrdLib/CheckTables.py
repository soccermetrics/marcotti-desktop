#!/usr/bin/env python
#
#    Desktop-based data entry tool for the Football Match Result Database (FMRD)
#
#    Copyright (C) 2010-2012, Howard Hamilton
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
from FmrdLib import Constants

"""Contains functions that count number of records in FMRD tables."""

def CheckMinimumCompetitions():
    """Check Competitions table and returns True if there is at least one record in it."""
    CompetitionQuery = QSqlQuery()
    CompetitionQuery.prepare("SELECT COUNT(*) FROM tbl_competitions")
    CompetitionQuery.exec_()
    
    if CompetitionQuery.isActive():
        CompetitionQuery.next()
        numCompetitions = CompetitionQuery.value(0).toInt()[0]
        if numCompetitions >= Constants.MIN_COMPETITIONS:
            return 1
        else:
            return 0
    else:
        return 0

def CheckMinimumVenues():
    """Check Venues table and returns True if there is at least one record in it."""
    VenuesQuery = QSqlQuery()
    VenuesQuery.prepare("SELECT COUNT(*) FROM tbl_venues")
    VenuesQuery.exec_()
    
    if VenuesQuery.isActive():
        VenuesQuery.next()
        numVenues = VenuesQuery.value(0).toInt()[0]
        if numVenues >= Constants.MIN_VENUES:
            return 1
        else:
            return 0
    else:
        return 0
    
def CheckMinimumManagers():
    """Check Managers table and returns True if there are at least two records in it."""
    ManagerQuery = QSqlQuery()
    ManagerQuery.prepare("SELECT COUNT(*) FROM tbl_managers")
    ManagerQuery.exec_()

    if ManagerQuery.isActive():
        ManagerQuery.next()
        numManagers = ManagerQuery.value(0).toInt()[0]
        if numManagers >= Constants.MIN_MANAGERS:
            return 1
        else:
            return 0
    else:
        return 0

def CheckMinimumReferees():
    """Check Referees table and returns True if there is at least one record in it."""
    RefereeQuery = QSqlQuery()
    RefereeQuery.prepare("SELECT COUNT(*) FROM tbl_referees")
    RefereeQuery.exec_()
    
    if RefereeQuery.isActive():
        RefereeQuery.next()
        numReferees = RefereeQuery.value(0).toInt()[0]
        if numReferees >= Constants.MIN_REFEREES:
            return 1
        else:
            return 0
    else:
        return 0

def CheckMinimumMatchCriteria():
    """Checks minimum criteria for match entry.
    
    Returns True if all of the following conditions are met:
        (1) at least one record in Referees table
        (2) at least two records in Managers table
        (3) at least one record in Venues table
        (4) at least one record in Competitions table    
    """
    if CheckMinimumCompetitions() and CheckMinimumVenues():
        if CheckMinimumManagers() and CheckMinimumReferees():
            return 1
                
    return 0

def CheckMinimumLineups():
    """Checks minimum criteria for match event entry.
    
    Returns True if all of the following conditions are met:
        (1) at least 11 entries in Lineups table where Starting = TRUE
        (2) at least one starting player in Lineups table where Captain = TRUE
        (3) at least one starting player in Lineups table at Goalkeeper position
    """
    StartersQuery = QSqlQuery()
    StartersQuery.prepare("SELECT COUNT(*) FROM tbl_lineups WHERE lp_starting = 'true'")
    StartersQuery.exec_()
    
    CaptainQuery = QSqlQuery()
    CaptainQuery.prepare("SELECT COUNT(*) FROM tbl_lineups WHERE lp_starting = 'true' AND lp_captain = 'true'")
    CaptainQuery.exec_()
    
    GoalkeeperQuery = QSqlQuery()
    GoalkeeperQuery.prepare("SELECT COUNT(*) FROM tbl_lineups WHERE lp_starting = 'true' AND "
                                            "position_id IN (SELECT position_id from positions_list WHERE position_name = ?)")
    GoalkeeperQuery.addBindValue(QVariant("Goalkeeper"))
    GoalkeeperQuery.exec_()
    if StartersQuery.isActive() and CaptainQuery.isActive() and GoalkeeperQuery.isActive():
        StartersQuery.next()
        numStarters = StartersQuery.value(0).toInt()[0]
        
        CaptainQuery.next()
        numCaptains = CaptainQuery.value(0).toInt()[0]
        
        GoalkeeperQuery.next()
        numGoalkeepers = GoalkeeperQuery.value(0).toInt()[0]
        
        if (numStarters >= Constants.MIN_STARTERS) and \
        (numCaptains >= Constants.MIN_STARTING_CAPTAINS) and \
        (numGoalkeepers >= Constants.MIN_STARTING_GOALKEEPERS):
            return 1
        else:
            return 0
    else:
        return 0

def CheckMinimumSubstitutes():
    """Checks minimum criteria for substitution data entry.
    
    Returns True if there is at least one record in Lineups table where Starting = FALSE.
    
    """
    SubstituteQuery = QSqlQuery()
    SubstituteQuery.prepare("SELECT COUNT(*) FROM tbl_lineups WHERE lp_starting = 'false'")
    SubstituteQuery.exec_()
    
    if SubstituteQuery.isActive():
        SubstituteQuery.next()
        numSubstitutes = SubstituteQuery.value(0).toInt()[0]
        
        if numSubstitutes >= Constants.MIN_SUBSTITUTES:
            return 1
        else:
            return 0
    else:
        return 0

def CheckMinimumKnockoutMatches():
    """Checks minimum criteria for penalty shootout entry.
    
    Returns TRUE if there is at least one record in Knockout Matches table.
    
    """
    KnockoutQuery = QSqlQuery()
    KnockoutQuery.prepare("SELECT COUNT(*) FROM tbl_knockoutmatches")
    KnockoutQuery.exec_()
    
    if KnockoutQuery.isActive():
        KnockoutQuery.next()
        numKnockoutMatches = KnockoutQuery.value(0).toInt()[0]
        
        if numKnockoutMatches >= Constants.MIN_KNOCKOUT_MATCHES:
            return 1
        else:
            return 0
    else:
        return 0

def CountStarters(match_id, team_id):
    """Counts number of starters for a team in Lineup table and returns an integer.
    
    Returns number of entries where starter = TRUE.
    Arguments:
        match_id - ID number from Matches table
        team_id - ID number from Countries table
        
    """
    StartersQuery = QSqlQuery()
    StartersQuery.prepare("SELECT COUNT(*) FROM tbl_lineups WHERE match_id=? AND lp_starting = 'true' \
                          AND player_id IN (SELECT player_id FROM tbl_players WHERE country_id=?)")
    StartersQuery.addBindValue(QVariant(match_id))
    StartersQuery.addBindValue(QVariant(team_id))
    StartersQuery.exec_()
    
    if StartersQuery.next():
        return StartersQuery.value(0).toInt()[0]
    else:
        return 0
        
def CountSubstitutes(match_id, team_id):
    """Counts number of substitutes for a team in Lineup table and returns an integer.
    
    Returns number of entries where starter = FALSE.
    Arguments:
        match_id - ID number from Matches table
        team_id - ID number from Countries table
        
    """
    SubstituteQuery = QSqlQuery()
    SubstituteQuery.prepare("SELECT COUNT(*) FROM tbl_lineups WHERE match_id=? AND lp_starting = 'false' \
                          AND player_id IN (SELECT player_id FROM tbl_players WHERE country_id=?)")
    SubstituteQuery.addBindValue(QVariant(match_id))
    SubstituteQuery.addBindValue(QVariant(team_id))
    SubstituteQuery.exec_()
    
    if SubstituteQuery.next():
        return SubstituteQuery.value(0).toInt()[0]
    else:
        return 0

def CountCaptains(match_id, team_id):
    """Counts number of captains for a team in Lineup table and returns an integer.
    
    Returns number of entries where captain = TRUE.
    Arguments:
        match_id - ID number from Matches table
        team_id - ID number from Countries table
    
    """
    CaptainQuery = QSqlQuery()
    CaptainQuery.prepare("SELECT COUNT(*) FROM tbl_lineups WHERE match_id=? AND lp_starting = 'true' AND lp_captain = 'true' \
                          AND player_id IN (SELECT player_id FROM tbl_players WHERE country_id=?)")
    CaptainQuery.addBindValue(QVariant(match_id))
    CaptainQuery.addBindValue(QVariant(team_id))
    CaptainQuery.exec_()
    
    if CaptainQuery.next():
        return CaptainQuery.value(0).toInt()[0]
    else:
        return 0

def CountGoalkeepers(match_id, team_id):
    """Counts number of goalkeepers for a team in Lineup table and returns an integer.
    
    Returns number of entries where starter = TRUE and position ID corresponds to Goalkeeper.
    Arguments:
        match_id - ID number from Matches table
        team_id - ID number from Countries table
        
    """
    
    GoalkeeperQuery = QSqlQuery()
    GoalkeeperQuery.prepare("SELECT COUNT(*) FROM tbl_lineups WHERE match_id=? AND lp_starting = 'true' \
                        AND player_id IN (SELECT player_id FROM tbl_players WHERE country_id=?) \
                        AND position_id IN (SELECT position_id FROM positions_list WHERE position_name = ?)")
    GoalkeeperQuery.addBindValue(QVariant(match_id))
    GoalkeeperQuery.addBindValue(QVariant(team_id))
    GoalkeeperQuery.addBindValue(QVariant("Goalkeeper"))                        
    GoalkeeperQuery.exec_()
    
    if GoalkeeperQuery.next():
        return GoalkeeperQuery.value(0).toInt()[0]
    else:
        return 0

def CountChildRecords(list, field, id):
    """Counts number of records in child table that refer to a field ID belonging to a parent table and returns an integer.
    
    Arguments:
        list - list of tables (string)
        field - name of foreign key field  (string)
        id - ID number of foreign key field (string)
        
    """

    numRecords = 0
    query = QSqlQuery()
    for table in list:
        queryString = QString("SELECT COUNT(*) FROM %1 WHERE %2=?").arg(table).arg(field)
        query.prepare(queryString)
        query.addBindValue(id)
        query.exec_()
        if query.next():
            numRecords += query.value(0).toInt()[0]
        else:
            return -1
    return numRecords

def CheckDuplicateRecords(field, table, desc):
    """Check for duplicate record before record is committed to database.
    
    Arguments:
        field - name of descriptor field in table (string)
        table - name of database table (string)
        desc - descriptor field in data entry form (string)
    If there is a duplicate, return TRUE.  Otherwise, return FALSE.
    """
    
    # trim whitespace from descriptor
    desc = desc.trimmed()
    
    query = QSqlQuery()
    queryString = QString("SELECT COUNT(*) FROM %1 WHERE %2=?").arg(table).arg(field)
    query.prepare(queryString)
    query.addBindValue(desc)
    query.exec_()
    if query.next():
        if query.value(0).toInt()[0]:
            return True
        else:
            return False
    else:
        return True

