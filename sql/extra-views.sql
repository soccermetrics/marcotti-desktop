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