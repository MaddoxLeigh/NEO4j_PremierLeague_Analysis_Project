# ST207 Group Project - AT2024

## Group name

Dam

## Topic (database application)

We will be using the database application to store data about football games, the players and their teams. This is so that we can predict football match odds. These predictions will mainly require analysis of match outcomes, individual player performance, and team trends. If possible, we will also take into account weather conditions of where each game is being played.

## Data sources

* Football Data API - https://www.football-data.org
* Fantasy Football dataset - https://github.com/vaastav/Fantasy-Premier-League.git

Will be our two main sources of data as they seem pretty conclusive. If not, these are some other sources:

* https://www.api-football.com/documentation-v3
* Web-scrapping data off of https://fantasy.premierleague.com/statistics

## Proposed use cases and queries

* "Use Case: Predict match outcomes.
Query: ""What is the probability of Team A winning against Team B based on recent performance?”

* Use Case: Analyze key player contributions.
Query: ""Which players contribute most to Team X’s success against opponents?""

* Use Case: Track team performance trends.
Query: ""How has Team C’s performance changed over the past three seasons compared to other league teams?""

* Use Case: Assess the impact of injuries.
Query: ""How does Player X's absence affect a Teams win rate in away games?""

* Use Case: Explore game factors and scoring patterns.
Query: ""What are the common scoring patterns in rainy matches, and which teams adapt best?"""

## Feedback

The proposed database is relevant and close to a real scenario. You may prioritise data that allows for more analytical queries, such as patterns, evolution of a given attribute over time, any groups or clusterings that allow for window functions or similar, and other "dynamic" aspects of the database. You should avoid any static queries, such as retrieving basic information from tables.

In this sense, most of your queries seem to concentrate on patterns, which is fine. You mentioned prediction, so it would be nice to have queries exploring that. I don't see major points needing clarification or revision, provided you focus your database on the dynamic aspects of the proposed queries.

What about adding a query to infer the best 11 squad ("dream team")?

## Decision: approved
