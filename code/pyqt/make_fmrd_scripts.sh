#!/bin/bash
#
#    Make FMRD Python scripts from Qt user interface files
#
#    Copyright (C) 2011, Howard Hamilton
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

#echo "Cleanup existing Python bytecodes..."
# Clean pyc files from parent and FmrdAdmin/ and FmrdMain/ directories.
#rm *.pyc FmrdAdmin/*.pyc FmrdMain/*.pyc

# Convert UIs used by main FMRD tables.
echo "Autocoding FMRD main UIs..." 
#pyuic4 -o FmrdMain/ui_competitionentry.py gui/competition_entry.ui
#pyuic4 -o FmrdMain/ui_enviroentry.py gui/enviro_entry.ui
#pyuic4 -o FmrdMain/ui_fmrdlogin.py gui/fmrd_login.ui
#pyuic4 -o FmrdMain/ui_goalentry.py gui/goal_entry.ui
#pyuic4 -o FmrdMain/ui_lineupentry.py gui/lineup_select.ui
#pyuic4 -o FmrdMain/ui_mainswitchboard.py gui/main_switchboard.ui
#pyuic4 -o FmrdMain/ui_managerentry.py gui/manager_entry.ui
#pyuic4 -o FmrdMain/ui_matchentry.py gui/match_entry.ui
#pyuic4 -o FmrdMain/ui_offenseentry.py gui/offense_entry.ui
#pyuic4 -o FmrdMain/ui_penaltyentry.py gui/penalty_entry.ui
pyuic4 -o FmrdMain/ui_playerentry.py gui/player_entry.ui
pyuic4 -o FmrdMain/ui_playerhistoryentry.py gui/playerhistory_entry.ui
#pyuic4 -o FmrdMain/ui_refereeentry.py gui/referee_entry.ui
#pyuic4 -o FmrdMain/ui_subsentry.py gui/subs_entry.ui
#pyuic4 -o FmrdMain/ui_switchentry.py gui/switchpos_entry.ui
pyuic4 -o FmrdMain/ui_teamentry.py gui/team_entry.ui
#pyuic4 -o FmrdMain/ui_usermainswitchboard.py gui/main_userswitchboard.ui
pyuic4 -o FmrdMain/ui_venueentry.py gui/venue_entry.ui
pyuic4 -o FmrdMain/ui_venuehistoryentry.py gui/venuehistory_entry.ui

# Convert UIs used by setup and validation tables of FMRD.
echo "Autocoding FMRD setup UIs..."
#pyuic4 -o FmrdAdmin/ui_cardsetup.py gui/card_setup.ui
#pyuic4 -o FmrdAdmin/ui_confederationsetup.py gui/confederation_setup.ui
#pyuic4 -o FmrdAdmin/ui_countrysetup.py gui/country_setup.ui
#pyuic4 -o FmrdAdmin/ui_fieldpossetup.py gui/fieldpos_setup.ui
#pyuic4 -o FmrdAdmin/ui_flankpossetup.py gui/flankpos_setup.ui
#pyuic4 -o FmrdAdmin/ui_foulsetup.py gui/fouls_setup.ui 
#pyuic4 -o FmrdAdmin/ui_goaleventsetup.py gui/goalevent_setup.ui
#pyuic4 -o FmrdAdmin/ui_goalstrikesetup.py gui/goalstrike_setup.ui
#pyuic4 -o FmrdAdmin/ui_penoutcomesetup.py gui/penoutcome_setup.ui
#pyuic4 -o FmrdAdmin/ui_positionsetup.py gui/position_setup.ui
#pyuic4 -o FmrdAdmin/ui_roundsetup.py gui/round_setup.ui
pyuic4 -o FmrdAdmin/ui_timezonesetup.py gui/timezone_setup.ui    
pyuic4 -o FmrdAdmin/ui_venuesurfacesetup.py gui/venuesurface_setup.ui    
#pyuic4 -o FmrdAdmin/ui_weathersetup.py gui/weather_setup.ui

# Convert resources file and copy to FmrdMain/ and FmrdAdmin/.
#echo "Autocoding resources file..."
#pyrcc4 -o gui/fmrd_resources_rc.py gui/fmrd_resources.qrc
#echo "Copying resource file to FmrdMain/ and FmrdAdmin/..."
#cp gui/fmrd_resources_rc.py FmrdMain/
#mv gui/fmrd_resources_rc.py FmrdAdmin/

echo "Autocoding complete."