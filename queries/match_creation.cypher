/*
This query is used for inserting general match data for matches played. This has some logic for detecting when a match has occured.

First as this is just executed once for all matches in a season, we use unwind.
As a match node would have not been made for this match yet, we use create and set attributes.
We then try to find the venue node(if it already exists) and if not, create a  new one and add the PLAYED_AT relation between match and venue.
Then, we match the home and away team nodes and set up their relations.
Finally, if in the data we have Match_Report=True, we know that we also have some more specific match attributes to set (such as scores, referee and expected goals) so we add this.

AI was used to assist with the logic with the FOREACH to add match report specific data when it was in the match_data.
*/



UNWIND $matches AS match_data
CREATE (match:Match {id: match_data.Match_ID})
SET match.date = date(match_data.Date),
    match.time = time(match_data.Time),
    match.home_score = toInteger(match_data.Home_Score),
    match.away_score = toInteger(match_data.Away_Score),
    match.home_expected = toFloat(match_data.Home_Expected),
    match.away_expected = toFloat(match_data.Away_Expected),
    match.game_week = match_data.GW,
    match.attendance = match_data.Attendance


MERGE (venue:Venue {name: match_data.Venue})
MERGE (match)-[:PLAYED_AT]->(venue)

WITH match, match_data
MATCH (home_team:Squad {team: match_data.Home, season:$season_name})
MATCH (away_team:Squad {team: match_data.Away, season: $season_name})
Merge (season:Season {season:$season_name })
MERGE (match)-[:HOME_TEAM]->(home_team)
MERGE (match)-[:AWAY_TEAM]->(away_team)
MERGE (match)-[:IS_PART_OF]->(season)

FOREACH (_ IN CASE WHEN match_data.Match_Report THEN [1] ELSE [] END |
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