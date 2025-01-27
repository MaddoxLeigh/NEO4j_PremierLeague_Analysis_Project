UNWIND $matches AS match_data
    CREATE (match:Match {id: match_data.Match_ID})
    SET match.date = date(match_data.Date),
        match.time = time(match_data.Time),
        match.home_score = toInteger(match_data.Home_Score),
        match.away_score = toInteger(match_data.Away_Score),
        match.home_expected = toFloat(match_data.Home_Expected),
        match.away_expected = toFloat(match_data.Away_Expected)
    MERGE (venue:Venue {name: match_data.Venue})
    MERGE (match)-[:PLAYED_AT]->(venue)
    WITH match, match_data
    MATCH (home_team:Squad {name: match_data.Home + " " + $season_name})
    MATCH (away_team:Squad {name: match_data.Away + " " + $season_name})
    MATCH (game_week:GameWeek {gw_number: match_data.GW, season: $season_name})
    MERGE (match)-[:HOME_TEAM]->(home_team)
    MERGE (match)-[:AWAY_TEAM]->(away_team)
    MERGE (match)-[:IS_OF_GW]->(game_week)
    FOREACH (_ IN CASE WHEN match_data.Match Report THEN [1] ELSE [] END |
        SET match.home_score = toInteger(match_data.Home_Score),
            match.away_score = toInteger(match_data.Away_Score)
        FOREACH (_ IN CASE WHEN match_data.Referee IS NOT NULL THEN [1] ELSE [] END |
            MERGE (referee:Referee {name: match_data.Referee})
            MERGE (match)-[:HAS_REFEREE]->(referee)
        )
        FOREACH (_ IN CASE WHEN match_data.home_expected IS NOT NULL THEN [1] ELSE [] END |
            SET match.home_expected = toFloat(match_data.Home_Expected),
                match.away_expected = toFloat(match_data.Away_Expected)
        )
    )
