UNWIND $players AS player
    MERGE (p:Player {name: player.Name})
    SET p.position = player.position,
        p.footed = player.footed,
        p.height = toFloat(player.height),
        p.weight = toFloat(player.weight),
        p.dob = date(player.dob),
        p.birth_place = player.birth_place,
        p.national_team = player.national_team,
        p.club = player.club,
        p.wages = toFloat(player.wages),
        p.contract_expiry = player.contract_expiry,
        p.img = player.img
    MERGE (team:Team {name: player.Team})
    MERGE (squad: Squad {name: player.Team + " " + $season_name})
    MERGE (team)-[:HAS_SQUAD]->(squad)
    MERGE (p)-[:IS_IN_SQUAD]->(squad)
