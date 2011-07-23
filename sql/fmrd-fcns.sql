-- fmrd-fcns.sql: Stored procedures in PL/pgSQL for Football Match Result Database
-- Version: 1.0.0
-- Author: Howard Hamilton
-- Date: 2010-08-09

CREATE LANGUAGE plpgsql

-- Return number of goals scored by team in match
CREATE FUNCTION MatchGoals(team integer, match integer) RETURNS integer AS $$
DECLARE
	num_goals DEFAULT 0;
BEGIN
-- Sum of:
-- 		number of open-play goals
--		number of own goals 
-- 		number of penalties
END;
$$ LANGUAGE plpgsql;


-- Return the teamIDs of match participants
CREATE FUNCTION MatchTeams(match integer) RETURNS integer AS $$
DECLARE
BEGIN
END;
$$ LANGUAGE plpgsql;