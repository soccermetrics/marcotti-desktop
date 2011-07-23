-- fmrd.sql: Football Match Result Database schema
-- Version 1.0.0
-- Developed by: Howard Hamilton (2010-07-24)

SET DATESTYLE TO 'ISO';

-- -------------------------------------------------
-- Personnel Tables
-- -------------------------------------------------

-- Confederation table
CREATE SEQUENCE conseq increment 1 minvalue 10 maxvalue 99 start 10;
CREATE TABLE tbl_confederations (
	confed_id		integer PRIMARY KEY DEFAULT nextval('conseq'),
	confed_name	varchar(40) NOT NULL
	) WITH OIDS;

-- Country table
CREATE SEQUENCE ctryseq increment 1 minvalue 100 maxvalue 999 start 100;
CREATE TABLE tbl_countries (
	country_id	integer PRIMARY KEY DEFAULT nextval('ctryseq'),
	confed_id		integer REFERENCES tbl_confederations,
	cty_name		varchar(60) NOT NULL
	) WITH OIDS;

-- Field position table
CREATE SEQUENCE fieldseq increment 1 minvalue 1 maxvalue 9 start 1;
CREATE TABLE tbl_fieldnames (
	posfield_id			integer PRIMARY KEY DEFAULT nextval('fieldseq'),
	posfield_name		varchar(15) NOT NULL
	) WITH OIDS;

-- Flank name table
CREATE SEQUENCE flankseq increment 1 minvalue 1 maxvalue 9 start 1;
CREATE TABLE tbl_flanknames (
	posflank_id			integer PRIMARY KEY DEFAULT nextval('flankseq'),
	posflank_name		varchar(8) NULL
	) WITH OIDS;
	
-- Position table
CREATE SEQUENCE posseq increment 1 minvalue 10 maxvalue 99 start 10;
CREATE TABLE tbl_positions (
	position_id		integer PRIMARY KEY DEFAULT nextval('posseq'),
	posfield_id		integer REFERENCES tbl_fieldnames,
	posflank_id		integer REFERENCES tbl_flanknames
	) WITH OIDS;

-- Player table
CREATE SEQUENCE plyrseq increment 1 minvalue 100000 maxvalue 999999 start 100000;
CREATE TABLE tbl_players (
	player_id				integer PRIMARY KEY DEFAULT nextval('plyrseq'),
	country_id			integer REFERENCES tbl_countries,
	plyr_birthdate  date NOT NULL,
	plyr_firstname	varchar(20) NOT NULL,
	plyr_lastname		varchar(30) NOT NULL,
	plyr_nickname		varchar(30) NULL,
	plyr_defposid		integer REFERENCES tbl_positions
	) WITH OIDS;

-- Manager table
CREATE SEQUENCE mgrseq increment 1 minvalue 1000 maxvalue 9999 start 1000;
CREATE TABLE tbl_managers (
	manager_id			integer PRIMARY KEY DEFAULT nextval('mgrseq'),
	country_id			integer REFERENCES tbl_countries,
	mgr_birthdate	  date NOT NULL,
	mgr_firstname		varchar(20) NOT NULL,
	mgr_lastname		varchar(30) NOT NULL,
	mgr_nickname		varchar(30) NULL
	) WITH OIDS;

-- Referee table
CREATE SEQUENCE refseq increment 1 minvalue 1000 maxvalue 9999 start 1000;
CREATE TABLE tbl_referees (
	referee_id			integer PRIMARY KEY DEFAULT nextval('refseq'),
	country_id			integer REFERENCES tbl_countries,
	ref_birthdate		date NOT NULL,
	ref_firstname		varchar(20) NOT NULL,
	ref_lastname		varchar(30) NOT NULL
	) WITH OIDS;

-- -------------------------------------------------
-- Match Overview Tables
-- -------------------------------------------------

