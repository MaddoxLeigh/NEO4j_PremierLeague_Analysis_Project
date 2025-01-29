    UNWIND $goalkeeper_stats AS gs
    MATCH (goalie:Player {name: gs.goalie_name})
    MATCH (squad:Squad {teams: gs.team_name, season: $season_name})
    MATCH (goalie)-[:IS_IN_SQUAD]->(squad)
    MATCH (match:Match {id: gs.match_id})
    MERGE (goalie)-[h:PLAYS_IN]->(match)
    SET h.minutes_played = toInteger(gs.minutes_played),
        h.sota = toInteger(gs.sota),
        h.goals_allowed = toInteger(gs.goals_allowed),
        h.saves = toInteger(gs.saves),
        h.save_percentage = toFloat(gs.save_percentage),
        h.psxg = toFloat(gs.psxg),
        h.passes_completed = toInteger(gs.passes_completed),
        h.passes_attempted = toInteger(gs.passes_attempted),
        h.pass_accuracy = toFloat(gs.pass_accuracy),
        h.gk_passes_attempted = toInteger(gs.gk_passes_attempted),
        h.throws = toInteger(gs.throws),
        h.launch_percentage = toFloat(gs.launch_percentage),
        h.launch_average_length = toFloat(gs.launch_average_length),
        h.goal_kicks_attempted = toInteger(gs.goal_kicks_attempted),
        h.goal_kick_launch_percentage = toFloat(gs.goal_kick_launch_percentage),
        h.goal_kick_average_length = toFloat(gs.goal_kick_average_length),
        h.crosses_opportunities = toInteger(gs.crosses_opportunities),
        h.crosses_stops = toInteger(gs.crosses_stops),
        h.crosses_stop_percentage = toFloat(gs.crosses_stop_percentage),
        h.opa = toInteger(gs.opa),
        h.opa_average_distance = toFloat(gs.opa_average_distance);
