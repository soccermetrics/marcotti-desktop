-- fmrd-views.sql: View schema for Football Match Result Database
-- Version: 1.0.0
-- Author: Howard Hamilton
-- Date: 2010-08-05

-- -------------------------------------------------
-- CountriesList View
-- -------------------------------------------------

CREATE VIEW countries_list AS
	SELECT country_id,
				 cty_name AS country,
				 confed_name AS confed
	FROM tbl_countries, tbl_confederations
	WHERE tbl_countries.confed_id = tbl_confederations.confed_id;

-- -------------------------------------------------
-- PositionsList View
-- -------------------------------------------------

CREATE VIEW positions_list AS
	SELECT position_id,
				 CASE WHEN tbl_positions.posflank_id IN 
				 					 (SELECT posflank_id FROM tbl_flanknames 
				 					  WHERE posflank_name IS NULL) 
				 			THEN posfield_name
				 		  ELSE posflank_name || ' ' || posfield_name
				 END AS position_name
	FROM tbl_positions, tbl_fieldnames, tbl_flanknames
	WHERE tbl_positions.posflank_id = tbl_flanknames.posflank_id
		AND tbl_positions.posfield_id = tbl_fieldnames.posfield_id;		

-- -------------------------------------------------
-- PlayersList View
-- -------------------------------------------------

CREATE VIEW players_list AS
	SELECT player_id,
				 CASE WHEN plyr_nickname IS NOT NULL THEN plyr_nickname
				 		  ELSE plyr_firstname || ' ' || plyr_lastname
				 END AS full_name,
				 CASE WHEN plyr_nickname IS NOT NULL THEN plyr_nickname
				 		  ELSE plyr_lastname
				 END AS sort_name,				 
				 position_name,
				 plyr_birthdate AS birthdate,
				 country
	FROM tbl_players, countries_list, positions_list
	WHERE tbl_players.country_id = countries_list.country_id
	  AND tbl_players.plyr_defposid = positions_list.position_id;		

-- -------------------------------------------------
-- ManagersList View
-- -------------------------------------------------

CREATE VIEW managers_list AS
	SELECT manager_id,
				 CASE WHEN mgr_nickname IS NOT NULL THEN mgr_nickname
				 		  ELSE mgr_firstname || ' ' || mgr_lastname
				 END AS full_name,
				 CASE WHEN mgr_nickname IS NOT NULL THEN mgr_nickname
				 		  ELSE mgr_lastname
				 END AS sort_name,				 				 
				 mgr_birthdate AS birthdate,
				 country
	FROM tbl_managers, countries_list
	WHERE tbl_managers.country_id = countries_list.country_id;		

-- -------------------------------------------------
-- RefereesList View
-- -------------------------------------------------

CREATE VIEW referees_list AS
	SELECT referee_id,
				 ref_firstname || ' ' || ref_lastname AS full_name,
				 ref_lastname AS sort_name,
				 ref_birthdate AS birthdate,
				 country
	FROM tbl_referees, countries_list
	WHERE tbl_referees.country_id = countries_list.country_id;		

-- -------------------------------------------------
-- HomeTeamList View
-- -------------------------------------------------

CREATE VIEW hometeam_list AS
	SELECT tbl_matches.match_id,
				 tm_name AS team
	FROM tbl_matches, tbl_hometeams, tbl_teams
	WHERE tbl_matches.match_id = tbl_hometeams.match_id
		AND tbl_hometeams.team_id = tbl_teams.team_id;

-- -------------------------------------------------
-- AwayTeamList View
-- -------------------------------------------------

CREATE VIEW awayteam_list AS
	SELECT tbl_matches.match_id,
				 tm_name AS team
	FROM tbl_matches, tbl_awayteams, tbl_teams
	WHERE tbl_matches.match_id = tbl_awayteams.match_id
		AND tbl_awayteams.team_id = tbl_teams.team_id;

-- -------------------------------------------------
-- VenueList View
-- -------------------------------------------------

CREATE VIEW venue_list AS
	SELECT venue_id,
				 ven_name AS venue,
				 ven_city AS city,
				 country,
				 ven_altitude AS altitude,
				 ven_latitude AS latitude,
				 ven_longitude AS longitude
	FROM tbl_venues, countries_list
	WHERE countries_list.country_id = tbl_venues.country_id;				

-- -------------------------------------------------
-- MatchList View
-- -------------------------------------------------