-- Competitions table
CREATE SEQUENCE compseq increment 1 minvalue 100 maxvalue 999 start 100;
CREATE TABLE tbl_competitions (
	competition_id	integer PRIMARY KEY DEFAULT nextval('compseq'),
	comp_name				varchar(100) NOT NULL
	) WITH OIDS;
	
-- Rounds table	
CREATE SEQUENCE roundseq increment 1 minvalue 10 maxvalue 99 start 10;
CREATE TABLE tbl_rounds (
	round_id		integer PRIMARY KEY DEFAULT nextval('roundseq'),
	round_desc 	varchar(20) NOT NULL
	) WITH OIDS;

-- Teams table	
CREATE SEQUENCE teamseq increment 1 minvalue 10000 maxvalue 99999 start 10000;
CREATE TABLE tbl_teams (
	team_id 	integer PRIMARY KEY DEFAULT nextval('teamseq'),
	tm_name		varchar(50) NOT NULL
	) WITH OIDS;		
	
-- Venues table
CREATE SEQUENCE venueseq increment 1 minvalue 1000 maxvalue 9999 start 1000;
CREATE TABLE tbl_venues (
	venue_id				integer PRIMARY KEY DEFAULT nextval('venueseq'),
	team_id					integer REFERENCES tbl_teams,
	country_id			integer REFERENCES tbl_countries,
	ven_city				varchar(40) NOT NULL,
	ven_name				varchar(40) NOT NULL,
	ven_altitude		numeric(4,0) CHECK (ven_altitude >= -200
																	AND ven_altitude <= 4500),
	ven_latitude		numeric(8,6) CHECK (ven_latitude >= -90.000000
																	AND ven_latitude <=  90.000000),
	ven_longitude		numeric(9,6) CHECK (ven_longitude >= -180.000000
																	AND ven_longitude <=  180.000000)
	) WITH OIDS;
		
-- Match table
CREATE SEQUENCE matchseq increment 1 minvalue 1000000 maxvalue 9999999 start 1000000;
CREATE TABLE tbl_matches (
	match_id							integer PRIMARY KEY DEFAULT nextval('matchseq'),
	match_date						date,
	match_firsthalftime	 	integer DEFAULT 45 CHECK (match_firsthalftime > 0),
	match_secondhalftime 	integer DEFAULT 45 CHECK (match_secondhalftime >= 0),
	competition_id				integer REFERENCES tbl_competitions,
	round_id							integer REFERENCES tbl_rounds,
	venue_id							integer REFERENCES tbl_venues,
	referee_id						integer REFERENCES tbl_referees
	) WITH OIDS;
	
-- Lineup table
CREATE SEQUENCE lineupseq increment 1 minvalue 1000000 maxvalue 9999999 start 1000000;
CREATE TABLE tbl_lineups (
	lineup_id				integer PRIMARY KEY DEFAULT nextval('lineupseq'),
	match_id				integer REFERENCES tbl_matches,
	team_id					integer REFERENCES tbl_teams,
	player_id				integer REFERENCES tbl_players,
	position_id			integer REFERENCES tbl_positions,
	lp_starting			boolean DEFAULT FALSE,
	lp_captain			boolean DEFAULT FALSE
	) WITH OIDS;
		
-- ---------------------------------------
-- Linking tables	to Match Overview tables
-- ---------------------------------------

-- Home/away teams
CREATE TABLE tbl_hometeams (
	match_id	integer REFERENCES tbl_matches,
	team_id		integer	REFERENCES tbl_teams,
	PRIMARY KEY (match_id, team_id)
	) WITH OIDS;
	
CREATE TABLE tbl_awayteams (
	match_id	integer REFERENCES tbl_matches,
	team_id		integer	REFERENCES tbl_teams,
	PRIMARY KEY (match_id, team_id)
	) WITH OIDS;	

