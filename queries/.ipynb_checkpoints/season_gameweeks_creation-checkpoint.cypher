UNWIND $game_weeks AS gw
    MERGE (s:Season {name: gw.season_name})
    MERGE (game_week:GameWeek {gw_number: toString(gw.gw_number), season: gw.season_name})
    MERGE (game_week)-[:IS_A_GW]->(s)
