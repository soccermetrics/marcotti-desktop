#!/usr/bin/env python
#
#    User interface autocoder for the Football Match Result Database (FMRD)
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

import os
import subprocess

mainDir = "FmrdMain/"
adminDir = "FmrdAdmin/"
guiDir = "gui/"

GuiMainList = ["competition_entry.ui",
            	 "enviro_entry.ui",
            	 "fmrd_login.ui",
            	 "goal_entry.ui",
            	 "lineup_select.ui",
            	 "main_switchboard.ui",
            	 "manager_entry.ui",
            	 "match_entry.ui",
            	 "offense_entry.ui",
            	 "penalty_entry.ui",
            	 "penshootout_entry.ui",
            	 "player_entry.ui",
            	 "playerhistory_entry.ui",
            	 "referee_entry.ui",
            	 "subs_entry.ui",
            	 "switchpos_entry.ui",
            	 "team_entry.ui",
            	 "main_userswitchboard.ui",
            	 "venue_entry.ui",
            	 "venuehistory_entry.ui"]   
            
MainList = ["ui_competitionentry.py",           		
            "ui_enviroentry.py", 
            "ui_fmrdlogin.py", 
            "ui_goalentry.py", 
            "ui_lineupentry.py", 
            "ui_mainswitchboard.py", 
            "ui_managerentry.py",
            "ui_matchentry.py",
            "ui_offenseentry.py",
            "ui_penaltyentry.py",
            "ui_penshootoutentry.py",
            "ui_playerentry.py", 
            "ui_playerhistoryentry.py",
            "ui_refereeentry.py",
            "ui_subsentry.py", 
            "ui_switchentry.py", 
            "ui_teamentry.py", 
            "ui_usermainswitchboard.py",
            "ui_venueentry.py",
            "ui_venuehistoryentry.py"]      
            
GuiAdminList = ["card_setup.ui",
                "confederation_setup.ui",
                "country_setup.ui",
                "fieldpos_setup.ui",
                "flankpos_setup.ui",
                "fouls_setup.ui",
                "goalevent_setup.ui",
                "goalstrike_setup.ui",
                "group_setup.ui",
                "grpround_setup.ui",
                "koround_setup.ui",
                "matchday_setup.ui",
                "penoutcome_setup.ui",
                "phase_setup.ui",
                "position_setup.ui",
                "round_setup.ui",
                "timezone_setup.ui",
                "venuesurface_setup.ui",
                "weather_setup.ui"]          

AdminList = ["ui_cardsetup.py",     
             "ui_confederationsetup.py", 
             "ui_countrysetup.py",
             "ui_fieldpossetup.py",  
             "ui_flankpossetup.py",  
             "ui_foulsetup.py",  
             "ui_goaleventsetup.py",
             "ui_goalstrikesetup.py",
             "ui_groupsetup.py",
             "ui_grproundsetup.py",
             "ui_koroundsetup.py",
             "ui_matchdaysetup.py",               
             "ui_penoutcomesetup.py",  
             "ui_phasesetup.py",
             "ui_positionsetup.py",  
             "ui_roundsetup.py",
             "ui_timezonesetup.py",  
             "ui_venuesurfacesetup.py", 
             "ui_weathersetup.py"]
             
guiResourceFile = "fmrd_resources.qrc"
resourceFile = "fmrd_resources_rc.py"
                   
print "Autoencoding main UIs..."                   
for mainFile,guiFile in zip(MainList,GuiMainList):
	if not os.path.isfile(mainDir+mainFile) or \
	 os.path.getmtime(mainDir+mainFile) < os.path.getmtime(guiDir+guiFile):
		print "Building %s" % mainFile
		subprocess.call("pyuic4 -o "+mainDir+mainFile+" "+guiDir+guiFile,shell=True)
	else:
		print "%s: No need to rebuild" % mainFile

print "Autoencoding setup UIs..."
for adminFile,guiFile in zip(AdminList,GuiAdminList):
	if not os.path.isfile(adminDir+adminFile) or \
	 os.path.getmtime(adminDir+adminFile) < os.path.getmtime(guiDir+guiFile):
		print "Building %s" % adminFile
		subprocess.call("pyuic4 -o "+adminDir+adminFile+" "+guiDir+guiFile,shell=True)		
	else:
		print "%s: No need to rebuild" % adminFile
	
print "Autoencoding resource files..."
for localDir in (adminDir,mainDir):
	if not os.path.isfile(localDir+resourceFile) or \
	 os.path.getmtime(localDir+resourceFile) < os.path.getmtime(guiDir+guiResourceFile):
		print "Building %s" % resourceFile
		subprocess.call("pyrcc4 -o "+localDir+resourceFile+" "+guiDir+guiResourceFile,shell=True)		
	else:
		print "%s: No need to rebuild" % resourceFile		
		
print "Autocoding complete."		