-- Home/away managers	
CREATE TABLE tbl_homemanagers (
	match_id		integer REFERENCES tbl_matches,
	manager_id	integer	REFERENCES tbl_managers,
	PRIMARY KEY (match_id, manager_id)
	) WITH OIDS;
	
CREATE TABLE tbl_awaymanagers (
	match_id		integer REFERENCES tbl_matches,
	manager_id	integer	REFERENCES tbl_managers,
	PRIMARY KEY (match_id, manager_id)
	) WITH OIDS;	
	
-- -------------------------------------------------
-- Environmental Condition Tables
-- -------------------------------------------------

-- Environment main table
CREATE SEQUENCE enviroseq increment 1 minvalue 1000000 maxvalue 9999999 start 1000000;
CREATE TABLE tbl_environments (
	enviro_id					integer PRIMARY KEY DEFAULT nextval('enviroseq'),
	match_id					integer REFERENCES tbl_matches,
	env_kickofftime		time,
	env_temperature 	numeric(4,2) CHECK (env_temperature >= -15.0 
																		AND env_temperature <= 45.0)
	) WITH OIDS;

-- Weather conditions table
CREATE SEQUENCE wxseq increment 1 minvalue 10 maxvalue 99 start 10;
CREATE TABLE tbl_weather (
	weather_id				integer PRIMARY KEY DEFAULT nextval('wxseq'),
	wx_conditiondesc	varchar(40) NOT NULL
	) WITH OIDS;

-- ------------------------------------------	
-- Linking tables	to Weather Condition tables
-- ------------------------------------------

-- Kickoff weather condition table
CREATE TABLE tbl_weatherkickoff (
	enviro_id			integer REFERENCES tbl_environments,
	weather_id		integer REFERENCES tbl_weather,
	PRIMARY KEY (enviro_id, weather_id)
	) WITH OIDS;

-- Halftime weather condition table
CREATE TABLE tbl_weatherhalftime (
	enviro_id			integer REFERENCES tbl_environments,
	weather_id		integer REFERENCES tbl_weather,
	PRIMARY KEY (enviro_id, weather_id)
	) WITH OIDS;

-- Fulltime weather condition table
CREATE TABLE tbl_weatherfulltime (
	enviro_id			integer REFERENCES tbl_environments,
	weather_id		integer REFERENCES tbl_weather,
	PRIMARY KEY (enviro_id, weather_id)
	) WITH OIDS;

-- -------------------------------------------------
-- Match Event Tables
-- -------------------------------------------------

-- Goal strikes table
CREATE SEQUENCE gstkseq increment 1 minvalue 1 maxvalue 9 start 1;
CREATE TABLE tbl_goalstrikes (
	gtstype_id		integer PRIMARY KEY DEFAULT nextval('gstkseq'),
	gts_desc			varchar(15) NOT NULL
	) WITH OIDS;
	
-- Goal events table
CREATE SEQUENCE gevtseq increment 1 minvalue 10 maxvalue 99 start 10;
CREATE TABLE tbl_goalevents (
	gtetype_id		integer PRIMARY KEY DEFAULT nextval('gevtseq'),
	gte_desc			varchar(30) NOT NULL
	) WITH OIDS;

-- Goals table	
CREATE SEQUENCE goalseq increment 1 minvalue 100000 maxvalue 999999 start 100000;
CREATE TABLE tbl_goals (
	goal_id				integer PRIMARY KEY DEFAULT nextval('goalseq'),
	team_id				integer REFERENCES tbl_teams,
	lineup_id			integer REFERENCES tbl_lineups,
	gtstype_id		integer REFERENCES tbl_goalstrikes,
	gtetype_id		integer REFERENCES tbl_goalevents,
	gls_time			integer NOT NULL CHECK (gls_time > 0 AND gls_time <= 90),
	gls_stime			integer DEFAULT 0 CHECK (gls_stime >= 0 AND gls_stime <= 15)
	) WITH OIDS;
	
