/*
This query is used for retrieving the league table for a specific season.

Is does this by taking in a specifided season ($season_name) as a parameter and performs the following logic:
* Find all matches that are part of this season.
* Performs logic for league points: Every win in a game is worth 3 points, loss is 1 point and draw is 0.
* Sum's this league points, and then also sums net game goal difference. 
Returns each team in order, first by total league points and then if they have the same amount of league points, the one with the higher goal difference.
*/


MATCH (match:Match)-[:IS_PART_OF]->(season:Season {season: $season_name}) 
MATCH (match)-[:HOME_TEAM]->(home_team:Squad)
MATCH (match)-[:AWAY_TEAM]->(away_team:Squad)
WHERE date(match.date) < date()

WITH 
    home_team, away_team,
    match.home_score AS home_goals,
    match.away_score AS away_goals,
    CASE
        WHEN match.home_score > match.away_score THEN 3
        WHEN match.home_score = match.away_score THEN 1
        ELSE 0
    END AS home_points,
    CASE
        WHEN match.away_score > match.home_score THEN 3
        WHEN match.away_score = match.home_score THEN 1
        ELSE 0
    END AS away_points

UNWIND [
    {team: home_team.team, points: home_points, goals_scored: home_goals, goals_conceded: away_goals},
    {team: away_team.team, points: away_points, goals_scored: away_goals, goals_conceded: home_goals}
] 
AS result

WITH result.team AS team, 
     SUM(result.points) AS total_points,
     SUM(result.goals_scored) AS total_goals,
     SUM(result.goals_scored) - SUM(result.goals_conceded) AS goal_difference

RETURN team, total_points, goal_difference
ORDER BY total_points DESC, goal_difference DESC