CREATE VIEW match_list AS
	SELECT tbl_matches.match_id,
				 tbl_competitions.competition_id,
				 tbl_rounds.round_id,
				 comp_name AS competition,
				 round_desc AS matchday,
				 hometeam_list.team || ' vs ' || awayteam_list.team AS matchup,
				 venue,
				 full_name AS referee
	FROM tbl_matches, tbl_competitions, tbl_rounds, hometeam_list, awayteam_list, venue_list, referees_list
	WHERE hometeam_list.match_id = tbl_matches.match_id
		AND awayteam_list.match_id = tbl_matches.match_id
		AND tbl_competitions.competition_id = tbl_matches.competition_id
		AND tbl_rounds.round_id = tbl_matches.round_id
		AND venue_list.venue_id = tbl_matches.venue_id
		AND referees_list.referee_id = tbl_matches.referee_id;
		
-- -------------------------------------------------
-- Weather Conditions Views
-- -------------------------------------------------
		
CREATE VIEW kowx_list AS
	SELECT enviro_id,
				 wx_conditiondesc AS cond
	FROM tbl_weatherkickoff, tbl_weather
	WHERE tbl_weather.weather_id = tbl_weatherkickoff.weather_id;
	
CREATE VIEW htwx_list AS
	SELECT enviro_id,
				 wx_conditiondesc AS cond
	FROM tbl_weatherhalftime, tbl_weather
	WHERE tbl_weather.weather_id = tbl_weatherhalftime.weather_id;
	 						
CREATE VIEW ftwx_list AS
	SELECT enviro_id,
				 wx_conditiondesc AS cond
	FROM tbl_weatherfulltime, tbl_weather
	WHERE tbl_weather.weather_id = tbl_weatherfulltime.weather_id;
		
-- -------------------------------------------------
-- EnviroList View
-- -------------------------------------------------

CREATE VIEW enviro_list AS
	SELECT tbl_environments.enviro_id,
				 matchup,
				 env_kickofftime AS kickoff_time,
				 env_temperature AS temperature,
				 kowx_list.cond	 AS kickoff_wx,
				 htwx_list.cond  AS halftime_wx,
				 ftwx_list.cond  AS fulltime_wx
	FROM tbl_environments, match_list, kowx_list, htwx_list, ftwx_list
	WHERE tbl_environments.match_id = match_list.match_id
	  AND tbl_environments.enviro_id = kowx_list.enviro_id
	  AND tbl_environments.enviro_id = htwx_list.enviro_id
	  AND tbl_environments.enviro_id = ftwx_list.enviro_id;				 						 
				 
-- -------------------------------------------------
-- LineupList View
-- -------------------------------------------------

CREATE VIEW lineup_list AS
	SELECT lineup_id,
				 matchup,
				 tm_name AS team,
				 full_name AS player,
				 positions_list.position_name,
				 lp_starting AS starter,
				 lp_captain AS captain,
				 sort_name				 
	FROM tbl_teams, players_list, positions_list, match_list, tbl_lineups
	WHERE tbl_lineups.team_id = tbl_teams.team_id
	  AND tbl_lineups.match_id = match_list.match_id 
	  AND players_list.player_id = tbl_lineups.player_id
	  AND tbl_lineups.position_id = positions_list.position_id;
	  
-- -------------------------------------------------
-- GoalsList View
-- -------------------------------------------------

CREATE VIEW goals_list AS
	SELECT goal_id,
				 match_list.matchup,
				 tm_name AS team,
				 player AS scorer,
				 gts_desc AS strike,
				 gte_desc AS play,
				 CASE WHEN gls_stime = 0 THEN gls_time || ''''
				 			ELSE gls_time || '+' || gls_stime || ''''
				 END AS time
	FROM tbl_teams, match_list, lineup_list, tbl_goalstrikes, tbl_goalevents, tbl_goals
	WHERE match_list.match_id IN (SELECT match_id FROM tbl_lineups)
		AND tbl_goals.lineup_id = lineup_list.lineup_id
		AND tbl_goals.team_id = tbl_teams.team_id
		AND tbl_goals.gtstype_id = tbl_goalstrikes.gtstype_id
		AND tbl_goals.gtetype_id = tbl_goalevents.gtetype_id;

-- -------------------------------------------------
-- OwnGoalsList View
-- -------------------------------------------------

CREATE VIEW owngoals_list AS
	SELECT goal_id,
				 match_list.matchup,
				 tm_name AS team,
				 player AS scorer,
				 gts_desc AS strike,
				 gte_desc AS play,
				 CASE WHEN gls_stime = 0 THEN gls_time || ''''
				 			ELSE gls_time || '+' || gls_stime || ''''
				 END AS time
	FROM tbl_teams, match_list, lineup_list, tbl_goalstrikes, tbl_goalevents, tbl_goals
	WHERE match_list.match_id IN (SELECT match_id FROM tbl_lineups)
	  AND tbl_goals.lineup_id = lineup_list.lineup_id
		AND tbl_goals.gtstype_id = tbl_goalstrikes.gtstype_id
		AND tbl_goals.gtetype_id = tbl_goalevents.gtetype_id	  
	  AND tbl_goals.team_id NOT IN (SELECT team_id FROM tbl_lineups
	  														  WHERE tbl_lineups.lineup_id = lineup_list.lineup_id);

