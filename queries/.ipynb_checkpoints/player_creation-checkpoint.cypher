/*
This query is used for creating player nodes. As a player node isn't unique to a season, their relationship to a squad is, we use merge insteaed of create as a player node may already exist if they play in multiple seasons.
*/

UNWIND $players AS player
MERGE (p:Player {name: player.Name})
SET p.position = player.position,
    p.footed = player.footed,
    p.height = toFloat(player.height),
    p.weight = toFloat(player.weight),
    p.dob = date(player.dob),
    p.birth_place = player.birth_place,
    p.national_team = player.national_team,
    p.wages = toFloat(player.wages),
    p.img = player.img
MERGE (squad: Squad {team: player.Team, season: $season_name})
MERGE (p)-[:IS_IN_SQUAD]->(squad)