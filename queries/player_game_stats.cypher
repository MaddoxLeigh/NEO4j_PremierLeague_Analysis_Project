/*
This query is used for inserting game player stats for a specific game. Note that a game player is all players but goalies

It works as followed:
It is executed with a list of player stats, so first we need to unpack this list via unwind
We then find the player node, via name. We have no two players with the same name.
We match this with squad and season name, and then create a relation between the  player and the match the stat is for.

We then set the attributes of the relation.

*/

UNWIND $player_stats AS ps
MATCH (player:Player {name: ps.player_name})
MATCH (squad:Squad {team: ps.team_name, season:  $season_name})
MATCH (player)-[:IS_IN_SQUAD]->(squad)
MATCH (match:Match {id: ps.match_id})
MERGE (player)-[h:PLAYS_IN]->(match)
SET h.goals = toInteger(ps.goals),
    h.position = ps.position,
    h.assists = toInteger(ps.assists),
    h.penalties = toInteger(ps.penalties),
    h.shots = toInteger(ps.shots),
    h.shots_on_target = toInteger(ps.shots_on_target),
    h.touches = toInteger(ps.touches),
    h.tackles = toInteger(ps.tackles),
    h.interceptions = toInteger(ps.interceptions),
    h.blocks = toInteger(ps.blocks),
    h.xg = toFloat(ps.xg),
    h.npxg = toFloat(ps.npxg),
    h.xag = toFloat(ps.xag),
    h.sca = toInteger(ps.sca),
    h.gca = toInteger(ps.gca),
    h.passes_completed = toInteger(ps.passes_completed),
    h.passes_attempted = toInteger(ps.passes_attempted),
    h.pass_accuracy = toFloat(ps.pass_accuracy),
    h.progressive_passes = toInteger(ps.progressive_passes),
    h.carries = toInteger(ps.carries),
    h.progressive_carries = toInteger(ps.progressive_carries);