-- Cards table
CREATE SEQUENCE cardseq increment 1 minvalue 1 maxvalue 9 start 1;
CREATE TABLE tbl_cards (
	card_id			integer PRIMARY KEY DEFAULT nextval('cardseq'),
	card_type		varchar(12) NOT NULL
	) WITH OIDS;
	
-- Fouls table
CREATE SEQUENCE foulseq increment 1 minvalue 10 maxvalue 99 start 10;
CREATE TABLE tbl_fouls (
	foul_id			integer PRIMARY KEY DEFAULT nextval('foulseq'),
	foul_desc 	varchar(40) NOT NULL
	) WITH OIDS;

-- Offenses table
CREATE SEQUENCE offseq increment 1 minvalue 100000 maxvalue 999999 start 100000;
CREATE TABLE tbl_offenses (
	offense_id		integer PRIMARY KEY DEFAULT nextval('offseq'),
	lineup_id			integer REFERENCES tbl_lineups,
	foul_id				integer REFERENCES tbl_fouls,
	card_id				integer REFERENCES tbl_cards,
	ofns_time			integer NOT NULL CHECK (ofns_time > 0 AND ofns_time <= 90),
	ofns_stime		integer DEFAULT 0 CHECK (ofns_stime >= 0 AND ofns_stime <= 15)
	) WITH OIDS;

-- Penalty Outcomes table
CREATE SEQUENCE poseq increment 1 minvalue 1 maxvalue 9 start 1;
CREATE TABLE tbl_penoutcomes (
	penoutcome_id		integer PRIMARY KEY DEFAULT nextval('poseq'),
	po_desc					varchar(15) NOT NULL
	) WITH OIDS;

-- Penalties table
CREATE SEQUENCE penseq increment 1 minvalue 10000 maxvalue 99999 start 10000;
CREATE TABLE tbl_penalties (
	penalty_id		integer PRIMARY KEY DEFAULT nextval('penseq'),
	lineup_id			integer REFERENCES tbl_lineups,
	foul_id				integer REFERENCES tbl_fouls,
	penoutcome_id	integer REFERENCES tbl_penoutcomes,
	pen_time			integer NOT NULL CHECK (pen_time > 0 AND pen_time <= 90),
	pen_stime			integer DEFAULT 0 CHECK (pen_stime >= 0 AND pen_stime <= 15)
	) WITH OIDS;
	
-- Substitutions table
CREATE SEQUENCE subsseq increment 1 minvalue 100000 maxvalue 999999 start 100000;
CREATE TABLE tbl_substitutions (
	subs_id				integer PRIMARY KEY DEFAULT nextval('subsseq'),
	subs_time			integer NOT NULL CHECK (subs_time > 0 AND subs_time <= 90),
	subs_stime		integer DEFAULT 0 CHECK (subs_stime >= 0 AND subs_stime <= 15)
	) WITH OIDS;

-- In Substitutions table
CREATE TABLE tbl_insubstitutions (
	subs_id			integer REFERENCES tbl_substitutions,
	lineup_id		integer	REFERENCES tbl_lineups
	) WITH OIDS;

-- Out Substitutions table
CREATE TABLE tbl_outsubstitutions (
	subs_id			integer REFERENCES tbl_substitutions,
	lineup_id		integer	REFERENCES tbl_lineups
	) WITH OIDS;

-- Switch Positions table
CREATE SEQUENCE switchseq increment 1 minvalue 100000 maxvalue 999999 start 100000;
CREATE TABLE tbl_switchpositions (
	switch_id						integer PRIMARY KEY DEFAULT nextval('switchseq'),
	lineup_id						integer REFERENCES tbl_lineups,
	switchposition_id	  integer REFERENCES tbl_positions,
	switch_time					integer NOT NULL CHECK (switch_time > 0 AND switch_time < 90),
	switch_stime				integer DEFAULT 0 CHECK (switch_stime >= 0 AND switch_stime <= 15)
	) WITH OIDS;
