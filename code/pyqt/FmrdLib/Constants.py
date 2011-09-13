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

"""Contains constants and initial table ID numbers for use in application source code."""

# #############
# Software version
# #############

DATAENTRY_VERSION = "1.1.0"
SQL_VERSION = "1.1.1"

# #############
# Table IDs
# #############

# personnel table IDs
MinManagerID       = "1000"
MinRefereeID       = "1000"
MinPlayerID        = "100000"
MinLineupID        = "1000000"
MinPlayerHistoryID = "1000000"

# match overview table IDs
MinCompetitionID  = "100"
MinTimeZoneID     = "100"
MinVenueID        = "1000"
MinTeamID         = "10000"
MinVenueHistoryID = "10000"
MinEnviroID       = "1000000"
MinMatchID        = "1000000"

# match event table IDs
MinPenaltyID      = "10000"
MinGoalID         = "100000"
MinOffenseID      = "100000"
MinSubstitutionID = "100000"
MinSwitchID       = "100000"

# auxiliary table IDs
MinCardID             = "1"
MinFieldID             = "1"
MinFlankID            = "1"
MinGoalStrikeID     = "1"
MinPenOutcomeID = "1"
MinSurfaceID         = "1"
MinConfedID          = "10"
MinFoulID              = "10"
MinGoalEventID     = "10"
MinPositionID         = "10"
MinRoundID           = "10"
MinWeatherID        = "10"
MinCountryID         = "100"

# #############
# Constants
# #############

# switchboard type definition
USER = 1
ADMIN = 2

# Define maximum number of login attempts
MAXLOGINS = 3

# Navigation enums
NULL, FIRST,  PREV,  NEXT,  LAST = range(5)

# Define minimum number of personnel 
MIN_STARTERS = 11
MIN_SUBSTITUTES = 3
MIN_STARTING_CAPTAINS = 1
MIN_STARTING_GOALKEEPERS = 1
MIN_MANAGERS = 2
MIN_REFEREES = 1

# Define minimum number of entities
MIN_VENUES = 1
MIN_COMPETITIONS = 1

# Define maximum number of entities for a team lineup
MAX_TEAM_STARTERS = 11
MAX_TEAM_STARTING_CAPTAINS = 1
MAX_TEAM_STARTING_GOALKEEPERS = 1
