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
from FmrdLib import (CheckTables, Constants, MsgPrompts)
from FmrdLib.CustomDelegates import *
from FmrdLib.CustomModels import *
from FmrdLib.CheckTables import *

from fmrd_personnel import LineupEntryDlg

"""Contains classes that implement entry forms to match tables of FMRD.

Classes:
EnviroEntryDlg - data entry to Environments table
MatchEntryDlg - data entry to Matches table
"""

class MatchEntryDlg(QDialog, ui_matchentry.Ui_MatchEntryDlg):
    """Implements match entry dialog, and accesses and writes to Matches table.
    
    This dialog is one of the central dialogs of the database entry form. It accepts
    high-level data on the match and opens subdialogs on match lineups and 
    environmental conditions of the match.
    
    """
    
    ID,  DATE, HALF1, HALF2, EXTRA1, EXTRA2, ATTEND, COMP_ID, PHASE_ID, VENUE_ID, REF_ID = range(11)
    
    def __init__(self, parent=None):
        """Constructor for MatchEntryDlg class."""
        super(MatchEntryDlg, self).__init__(parent)
        self.setupUi(self)
        
        # define local parameters
        HOME_ID = AWAY_ID = 1
        TEAM_NAME = 1
        COUNTRY = 2
        CMP_ID,  COMP_NAME = range(2)
        PHS_ID,  PHASE_NAME = range(2)
        RND_ID,  ROUND_NAME = range(2)
        GRP_ID,  GROUP_NAME = range(2)
        MCH_ID,  MATCHDAY_NAME = range(2)
        VEN_ID,  VENUE_NAME = range(2)
        RF_ID,  REF_NAME,  REF_SORT = range(3)
        CONFED_ID, CONFED_NAME = range(2)
        MG_ID,  MGR_NAME,  MGR_SORT = range(3)
        
        GROUP_ROUND,  GROUP,  GROUP_MATCHDAY = range(1, 4)
        KO_ROUND, KO_MATCHDAY = range(1, 3)
        
        # define lists of comboboxes
        self.selectWidgets = (
            self.matchCompSelect, self.matchPhaseSelect, self.lgRoundSelect, 
            self.groupSelect, self.grpRoundSelect, self.grpMatchdaySelect, 
            self.koRoundSelect, self.koMatchdaySelect,  self.matchRefSelect, self.matchVenueSelect, 
            self.homeconfedSelect, self.hometeamSelect, self.homemgrSelect, 
            self.awayconfedSelect, self.awayteamSelect, self.awaymgrSelect
        )
        
        self.upperFormWidgets = (
            self.matchCompSelect, self.matchDateEdit, self.matchPhaseSelect
        )
        
        self.lowerFormWidgets = (
            self.matchRefSelect, self.matchVenueSelect, self.matchAttendanceEdit, self.firstHalfLengthEdit, 
            self.secondHalfLengthEdit, self.firstExtraLengthEdit, self.secondExtraLengthEdit,
        )
        
        self.phaseWidgets = (
            self.lgRoundSelect, self.koRoundSelect, self.koMatchdaySelect, self.groupSelect, 
            self.grpRoundSelect, self.grpMatchdaySelect                             
        )
        
        self.homeawayWidgets = (
            self.homeconfedSelect, self.hometeamSelect, self.homemgrSelect, 
            self.awayconfedSelect, self.awayteamSelect, self.awaymgrSelect, 
            self.homeLineupButton, self.awayLineupButton,  self.enviroButton
        )
        
        # define underlying database model (tbl_matches)
        # because of foreign keys, instantiate QSqlRelationalTableModel and define relations to it
        self.model = QSqlRelationalTableModel(self)
        self.model.setTable("tbl_matches")
        self.model.setRelation(MatchEntryDlg.COMP_ID, QSqlRelation("tbl_competitions", "competition_id", "comp_name"))
        self.model.setRelation(MatchEntryDlg.PHASE_ID, QSqlRelation("tbl_phases", "phase_id", "phase_desc"))
        self.model.setRelation(MatchEntryDlg.VENUE_ID, QSqlRelation("tbl_venues", "venue_id", "ven_name"))
        self.model.setRelation(MatchEntryDlg.REF_ID, QSqlRelation("referees_list", "referee_id", "full_name"))
        self.model.setSort(MatchEntryDlg.ID, Qt.AscendingOrder)
        self.model.select()
        
        # define main mapper (Matches)
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.setItemDelegate(QSqlRelationalDelegate(self))        

        # relation model for Competitions combobox
        self.compModel = self.model.relationModel(MatchEntryDlg.COMP_ID)
        self.compModel.setSort(CMP_ID, Qt.AscendingOrder)
        self.matchCompSelect.setModel(self.compModel)
        self.matchCompSelect.setModelColumn(self.compModel.fieldIndex("comp_name"))
        self.matchCompSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.matchCompSelect, MatchEntryDlg.COMP_ID)
        
        # relation model for Competition Phases combobox
        self.phaseModel = self.model.relationModel(MatchEntryDlg.PHASE_ID)
        self.phaseModel.setSort(PHS_ID, Qt.AscendingOrder)
        self.matchPhaseSelect.setModel(self.phaseModel)
        self.matchPhaseSelect.setModelColumn(self.phaseModel.fieldIndex("phase_desc"))
        self.matchPhaseSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.matchPhaseSelect, MatchEntryDlg.PHASE_ID)
        
        # relation model for Venues combobox
        self.venueModel = self.model.relationModel(MatchEntryDlg.VENUE_ID)
        self.venueModel.setSort(VENUE_NAME, Qt.AscendingOrder)
        self.matchVenueSelect.setModel(self.venueModel)
        self.matchVenueSelect.setModelColumn(self.venueModel.fieldIndex("ven_name"))
        self.matchVenueSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.matchVenueSelect, MatchEntryDlg.VENUE_ID)
        
        # relation model for Referees combobox
        self.refereeModel = self.model.relationModel(MatchEntryDlg.REF_ID)
        self.refereeModel.setSort(REF_SORT, Qt.AscendingOrder)
        self.matchRefSelect.setModel(self.refereeModel)
        self.matchRefSelect.setModelColumn(self.refereeModel.fieldIndex("full_name"))
        self.matchRefSelect.setCurrentIndex(-1)
        self.mapper.addMapping(self.matchRefSelect, MatchEntryDlg.REF_ID)        

        # map other widgets on form
        self.mapper.addMapping(self.matchID_display, MatchEntryDlg.ID)
        self.mapper.addMapping(self.matchDateEdit, MatchEntryDlg.DATE)
        self.mapper.addMapping(self.firstHalfLengthEdit, MatchEntryDlg.HALF1)
        self.mapper.addMapping(self.secondHalfLengthEdit, MatchEntryDlg.HALF2)
        self.mapper.addMapping(self.firstExtraLengthEdit, MatchEntryDlg.EXTRA1)
        self.mapper.addMapping(self.secondExtraLengthEdit, MatchEntryDlg.EXTRA2)
        self.mapper.addMapping(self.matchAttendanceEdit, MatchEntryDlg.ATTEND)
        self.mapper.toFirst()
        
        #
        # define models used for League matches
        #
        
        leagueRoundModel = QSqlTableModel(self)
        leagueRoundModel.setTable("tbl_rounds")
        leagueRoundModel.setSort(RND_ID, Qt.AscendingOrder)
        leagueRoundModel.select()
        
        # League Match linking model
        self.leagueMatchModel = LeagueLinkingModel("tbl_leaguematches", self)
        self.lgRoundSelect.setModel(leagueRoundModel)
        self.lgRoundSelect.setModelColumn(leagueRoundModel.fieldIndex("round_desc"))
        self.lgRoundSelect.setCurrentIndex(-1)
        
        # League Match mapper
        self.leagueMatchMapper = QDataWidgetMapper(self)
        self.leagueMatchMapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.leagueMatchMapper.setModel(self.leagueMatchModel)
        leagueMatchDelegate = GenericDelegate(self)
        leagueMatchDelegate.insertColumnDelegate(ROUND_NAME, RoundsComboBoxDelegate(self))
        self.leagueMatchMapper.setItemDelegate(leagueMatchDelegate)
        self.leagueMatchMapper.addMapping(self.lgRoundSelect, ROUND_NAME)
        self.leagueMatchMapper.toFirst()
        
        #
        # define models used for Group matches
        #
        
        groupNameModel = QSqlTableModel(self)
        groupNameModel.setTable("tbl_groups")
        groupNameModel.setSort(GRP_ID,  Qt.AscendingOrder)
        groupNameModel.select()
        
        groupRoundModel = QSqlTableModel(self)
        groupRoundModel.setTable("tbl_grouprounds")
        groupRoundModel.setSort(RND_ID, Qt.AscendingOrder)
        groupRoundModel.select()
        
        groupMatchdayModel = QSqlTableModel(self)
        groupMatchdayModel.setTable("tbl_rounds")
        groupMatchdayModel.setSort(RND_ID, Qt.AscendingOrder)
        groupMatchdayModel.select()
        
        # Group Match linking model
        self.groupMatchModel = GroupLinkingModel("tbl_groupmatches", self)
        self.groupSelect.setModel(groupNameModel)
        self.groupSelect.setModelColumn(groupNameModel.fieldIndex("group_desc"))
        self.groupSelect.setCurrentIndex(-1)
        self.grpRoundSelect.setModel(groupRoundModel)
        self.grpRoundSelect.setModelColumn(groupRoundModel.fieldIndex("grpround_desc"))
        self.grpRoundSelect.setCurrentIndex(-1)
        self.grpMatchdaySelect.setModel(groupMatchdayModel)
        self.grpMatchdaySelect.setModelColumn(groupMatchdayModel.fieldIndex("round_desc"))
        self.grpMatchdaySelect.setCurrentIndex(-1)
        
        # Group Match mapper
        self.groupMatchMapper = QDataWidgetMapper(self)
        self.groupMatchMapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.groupMatchMapper.setModel(self.groupMatchModel)
        groupMatchDelegate = GenericDelegate(self)
        groupMatchDelegate.insertColumnDelegate(GROUP, GroupsComboBoxDelegate(self))
        groupMatchDelegate.insertColumnDelegate(GROUP_ROUND, GroupRoundsComboBoxDelegate(self))
        groupMatchDelegate.insertColumnDelegate(GROUP_MATCHDAY, RoundsComboBoxDelegate(self))
        self.groupMatchMapper.setItemDelegate(groupMatchDelegate)
        self.groupMatchMapper.addMapping(self.groupSelect, GROUP)
        self.groupMatchMapper.addMapping(self.grpRoundSelect, GROUP_ROUND)
        self.groupMatchMapper.addMapping(self.grpMatchdaySelect, GROUP_MATCHDAY)
        self.groupMatchMapper.toFirst()
        
        #
        # define models used for Knockout matches
        #

        knockoutRoundModel = QSqlTableModel(self)
        knockoutRoundModel.setTable("tbl_knockoutrounds")
        knockoutRoundModel.setSort(RND_ID, Qt.AscendingOrder)
        knockoutRoundModel.select()
        
        knockoutMatchdayModel = QSqlTableModel(self)
        knockoutMatchdayModel.setTable("tbl_matchdays")
        knockoutMatchdayModel.setSort(MATCHDAY_NAME, Qt.AscendingOrder)
        knockoutMatchdayModel.select()
        
        # Knockout Match linking model
        self.knockoutMatchModel = KnockoutLinkingModel("tbl_knockoutmatches", self)
        self.koRoundSelect.setModel(knockoutRoundModel)
        self.koRoundSelect.setModelColumn(knockoutRoundModel.fieldIndex("koround_desc"))
        self.koRoundSelect.setCurrentIndex(-1)
        self.koMatchdaySelect.setModel(knockoutMatchdayModel)
        self.koMatchdaySelect.setModelColumn(knockoutMatchdayModel.fieldIndex("matchday_desc"))
        self.koMatchdaySelect.setCurrentIndex(-1)
        
        # Knockout Match mapper
        self.knockoutMatchMapper = QDataWidgetMapper(self)
        self.knockoutMatchMapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.knockoutMatchMapper.setModel(self.knockoutMatchModel)
        knockoutMatchDelegate = GenericDelegate(self)
        knockoutMatchDelegate.insertColumnDelegate(KO_ROUND, KnockoutRoundsComboBoxDelegate(self))
        knockoutMatchDelegate.insertColumnDelegate(KO_MATCHDAY, KnockoutMatchdayComboBoxDelegate(self))
        self.knockoutMatchMapper.setItemDelegate(knockoutMatchDelegate)
        self.knockoutMatchMapper.addMapping(self.koRoundSelect, KO_ROUND)
        self.knockoutMatchMapper.addMapping(self.koMatchdaySelect, KO_MATCHDAY)
        self.knockoutMatchMapper.toFirst()

        #
        # define models used in Team and Manager comboboxes
        # we need multiple instantiations of Teams and Managers tables
        # so that there is no confusion in SQL logic
        
        self.homeCountryModel = QSqlTableModel(self)
        self.homeCountryModel.setTable("tbl_countries")
        self.homeCountryModel.setSort(COUNTRY, Qt.AscendingOrder)
        self.homeCountryModel.select()
        
        self.awayCountryModel = QSqlTableModel(self)
        self.awayCountryModel.setTable("tbl_countries")
        self.awayCountryModel.setSort(COUNTRY, Qt.AscendingOrder)
        self.awayCountryModel.select()

        self.homeManagerModel = QSqlTableModel(self)
        self.homeManagerModel.setTable("managers_list")
        self.homeManagerModel.setSort(MGR_SORT, Qt.AscendingOrder)
        self.homeManagerModel.select()
        
        self.awayManagerModel = QSqlTableModel(self)
        self.awayManagerModel.setTable("managers_list")
        self.awayManagerModel.setSort(MGR_SORT, Qt.AscendingOrder)
        self.awayManagerModel.select()
        
        # set up Home Team linking table 
        # set up Home Team combobox with items from tbl_teams table
        self.hometeamModel = TeamLinkingModel("tbl_hometeams", self)
        self.hometeamSelect.setModel(self.homeCountryModel)
        self.hometeamSelect.setModelColumn(self.homeCountryModel.fieldIndex("cty_name"))
        self.hometeamSelect.setCurrentIndex(-1)

        # set up Away Team linking table
        # set up Away Team combobox with items from tbl_teams table
        self.awayteamModel = TeamLinkingModel("tbl_awayteams", self)
        self.awayteamSelect.setModel(self.awayCountryModel)
        self.awayteamSelect.setModelColumn(self.awayCountryModel.fieldIndex("cty_name"))
        self.awayteamSelect.setCurrentIndex(-1)

        # set up Home Manager linking table
        # set up Home Manager combobox with items from managers_list table
        self.homemgrModel = ManagerLinkingModel("tbl_homemanagers", self)
        self.homemgrSelect.setModel(self.homeManagerModel)
        self.homemgrSelect.setModelColumn(self.homeManagerModel.fieldIndex("full_name"))
        self.homemgrSelect.setCurrentIndex(-1)

        # set up Away Manager linking table
        # set up Away Manager combobox with items from managers_list table
        self.awaymgrModel = ManagerLinkingModel("tbl_awaymanagers", self)
        self.awaymgrSelect.setModel(self.awayManagerModel)
        self.awaymgrSelect.setModelColumn(self.awayManagerModel.fieldIndex("full_name"))
        self.awaymgrSelect.setCurrentIndex(-1)

        # Home Team mapper
        self.hometeamMapper = QDataWidgetMapper(self)
        self.hometeamMapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.hometeamMapper.setModel(self.hometeamModel)
        hometeamDelegate = GenericDelegate(self)
        hometeamDelegate.insertColumnDelegate(TEAM_NAME, HomeTeamComboBoxDelegate(self))
        self.hometeamMapper.setItemDelegate(hometeamDelegate)
        self.hometeamMapper.addMapping(self.hometeamSelect, TEAM_NAME)
        self.hometeamMapper.toFirst()
        
        # Away Team mapper
        self.awayteamMapper = QDataWidgetMapper(self)
        self.awayteamMapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.awayteamMapper.setModel(self.awayteamModel)
        awayteamDelegate = GenericDelegate(self)
        awayteamDelegate.insertColumnDelegate(TEAM_NAME, AwayTeamComboBoxDelegate(self))
        self.awayteamMapper.setItemDelegate(awayteamDelegate)
        self.awayteamMapper.addMapping(self.awayteamSelect, TEAM_NAME)
        self.awayteamMapper.toFirst()

        # Home Manager mapper
        self.homemgrMapper = QDataWidgetMapper(self)
        self.homemgrMapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.homemgrMapper.setModel(self.homemgrModel)
        homemgrDelegate = GenericDelegate(self)
        homemgrDelegate.insertColumnDelegate(MGR_NAME, HomeMgrComboBoxDelegate(self))
        self.homemgrMapper.setItemDelegate(homemgrDelegate)
        self.homemgrMapper.addMapping(self.homemgrSelect, MGR_NAME)
        self.homemgrMapper.toFirst()
        
        # Away Manager mapper
        self.awaymgrMapper = QDataWidgetMapper(self)
        self.awaymgrMapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.awaymgrMapper.setModel(self.awaymgrModel)
        awaymgrDelegate = GenericDelegate(self)
        awaymgrDelegate.insertColumnDelegate(MGR_NAME, AwayMgrComboBoxDelegate(self))
        self.awaymgrMapper.setItemDelegate(awaymgrDelegate)
        self.awaymgrMapper.addMapping(self.awaymgrSelect, MGR_NAME)
        self.awaymgrMapper.toFirst()        
        
        # define models used in Confederation comboboxes
        # these comboboxes are used to filter Country comboboxes
        # we need multiple instantiations of Confederations tables
        # so that there is no confusion in SQL logic
        
        # Home Confederation model
        self.homeconfedModel = QSqlTableModel(self)
        self.homeconfedModel.setTable("tbl_confederations")
        self.homeconfedModel.setSort(CONFED_ID, Qt.AscendingOrder)
        self.homeconfedModel.select()
    
        # Home Confederation combobox
        self.homeconfedSelect.setModel(self.homeconfedModel)
        self.homeconfedSelect.setModelColumn(self.homeconfedModel.fieldIndex("confed_name"))
        self.homeconfedSelect.setCurrentIndex(-1)
        
        # Home Confederation mapper 
        homeconfedMapper = QDataWidgetMapper(self)
        homeconfedMapper.setModel(self.homeconfedModel)
        homeconfedMapper.setItemDelegate(HomeConfedComboBoxDelegate(self))
        homeconfedMapper.addMapping(self.homeconfedSelect, CONFED_NAME)
        homeconfedMapper.toFirst()       
        
        # Away Confederation model
        self.awayconfedModel = QSqlTableModel(self)
        self.awayconfedModel.setTable("tbl_confederations")
        self.awayconfedModel.setSort(CONFED_ID, Qt.AscendingOrder)
        self.awayconfedModel.select()
    
        # Away Confederation combobox
        self.awayconfedSelect.setModel(self.awayconfedModel)
        self.awayconfedSelect.setModelColumn(self.awayconfedModel.fieldIndex("confed_name"))
        self.awayconfedSelect.setCurrentIndex(-1)
        
        # Away Confederation mapper 
        awayconfedMapper = QDataWidgetMapper(self)
        awayconfedMapper.setModel(self.awayconfedModel)
        awayconfedMapper.setItemDelegate(AwayConfedComboBoxDelegate(self))
        awayconfedMapper.addMapping(self.awayconfedSelect, CONFED_NAME)
        awayconfedMapper.toFirst()       

        # disable all fields if no records in database table
        if not self.model.rowCount():
            
            # disable form widgets
            for widget in self.upperFormWidgets:
                widget.setDisabled(True)
            
            # disable remaining form widgets
            for widget in self.lowerFormWidgets:
                widget.setDisabled(True)
                
            # disable phase-related widgets
            for widget in self.phaseWidgets:
                widget.setDisabled(True)
                
            # disable home/away widgets
            for widget in self.homeawayWidgets:
                widget.setDisabled(True)
            
            # disable save and delete entry buttons
            self.saveEntry.setDisabled(True)
            self.deleteEntry.setDisabled(True)
        
        # disable phase-related widgets if mapper points to first record
        if not self.mapper.currentIndex():
            self.matchPhaseSelect.setDisabled(True)
            for widget in self.phaseWidgets:
                widget.setDisabled(True)
            self.filterReferees()
                
        # disable First and Previous Entry buttons
        self.firstEntry.setDisabled(True)
        self.prevEntry.setDisabled(True)        
        
        # disable Next and Last Entry buttons if less than two records
        if self.model.rowCount() < 2:
            self.nextEntry.setDisabled(True)
            self.lastEntry.setDisabled(True)
            
        
        # configure signal/slots
        self.connect(self.firstEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.FIRST))
        self.connect(self.prevEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.PREV))
        self.connect(self.nextEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NEXT))
        self.connect(self.lastEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.LAST))
        self.connect(self.saveEntry, SIGNAL("clicked()"), lambda: self.saveRecord(Constants.NULL))
        self.connect(self.addEntry, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.deleteEntry, SIGNAL("clicked()"), self.deleteRecord)           
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)

        self.connect(self.mapper, SIGNAL("currentIndexChanged(int)"), 
                            lambda: self.updateConfed((self.homeconfedSelect, self.awayconfedSelect), (self.hometeamSelect, self.awayteamSelect)))
        
        self.connect(self.homeconfedSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.enableWidget(self.hometeamSelect))
        self.connect(self.awayconfedSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.enableWidget(self.awayteamSelect))

        self.connect(self.homeconfedSelect, SIGNAL("activated(int)"), 
                                                                        lambda: self.filterCountryBox(self.homeconfedSelect, self.hometeamSelect))
        self.connect(self.awayconfedSelect, SIGNAL("activated(int)"), 
                                                                        lambda: self.filterCountryBox(self.awayconfedSelect, self.awayteamSelect))
        self.connect(self.matchPhaseSelect, SIGNAL("currentIndexChanged(int)"), self.enablePhaseDetails)
        
        self.connect(self.lgRoundSelect, SIGNAL("currentIndexChanged(int)"),
                                                                lambda: self.enableWidget(self.matchVenueSelect))        
        self.connect(self.grpRoundSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                lambda: self.enableWidget(self.groupSelect))
        self.connect(self.groupSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                lambda: self.enableWidget(self.grpMatchdaySelect))
        self.connect(self.grpMatchdaySelect, SIGNAL("currentIndexChanged(int)"),
                                                                lambda: self.enableWidget(self.matchVenueSelect))

        self.connect(self.koRoundSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                lambda: self.enableWidget(self.koMatchdaySelect))
        self.connect(self.koMatchdaySelect, SIGNAL("currentIndexChanged(int)"),
                                                                lambda: self.enableWidget(self.matchVenueSelect))
                                                                
        self.connect(self.matchVenueSelect, SIGNAL("currentIndexChanged(int)"), self.enableAndFilterReferees)
        self.connect(self.matchRefSelect, SIGNAL("currentIndexChanged(int)"), self.enableDefaults)

        self.connect(self.hometeamSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.enableWidget(self.homemgrSelect))
        self.connect(self.hometeamSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.removeDuplicateTeam(self.awayteamSelect, self.hometeamSelect))
        self.connect(self.homemgrSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                     lambda: self.enableWidget(self.homeLineupButton))
        self.connect(self.homemgrSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                     lambda: self.enableWidget(self.awayconfedSelect))
        self.connect(self.homemgrSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                     lambda: self.removeDuplicateManager(self.awaymgrSelect, self.homemgrSelect))
        
        self.connect(self.awayteamSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.enableWidget(self.awaymgrSelect))
        self.connect(self.awayteamSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                      lambda: self.removeDuplicateTeam(self.hometeamSelect, self.awayteamSelect))
        self.connect(self.awaymgrSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                     lambda: self.enableWidget(self.awayLineupButton))
        self.connect(self.awaymgrSelect, SIGNAL("currentIndexChanged(int)"), 
                                                                     lambda: self.removeDuplicateManager(self.homemgrSelect, self.awaymgrSelect))

        self.connect(self.enviroButton, SIGNAL("clicked()"), lambda: self.openEnviros(self.matchID_display.text()))
        self.connect(self.homeLineupButton, SIGNAL("clicked()"), 
                                                                lambda: self.openLineups(self.matchID_display.text(), self.hometeamSelect.currentText()))
        self.connect(self.awayLineupButton, SIGNAL("clicked()"), 
                                                               lambda: self.openLineups(self.matchID_display.text(), self.awayteamSelect.currentText()))

    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if MsgPrompts.SaveDiscardOptionPrompt(self):
                if not self.mapper.submit():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                else:
                    self.submitForms()
        QDialog.accept(self)
    
    def submitForms(self):
        """Writes to linking tables."""
        
        mapperList = [self.hometeamMapper, self.awayteamMapper, self.homemgrMapper, self.awaymgrMapper]
        editorList = [self.hometeamSelect, self.awayteamSelect, self.homemgrSelect, self.awaymgrSelect]
        
        # write to home/away linking tables
        for mapper, editor in zip(mapperList, editorList):
            if not self.updateLinkingTable(mapper, editor, 0):
                return
        
        # write to specific Phase linking tables
        # update linking table, then call submit()
        phaseText = self.matchPhaseSelect.currentText()
        if phaseText == "League":
            self.updateLinkingTable(self.leagueMatchMapper, self.lgRoundSelect, 1)
            self.leagueMatchModel.submit()
        elif phaseText == "Group":
            editorList = [self.grpRoundSelect, self.groupSelect, self.grpMatchdaySelect]
            for editor,  column in zip(editorList, range(1, 4)):
                self.updateLinkingTable(self.groupMatchMapper, editor, column)
            self.groupMatchModel.submit()
        elif phaseText == "Knockout":
            editorList = [self.koRoundSelect, self.koMatchdaySelect]
            for editor,  column in zip(editorList, range(1, 3)):
                self.updateLinkingTable(self.knockoutMatchMapper, editor, column)                
            self.knockoutMatchModel.submit()
            
    def saveRecord(self, where):
        """"Submits changes to database, navigates through form, and resets subforms."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if MsgPrompts.SaveDiscardOptionPrompt(self):
                if not self.mapper.submit():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                else:
                    self.submitForms()
            else:
                self.mapper.revert()
        
        for widget in self.phaseWidgets:
            widget.blockSignals(True)
        
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
        self.mapper.setCurrentIndex(row)
                    
        # disable Phase comboboxes
        # prevent user from editing Competition Phase once record is saved
        self.matchPhaseSelect.setDisabled(True)
            
        # enable Delete button if at least one record
        if self.model.rowCount():
            self.deleteEntry.setEnabled(True)        
        
        # enable time boxes and refresh subforms
        currentID = self.matchID_display.text()
        phaseText = self.matchPhaseSelect.currentText()
        self.enableTimes(phaseText)
        self.resetPhaseDetails(phaseText)
        self.refreshSubForms(currentID)
        self.refreshPhaseForms(currentID, phaseText)
        
        for widget in self.phaseWidgets:
            widget.blockSignals(False)

    def refreshSubForms(self, currentID):
        """Sets match ID for linking models and refreshes models and mappers."""
        self.hometeamModel.setID(currentID)
        self.hometeamModel.refresh()
        
        self.awayteamModel.setID(currentID)
        self.awayteamModel.refresh()
        
        self.homemgrModel.setID(currentID)
        self.homemgrModel.refresh()

        self.awaymgrModel.setID(currentID)
        self.awaymgrModel.refresh()
        
        # go to first record of mapper
        self.hometeamMapper.toFirst()
        self.awayteamMapper.toFirst()
        self.homemgrMapper.toFirst()
        self.awaymgrMapper.toFirst()

    def refreshPhaseForms(self, currentID, phaseText):
        """Sets match ID for linking models and refreshed models and mappers.
        
        Parameters:
        currentID: matchID key
        phaseText: text associated with current index in Competition Phase combobox
        """
        self.leagueMatchModel.setID(currentID)
        self.groupMatchModel.setID(currentID)
        self.knockoutMatchModel.setID(currentID)
            
        if phaseText == "League":
            self.leagueMatchModel.refresh()
            self.leagueMatchMapper.toFirst()
        elif phaseText == "Group":
            self.groupMatchModel.refresh()
            self.groupMatchMapper.toFirst()
        elif phaseText == "Knockout":
            self.knockoutMatchModel.refresh()
            self.knockoutMatchMapper.toFirst()
        
        self.filterReferees()
        
    def addRecord(self):
        """Adds new record at end of entry list.
        
        Disables comboboxes and sets focus to Date field.
        
        """
        # save current index if valid
        row = self.mapper.currentIndex()
        if row != -1:
            if self.isDirty(row):
                if MsgPrompts.SaveDiscardOptionPrompt(self):
                    if not self.mapper.submit():
                        MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                    else:
                        self.submitForms()
                else:
                    self.mapper.revert()
                    return
        
        row = self.model.rowCount()
        query = QSqlQuery()
        query.exec_(QString("SELECT MAX(match_id) FROM tbl_matches"))
        if query.next():
            maxMatchID= query.value(0).toInt()[0]
            if not maxMatchID:
                match_id = Constants.MinMatchID
            else:
                match_id= QString()
                match_id.setNum(maxMatchID+1)                  
        self.model.insertRow(row)
        self.mapper.setCurrentIndex(row)
        
        # assign value to matchID field
        self.matchID_display.setText(match_id)
        
        # obtain Competition Phase of current record
        phaseText = self.matchPhaseSelect.currentText()
        
        # disable next/last navigation buttons
        self.nextEntry.setDisabled(True)
        self.lastEntry.setDisabled(True)
        # enable first/previous navigation buttons
        if self.model.rowCount() > 1:
            self.prevEntry.setEnabled(True)
            self.firstEntry.setEnabled(True)
            # enable Delete button if at least one record
            self.deleteEntry.setEnabled(True)

        # enable Save button
        if not self.saveEntry.isEnabled():
            self.saveEntry.setEnabled(True)
        
        # flush filters
        for widget in [self.homeCountryModel, self.homeManagerModel, self.awayCountryModel, self.awayManagerModel]:
            widget.blockSignals(True)
            widget.setFilter(QString())
            widget.blockSignals(False)    
    
        # block all dropbox signals
        for widget in self.selectWidgets:
            widget.blockSignals(True)
            
        # enable form widgets
        for widget in self.upperFormWidgets:
            widget.setEnabled(True)
        
        # disable phase-related widgets
        for widget in self.phaseWidgets:
            widget.setDisabled(True)
            
        # disable remaining form widgets
        for widget in self.lowerFormWidgets:
            widget.setDisabled(True)
            
        # disable home/away widgets
        for widget in self.homeawayWidgets:
            widget.setDisabled(True)
            
        # initialize form widgets
        for widget in self.selectWidgets:
            widget.setCurrentIndex(-1)
        
        # unblock all dropbox signals
        for widget in self.selectWidgets:
            widget.blockSignals(False)
            
        self.firstHalfLengthEdit.setText("45")
        self.secondHalfLengthEdit.setText("45")
        self.firstExtraLengthEdit.setText("0")
        self.secondExtraLengthEdit.setText("0")
        self.matchAttendanceEdit.setText("0")
        self.matchDateEdit.setDate(QDate(1856, 1, 1))
        self.matchDateEdit.setFocus()
        
        # refresh subforms
        self.refreshSubForms(match_id)    
        self.refreshPhaseForms(match_id, phaseText)

    def deleteRecord(self):
        """Deletes record from database upon user confirmation.
        
        First, check that the match record is not being referenced in any of the following tables:
            - Lineups table
            - PenShootoutOpeners linking table
        If it is not being referenced in the child tables, ask for user confirmation and upon pos-
        itive confirmation, delete records in the following order:
            (1) HomeTeams and AwayTeams linking tables
            (2) HomeManagers and AwayManagers linking tables
            (3) LeagueMatches, GroupMatches, and KnockoutMatches linking tables
            (4) WeatherKickoff, WeatherHalftime, and WeatherFulltime linking tables
            (5) Environments table
            (6) Match table
        If match record is being referenced by Lineups, alert user.
        """
        childTableList = ["tbl_lineups", "tbl_penshootoutopeners"]
        fieldName = "match_id"
        match_id = self.matchID_display.text()
        
        if not CheckTables.CountChildRecords(childTableList, fieldName, match_id):
            if QMessageBox.question(self, QString("Delete Record"), 
                                                QString("Delete current record?"), 
                                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                return
            else:
                # delete corresponding records in HomeTeams and AwayTeams 
                self.hometeamModel.delete(match_id)
                self.awayteamModel.delete(match_id)
                
                # delete corresponding records in HomeManagers and AwayManagers
                self.homemgrModel.delete(match_id)
                self.awaymgrModel.delete(match_id)
                
                # delete corresponding records in LeagueMatches, GroupMatches, and KnockoutMatches
                # (will be in one of either, but make a sweep through all three to make sure)
                self.leagueMatchModel.delete(match_id)
                self.groupMatchModel.delete(match_id)
                self.knockoutMatchModel.delete(match_id)
                
                # find enviro_id in Environments table that contains match_id
                self.deleteEnviroTables(match_id)
                
                # delete record in Match table
                row = self.mapper.currentIndex()
                self.model.removeRow(row)
                if not self.model.submitAll():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                    return
                if row + 1 >= self.model.rowCount():
                    row = self.model.rowCount() - 1
                self.mapper.setCurrentIndex(row) 
                
                # enable time boxes and refresh subforms
                currentID = self.matchID_display.text()
                phaseText = self.matchPhaseSelect.currentText()
                self.enableTimes(phaseText)
                self.refreshSubForms(currentID)
                self.refreshPhaseForms(currentID, phaseText)
                
                if not self.model.rowCount():
                    # disable Save and Delete buttons if no records in database
                    self.deleteEntry.setDisabled(True)
                    self.saveEntry.setDisabled(True)
                    
                    self.firstHalfLengthEdit.setText("45")
                    self.secondHalfLengthEdit.setText("45")
                    self.firstExtraLengthEdit.setText("0")
                    self.secondExtraLengthEdit.setText("0")
                    self.matchAttendanceEdit.setText("0")
                    self.matchDateEdit.setDate(QDate(1856, 1, 1))
                    self.matchDateEdit.setFocus()
                    self.matchID_display.setText(QString())
                        
                    # initialize form widgets
                    for widget in self.selectWidgets:
                        widget.setCurrentIndex(-1)
                        
                    # enable form widgets
                    for widget in self.upperFormWidgets:
                        widget.setDisabled(True)
                    
                    # disable phase-related widgets
                    for widget in self.phaseWidgets:
                        widget.setDisabled(True)
                        
                    # disable remaining form widgets
                    for widget in self.lowerFormWidgets:
                        widget.setDisabled(True)
                        
                    # disable home/away widgets
                    for widget in self.homeawayWidgets:
                        widget.setDisabled(True)
                        
                    # disable all navigation widgets
                    for widget in (self.prevEntry, self.firstEntry, self.nextEntry, self.lastEntry):
                        widget.setDisabled(True)
        else:
                DeletionErrorPrompt(self)
                
    def isDirty(self, row):
        """Compares current state of data entry form to current record in database, and returns a boolean.
        
        Arguments:
            row: current record in mapper and model
        
        Returns:
            TRUE: there are changes between data entry form and current record in database,
                      or new record in database
            FALSE: no changes between data entry form and current record in database
        """
        
        # date field
        dateList = (self.matchDateEdit, )
        columnList = (MatchEntryDlg.DATE, )
        for editor, column in zip(dateList, columnList):
            index = self.model.index(row, column)
            if editor.date().toString(Qt.ISODate) != self.model.data(index).toString():
                return True
                
        # line edit fields
        editorList = (self.firstHalfLengthEdit, self.secondHalfLengthEdit, 
                            self.firstExtraLengthEdit,  self.secondExtraLengthEdit, self.matchAttendanceEdit)
        columnList = (MatchEntryDlg.HALF1, MatchEntryDlg.HALF2, 
                              MatchEntryDlg.EXTRA1, MatchEntryDlg.EXTRA2, MatchEntryDlg.ATTEND)
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.text() != self.model.data(index).toString():
                return True
                
        # combobox fields
        editorList = (self.matchCompSelect, self.matchPhaseSelect, self.matchRefSelect, self.matchVenueSelect)
        columnList = (MatchEntryDlg.COMP_ID, MatchEntryDlg.PHASE_ID, MatchEntryDlg.REF_ID, MatchEntryDlg.VENUE_ID)
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.currentText() != self.model.data(index).toString():
                return True
                    
        # combobox fields that map to linking tables
        editorList = (self.hometeamSelect, self.homemgrSelect, self.awayteamSelect, self.awaymgrSelect)
        modelList = (self.hometeamModel, self.homemgrModel, self.awayteamModel, self.awaymgrModel)
        for editor, model in zip(editorList, modelList):
            index = model.index(0, 1)
            editIndex = editor.model().index(editor.currentIndex(), 0)
            if editor.model().data(editIndex).toString() != model.data(index).toString():
                return True

        return False                

    def updateConfed(self, confedList, countryList):
        """Updates current index of Confederation combobox.
        
        Ensures consistency between confederation and selected nation in Country combobox.
        
        """
        for confedSelect, countrySelect in zip(confedList, countryList):
            if confedSelect.isEnabled():
                confedSelect.blockSignals(True)
                # define underlying model
                countryModel = countrySelect.model()
                
                # look for current index on Country combobox
                # extract confed_id from underlying model
                currIdx = countrySelect.currentIndex()
                currCountry = countrySelect.currentText()
                id = countryModel.record(currIdx).value("confed_id").toString()
        
                # make query on tbl_confederations
                # extract confederation name corresponding to confederation ID
                # there will only be one confederation in query result
                query = QSqlQuery()
                query.exec_(QString("SELECT confed_name FROM tbl_confederations WHERE confed_id = %1").arg(id))
                if query.isActive():
                    query.next()
                    confedStr = query.value(0).toString()
                else:
                    confedStr = "-1"
            
                # search for confederation name in combobox, set index to current index
                confedSelect.setCurrentIndex(confedSelect.findText(confedStr, Qt.MatchExactly))
                
                # call filter Country combobox
                # update index of Country combobox to that of currCountry
                self.filterCountryBox(confedSelect, countrySelect)
                countrySelect.setCurrentIndex(countrySelect.findText(currCountry, Qt.MatchExactly))
                confedSelect.blockSignals(False)
     
    def filterCountryBox(self, confedSelect, countrySelect):
        """Enables and filters Country combobox upon selection in Confederation combobox."""        
        countrySelect.blockSignals(True)
        
        # define underlying models
        countryModel = countrySelect.model()
        confedModel = confedSelect.model()
        
        # flush filter
        countryModel.setFilter(QString())
        
        # filter tbl_countries based on confederation selection
        currIdx = confedSelect.currentIndex()
        id = confedModel.record(currIdx).value("confed_id").toString()
        countryModel.setFilter(QString("confed_id = %1").arg(id))
        
        # check current indices of confederation comboboxes
        # if same, call removeDuplicateTeam()
        if self.homeconfedSelect.currentIndex() == self.awayconfedSelect.currentIndex():
            self.removeDuplicateTeam(self.hometeamSelect, self.awayteamSelect)
            self.removeDuplicateTeam(self.awayteamSelect, self.hometeamSelect)
        
        countrySelect.blockSignals(False)
        
    def enableAndFilterReferees(self):
        """Enables and filters Referees combobox.
        
        Ensures that referee is not selected twice on same matchday in football competition.
        """
        self.enableWidget(self.matchRefSelect)
        self.filterReferees()
            
    def filterReferees(self):
        """Filters Referees combobox."""
        row = self.mapper.currentIndex()
        # current referee name
        currentReferee = self.model.record(row).value("full_name").toString()
        
        # match ID and competition phase information
        match_id = self.matchID_display.text()
        phaseText = self.matchPhaseSelect.currentText()        
        # get list of used referees for current competition phase details
        usedRefereeList = self.getUsedReferees(match_id, phaseText)       
       
        self.matchRefSelect.blockSignals(True)
        # set filter on underlying referee model
        self.refereeModel.setFilter(QString())
        filterString = "referee_id NOT IN (" + ",".join((str(n) for n in usedRefereeList)) + ")"
        self.refereeModel.setFilter(filterString)
        # set index of combobox to current referee
        self.matchRefSelect.setCurrentIndex(self.matchRefSelect.findText(currentReferee, Qt.MatchExactly))
        self.matchRefSelect.blockSignals(False)
        
    def getUsedReferees(self, match_id, phaseText):
        """Returns list of referees who have already been selected for matches that cover a specific competition matchday."""
        compName = self.matchCompSelect.currentText()        
        usedRefereeList = []
        
        refereeQuery = QSqlQuery()
        idQuery = QSqlQuery()
        if phaseText == "League":
            # get text from current index of Rounds combobox
            roundName = self.lgRoundSelect.currentText()
            # query match referees currently in database for specific league round
            refereeQuery.prepare("SELECT referee FROM league_match_list WHERE "
                "competition = ? AND round = ? AND match_id NOT IN (?)")
            refereeQuery.addBindValue(compName)
            refereeQuery.addBindValue(roundName)
            refereeQuery.addBindValue(match_id)
            refereeQuery.exec_()
            while refereeQuery.next():
                idQuery.prepare("SELECT referee_id FROM referees_list WHERE full_name = ?")
                idQuery.addBindValue(refereeQuery.value(0).toString())
                idQuery.exec_()
                while idQuery.next():
                    usedRefereeList.append(idQuery.value(0).toString())
        elif phaseText == "Group":
            # get text from current index of Group Rounds combobox
            groupRoundName = self.grpRoundSelect.currentText()
            # get text from current index of Group Name combobox
            groupName = self.groupSelect.currentText()
            # get text from current index of Group Matchdays combobox
            matchdayName = self.grpMatchdaySelect.currentText()
            # query match referees currently in database for specific group stage round, group, and matchday
            refereeQuery.prepare("SELECT referee FROM group_match_list WHERE "
                "competition = ? AND round = ? AND group_name = ? AND matchday = ? AND match_id NOT IN (?)")
            refereeQuery.addBindValue(compName)
            refereeQuery.addBindValue(groupRoundName)
            refereeQuery.addBindValue(groupName)
            refereeQuery.addBindValue(matchdayName)
            refereeQuery.addBindValue(match_id)
            refereeQuery.exec_()
            while refereeQuery.next():
                idQuery.prepare("SELECT referee_id FROM referees_list WHERE full_name = ?")
                idQuery.addBindValue(refereeQuery.value(0).toString())
                idQuery.exec_()
                while idQuery.next():
                    usedRefereeList.append(idQuery.value(0).toString())
        elif phaseText == "Knockout":
            # get text from current index of Knockout Rounds combobox
            knockoutRoundName = self.koRoundSelect.currentText()
            # get text from current index of Knockout Matchdays combobox
            matchdayName = self.koMatchdaySelect.currentText()
            # query match referees currently in database for specific knockout stage round and matchday
            refereeQuery.prepare("SELECT referee FROM knockout_match_list WHERE "
                "competition = ? AND round = ? AND game = ? AND match_id NOT IN (?)")
            refereeQuery.addBindValue(compName)
            refereeQuery.addBindValue(knockoutRoundName)
            refereeQuery.addBindValue(matchdayName)
            refereeQuery.addBindValue(match_id)
            refereeQuery.exec_()
            while refereeQuery.next():
                idQuery.prepare("SELECT referee_id FROM referees_list WHERE full_name = ?")
                idQuery.addBindValue(refereeQuery.value(0).toString())
                idQuery.exec_()
                while idQuery.next():
                    usedRefereeList.append(idQuery.value(0).toString())
                
        return usedRefereeList
        
    def removeDuplicateTeam(self, teamSelect, opposingSelect):
        """Filters selected team in opposingSelect combobox from teamSelect combobox."""
        teamSelect.blockSignals(True)
        currentModel = teamSelect.model()
        currentIndex = teamSelect.currentIndex()
        currentTeam = teamSelect.currentText()

        # get current confed_id in teamSelect
        if currentIndex == -1:
            confed_id = currentModel.record(0).value("confed_id").toString()
        else:
            confed_id = currentModel.record(currentIndex).value("confed_id").toString()
            
        # current index in selected item in opposingSelect
        opposingIndex = opposingSelect.currentIndex()
        opposing_id = opposingSelect.model().record(opposingIndex).value("country_id").toString()
        
        # set filter in underlying teamSelect model
        currentModel.setFilter(QString())        
        currentModel.setFilter(QString("confed_id = %1 AND country_id NOT IN (%2)").arg(confed_id, opposing_id))
        # set current index to item that matches team name
        teamSelect.setCurrentIndex(teamSelect.findText(currentTeam, Qt.MatchExactly))
        teamSelect.blockSignals(False)
        
    def removeDuplicateManager(self, mgrSelect, opposingSelect):
        """Filters selected manager in opposingSelect combobox from mgrSelect combobox."""
        mgrSelect.blockSignals(True)
        
        currentModel = mgrSelect.model()
        currentIndex = mgrSelect.currentIndex()
        currentMgr = mgrSelect.currentText()
        
        # flush filter of underlying mgrSelect model
        currentModel.setFilter(QString())
        
        # current index in selected item in opposingSelect
        opposingIndex = opposingSelect.currentIndex()
        opposing_id = opposingSelect.model().record(opposingIndex).value("manager_id").toString()
        
        # set filter in underlying mgrSelect model
        currentModel.setFilter(QString("manager_id NOT IN (%1)").arg(opposing_id))
        # set current index to item that matches manager name
        mgrSelect.setCurrentIndex(mgrSelect.findText(currentMgr, Qt.MatchExactly))
        mgrSelect.blockSignals(False)
        
    def deleteEnviroTables(self, match_id):
        """Deletes environmental conditions tables that reference a specific match.
        
        (1) Find the enviro_id record in Environments that is tied to a specific match (match_id).
        (2) Delete the linking tables associated with enviro_id.
        (3) Delete the enviro_id record in Environments table.
        
        """
        query = QSqlQuery()
        query.prepare("SELECT enviro_id FROM tbl_environments WHERE match_id = ?")
        query.addBindValue(QVariant(match_id))
        query.exec_()
        if query.next():
            enviro_id = query.value(0).toInt()[0]
        else:
            return
            
        list = ["tbl_weatherkickoff", "tbl_weatherhalftime", "tbl_weatherfulltime",  "tbl_environments"]
        deletionQuery = QSqlQuery()
        for table in list:
            deletionQuery.prepare(QString("DELETE FROM %1 WHERE enviro_id = ?").arg(table))
            deletionQuery.addBindValue(QVariant(enviro_id))
            deletionQuery.exec_()
                
    def updateLinkingTable(self, mapper, editor, column):
        """Updates custom linking table."""
        
        # database table associated with mapper
        # get current index of model
        linkmodel = mapper.model()
        index = linkmodel.index(linkmodel.rowCount()-1, column, QModelIndex())
        boxIndex = editor.currentIndex()
        value = editor.model().record(boxIndex).value(0)
        ok = linkmodel.setData(index, value)
        return ok
        
    def resetPhaseDetails(self, phaseText):
        """Sets phase widgets not corresponding to selected competition phase to -1."""
        if phaseText == "League":
            for widget in (self.groupSelect, self.grpRoundSelect, self.grpMatchdaySelect):
                widget.setCurrentIndex(-1)
            for widget in (self.koRoundSelect, self.koMatchdaySelect):
                widget.setCurrentIndex(-1)
        elif phaseText == "Group":
            self.lgRoundSelect.setCurrentIndex(-1)
            for widget in (self.koRoundSelect, self.koMatchdaySelect):
                widget.setCurrentIndex(-1)
        elif phaseText == "Knockout":
            self.lgRoundSelect.setCurrentIndex(-1)
            for widget in (self.groupSelect, self.grpRoundSelect, self.grpMatchdaySelect):
                widget.setCurrentIndex(-1)
                
        for widget in self.phaseWidgets:
            widget.setDisabled(True)
            
    def enableWidget(self, widget):
        """Enables widget passed in function parameter, if not already enabled."""
        widget.blockSignals(True)
        if not widget.isEnabled():
            widget.setEnabled(True)
        widget.blockSignals(False)
        
    def enablePhaseDetails(self):
        """Enables comboboxes associated with specific competition phase."""
        phaseText = self.matchPhaseSelect.currentText()
        if phaseText == "League":
            self.lgRoundSelect.setEnabled(True)
        elif phaseText == "Group":
            self.grpRoundSelect.setEnabled(True)
        elif phaseText == "Knockout":
            self.koRoundSelect.setEnabled(True)
            
    def enableTimes(self, phaseText):
        """Enables Time edit boxes according to Competition Phase.
        
        Enables 1st/2nd extra time edit boxes only if Knockout phase match.
        """
        self.firstHalfLengthEdit.setEnabled(True)
        self.secondHalfLengthEdit.setEnabled(True)
        if phaseText == "Knockout":
            self.firstExtraLengthEdit.setEnabled(True)
            self.secondExtraLengthEdit.setEnabled(True)
        
    def enableDefaults(self):
        """Enables Attendance and Time edit boxes, Home Team comboboxes and Enviroments button."""
        self.matchAttendanceEdit.setEnabled(True)
        self.enableTimes(self.matchPhaseSelect.currentText())
        self.homeconfedSelect.setEnabled(True)
        self.enviroButton.setEnabled(True)
        
    def openEnviros(self, match_id):
        """Opens Environment subdialog for a specific match from Match dialog.
        
        Saves current match record (but not subforms), instantiates EnviroEntryDlg object and opens window.
        Argument: 
        match_id -- primary key of current record in Matches table
        
        """
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
            return
            
        subdialog = EnviroEntryDlg(match_id, self)
        subdialog.exec_()
        self.mapper.setCurrentIndex(row)
        
    def openLineups(self, match_id, teamName):
        """Opens Lineups subdialog for one of the teams in a specific match from Match dialog.
        
        Saves current match record, instantiates LineupEntryDlg object and opens window.
        Arguments: 
        match_id -- primary key of current record in Matches table
        teamName -- team name corresponding to one of the two participants in 
                            current Match record
        
        This method is only allowed to be called when all of the home/away team
        and manager fields have been populated with non-NULL values.
        
        """
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
            return
            
        subdialog = LineupEntryDlg(match_id, teamName, self)
#        print "Match ID: %s" % match_id
#        print "Team Name: %s" % teamName
        subdialog.exec_()
        self.mapper.setCurrentIndex(row)
    
class EnviroEntryDlg(QDialog, ui_enviroentry.Ui_EnviroEntryDlg):
    """Implements environmental conditions data entry dialog, and accesses and writes to Environments table.
    
    This is a subdialog of the environmental conditions of the match -- kickoff time, ambient temperature, 
    weather conditions at kickoff, halftime, and fulltime.
    
    Argument:
    match_id -- primary key of current record in Matches table
    
    """

    ENVIRO_ID,  MATCH_ID,  KICKOFF,  TEMP = range(4)
    
    def __init__(self, match_id, parent=None):
        """Constructor for EnviroEntryDlg class"""
        super(EnviroEntryDlg, self).__init__(parent)
        self.setupUi(self)
#        print "Calling init() in EnviroEntryDlg"
        
        # define local parameters
        WX_COND = KICKOFF_WX = HALFTIME_WX = FULLTIME_WX = 1

        # define underlying database model (tbl_environments)
        self.model = QSqlTableModel(self)
        self.model.setTable("tbl_environments")
        self.model.setFilter(QString("match_id = %1").arg(match_id))
        self.model.select()
        
        # if no entry for given table, create one
        # assign new id to enviro_id edit box
        row = self.model.rowCount()
        if not row:
            # get highest enviro_id from entries in table
            query = QSqlQuery()
            query.exec_(QString("SELECT MAX(enviro_id) FROM tbl_environments"))
            if query.next():
                maxEnviroID = query.value(0).toInt()[0]
                if not maxEnviroID:
                    enviro_id = Constants.MinEnviroID
                else:
                    enviro_id= QString()
                    enviro_id.setNum(maxEnviroID+1)
            # insert row into model
            self.model.insertRow(row)
            # assign ID to enviroID display field
            self.enviroID_display.setText(enviro_id)
            
        # assign value to matchID display field
        self.matchID_display.setText(match_id)

        # define mapper for Environments table
        # establish ties between underlying database model and data widgets on form
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.enviroID_display, EnviroEntryDlg.ENVIRO_ID)
        self.mapper.addMapping(self.matchID_display, EnviroEntryDlg.MATCH_ID)
        self.mapper.addMapping(self.envKOTimeEdit, EnviroEntryDlg.KICKOFF)
        self.mapper.addMapping(self.envKOTempEdit, EnviroEntryDlg.TEMP)
        self.mapper.toFirst()

        # define Weather Conditions table
        weatherModel = QSqlTableModel(self)
        weatherModel.setTable("tbl_weather")
        weatherModel.setSort(WX_COND, Qt.AscendingOrder)
        weatherModel.select()

        # set up Kickoff Weather linking table 
        # set up Kickoff Weather Condition combobox with items from tbl_weather table
        self.kickoffWeatherModel = WeatherLinkingModel("tbl_weatherkickoff", self)
        self.envKOWxSelect.setModel(weatherModel)
        self.envKOWxSelect.setModelColumn(weatherModel.fieldIndex("wx_conditiondesc"))
        self.envKOWxSelect.setCurrentIndex(-1)
        
        # set up Halftime Weather linking table 
        # set up Halftime Weather Condition combobox with items from tbl_weather table
        self.halftimeWeatherModel = WeatherLinkingModel("tbl_weatherhalftime", self)
        self.envHTWxSelect.setModel(weatherModel)
        self.envHTWxSelect.setModelColumn(weatherModel.fieldIndex("wx_conditiondesc"))
        self.envHTWxSelect.setCurrentIndex(-1)
        
        # set up Fulltime Weather linking table 
        # set up Fulltime Weather Condition combobox with items from tbl_weather table
        self.fulltimeWeatherModel = WeatherLinkingModel("tbl_weatherfulltime", self)
        self.envFTWxSelect.setModel(weatherModel)
        self.envFTWxSelect.setModelColumn(weatherModel.fieldIndex("wx_conditiondesc"))
        self.envFTWxSelect.setCurrentIndex(-1)        

        # define mapper for Kickoff Weather Conditions
        self.kickoffWeatherMapper = QDataWidgetMapper(self)
        self.kickoffWeatherMapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.kickoffWeatherMapper.setModel(self.kickoffWeatherModel)
        kickoffWeatherDelegate = GenericDelegate(self)
        kickoffWeatherDelegate.insertColumnDelegate(KICKOFF_WX, WeatherComboBoxDelegate(self))
        self.kickoffWeatherMapper.setItemDelegate(kickoffWeatherDelegate)
        self.kickoffWeatherMapper.addMapping(self.envKOWxSelect, KICKOFF_WX)
        self.kickoffWeatherMapper.toFirst()
        
        # define mapper for Halftime Weather Conditions
        self.halftimeWeatherMapper = QDataWidgetMapper(self)
        self.halftimeWeatherMapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.halftimeWeatherMapper.setModel(self.halftimeWeatherModel)
        halftimeWeatherDelegate = GenericDelegate(self)
        halftimeWeatherDelegate.insertColumnDelegate(HALFTIME_WX, WeatherComboBoxDelegate(self))
        self.halftimeWeatherMapper.setItemDelegate(halftimeWeatherDelegate)
        self.halftimeWeatherMapper.addMapping(self.envHTWxSelect, HALFTIME_WX)
        self.halftimeWeatherMapper.toFirst()
        
        # define mapper for Fulltime Weather Conditions
        self.fulltimeWeatherMapper = QDataWidgetMapper(self)
        self.fulltimeWeatherMapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.fulltimeWeatherMapper.setModel(self.fulltimeWeatherModel)
        fulltimeWeatherDelegate = GenericDelegate(self)
        fulltimeWeatherDelegate.insertColumnDelegate(FULLTIME_WX, WeatherComboBoxDelegate(self))
        self.fulltimeWeatherMapper.setItemDelegate(fulltimeWeatherDelegate)
        self.fulltimeWeatherMapper.addMapping(self.envFTWxSelect, FULLTIME_WX)
        self.fulltimeWeatherMapper.toFirst()

        # configure signal/slot
        self.connect(self.closeButton, SIGNAL("clicked()"), self.accept)
        
    def accept(self):
        """Submits changes to database and closes window upon confirmation from user."""
        row = self.mapper.currentIndex()
        if self.isDirty(row):
            if MsgPrompts.SaveDiscardOptionPrompt(self):
                if not self.mapper.submit():
                    MsgPrompts.DatabaseCommitErrorPrompt(self, self.model.lastError())
                else:
                    self.updateLinkingTable(self.kickoffWeatherMapper, self.envKOWxSelect)
                    self.updateLinkingTable(self.halftimeWeatherMapper, self.envHTWxSelect)
                    self.updateLinkingTable(self.fulltimeWeatherMapper, self.envFTWxSelect)
        QDialog.accept(self)

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
        editorList = (self.envKOTimeEdit, self.envKOTempEdit)
        columnList = (EnviroEntryDlg.KICKOFF, EnviroEntryDlg.TEMP)
        for editor, column in zip(editorList, columnList):
            index = self.model.index(row, column)        
            if editor.text() != self.model.data(index).toString():
                return True
                
        # combobox fields that map to linking tables
        editorList = (self.envKOWxSelect, self.envHTWxSelect, self.envFTWxSelect)   
        modelList = (self.kickoffWeatherModel, self.halftimeWeatherModel, self.fulltimeWeatherModel)
        for editor, model in zip(editorList, modelList):
            index = model.index(0, 1)
            if editor.currentText() != model.data(index).toString():
                return True

        return False                

    def updateLinkingTable(self, mapper, editor):
        """Updates current record or inserts new record in custom linking table.
        
        Arguments:
        mapper -- mapper object associated with data widget and data model
        editor -- data widget object
        """
#        print "Calling updateLinkingTable()"
        # database table associated with mapper
        # get current index of model
        linkmodel = mapper.model()
        index = linkmodel.index(linkmodel.rowCount()-1, 0)
        boxIndex = editor.currentIndex()
        value = editor.model().record(boxIndex).value(0)
#        print value.toString()
        ok = linkmodel.setData(index, value)
#        print ok
        return ok