-- -------------------------------------------------
-- PenaltiesList View
-- -------------------------------------------------

CREATE VIEW penalties_list AS
	SELECT penalty_id,
				 matchup,
				 player AS taker,
				 foul_desc AS foul,
				 po_desc AS outcome,
				 CASE WHEN pen_stime = 0 THEN pen_time || ''''
				 			ELSE pen_time || '+' || pen_stime || ''''
				 END AS time
	FROM tbl_penalties, lineup_list, tbl_fouls, tbl_penoutcomes
	WHERE tbl_penalties.foul_id = tbl_fouls.foul_id
	  AND tbl_penalties.penoutcome_id = tbl_penoutcomes.penoutcome_id
	  AND tbl_penalties.lineup_id = lineup_list.lineup_id;				 

-- -------------------------------------------------
-- CautionsList View
-- -------------------------------------------------

CREATE VIEW cautions_list AS
	SELECT offense_id,
				 matchup,
				 player,
				 foul_desc AS foul,
				 CASE WHEN ofns_stime = 0 THEN ofns_time || ''''
				 			ELSE ofns_time || '+' || ofns_stime || ''''
				 END AS time
	FROM tbl_offenses, lineup_list, tbl_fouls
	WHERE tbl_offenses.lineup_id = lineup_list.lineup_id
		AND tbl_offenses.foul_id = tbl_fouls.foul_id
		AND tbl_offenses.card_id IN (SELECT card_id FROM tbl_cards
				WHERE card_type = 'Yellow');

-- -------------------------------------------------
-- ExpulsionsList View
-- -------------------------------------------------

CREATE VIEW expulsions_list AS
	SELECT offense_id,
				 matchup,
				 player,
				 foul_desc AS foul,
				 CASE WHEN ofns_stime = 0 THEN ofns_time || ''''
				 			ELSE ofns_time || '+' || ofns_stime || ''''
				 END AS time
	FROM tbl_offenses, lineup_list, tbl_fouls
	WHERE tbl_offenses.lineup_id = lineup_list.lineup_id
		AND tbl_offenses.foul_id = tbl_fouls.foul_id
		AND tbl_offenses.card_id IN (SELECT card_id FROM tbl_cards
				WHERE card_type = 'Yellow/Red' OR card_type = 'Red');

-- -------------------------------------------------
-- SubstitutionsList View
-- -------------------------------------------------

CREATE VIEW insub_list AS
	SELECT subs_id,
				 player
	FROM tbl_insubstitutions, lineup_list
	WHERE tbl_insubstitutions.lineup_id = lineup_list.lineup_id;
	
CREATE VIEW outsub_list AS
	SELECT subs_id,
				 player
	FROM tbl_outsubstitutions, lineup_list
	WHERE tbl_outsubstitutions.lineup_id = lineup_list.lineup_id;

CREATE VIEW subs_list AS
	SELECT tbl_substitutions.subs_id, 
			 a1.matchup, 
			 a1.team, 
			 a1.player AS in_player, 
			 a2.player AS out_player, 
			 case when subs_stime = 0 then subs_time || '''' 
			 			else subs_time || '+' || subs_stime || '''' 
			 end AS time 
	FROM lineup_list a1, lineup_list a2, tbl_substitutions, tbl_insubstitutions, tbl_outsubstitutions 
	WHERE a1.player in (SELECT player FROM lineup_list 
											WHERE lineup_list.lineup_id = tbl_insubstitutions.lineup_id) 
		AND a2.player in (SELECT player FROM lineup_list 
											WHERE lineup_list.lineup_id = tbl_outsubstitutions.lineup_id) 
		AND (tbl_substitutions.subs_id = tbl_insubstitutions.subs_id 
				 AND tbl_substitutions.subs_id = tbl_outsubstitutions.subs_id);
	
CREATE VIEW switchpos_list AS
	SELECT switch_id,
				 matchup,
				 team,
				 player,
				 lineup_list.position_name AS old_position,
				 positions_list.position_name AS new_position,
				 CASE WHEN switch_stime = 0 THEN switch_time || ''''
				 			ELSE switch_time || '+' || switch_stime || ''''
				 END AS time
	FROM tbl_switchpositions, lineup_list, positions_list
	WHERE tbl_switchpositions.lineup_id = lineup_list.lineup_id
		AND tbl_switchpositions.switchposition_id = positions_list.position_id;