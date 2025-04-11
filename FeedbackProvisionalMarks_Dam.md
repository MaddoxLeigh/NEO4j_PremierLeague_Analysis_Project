# DAM
## Project title: Football Database  
### Group: DAM
### Candidate Numbers: 49150, 39706, 45417

---

## TOPIC AND SCENARIO (maximum 15 points)


This project presents a football database built around FIFA World Cup data, with the aim of analysing team and player performance. The topic is popular and data-rich, and the use of Neo4j adds an interesting dimension.

However, the final implementation does not align with the scenario originally proposed. The group had planned to build a system that could predict match outcomes, evaluate the impact of injuries and weather, and use rich, up-to-date sources such as the Football Data API and Fantasy Premier League datasets. These were not included in the final submission, and the project shifted toward static, descriptive analysis based on a single historical dataset. This narrowing of scope is partially acknowledged in the report.

Some suggestions from the feedback, such as prioritizing dynamic queries are not incorporated, but a query constructing a ‘dream team’ is added. The other queries from the proposal are somewhat simplified.

The scenario feels underdeveloped, with no clear user or application context (e.g., who would use this database, and for what decisions?). As a result, the topic remains technically valid but lacks depth.



---

## DATA (maximum 10 points)

The group obtained the data through web scraping from fbref.com, a football statistics site and a solid data source. This site offers detailed and structured data and performance metrics across multiple seasons. The web scraping process is documented in their notebooks, but not that well explained in the report (what is the structure of the data that is scraped), what kind of cleaning was required, what clubs/leagues were considered, how many years of data in total. Was there some part of the data that was available but excluded because of the simplicity of the model. Some discussion is missing on the limitations.

Perhaps another data source could have been used (like weather), or additional data could be derived, such as the distance the the away team had to travel etc.

Good job using web scraping, but it would’ve helped to have more data sources to match the original project goals.




---


## DATABASE MODELLING (maximum 20 points)

The project uses Neo4j to model a property graph of football data, with entities such as Player, Squad, Match, Season, Venue, and Referee. The choice of Neo4j is justified and mostly well-executed — football is inherently relationship-driven, and the use of graph modelling supports many of the proposed queries.

Some limitations are discussed: not able to model January transfers, but not resolved.
There is no TEAM node, but SQUAD (for specific season). SQUAD node makes sense, however, having TEAM node related to SQUAD nodes might be a good solution. Then you could store some additional general information about the team within the TEAM node,  and store the team’s name in a single place.

It seems that only the PLAYED relationship has attributes, perhaps there was an opportunity to add more data to some of the relationships. The model does not support any temporal analysis which could be of interest (for example the time when the goal is scored is not recorded). The PLAYER has a contract_expiry attribute, so only the information about the current contract is stored - another limitation. Could the information about contract be stored in IS_IN_SQUAD relationship?




---

## DATABASE CREATION (maximum 10 points)

The group created the database using Python and Jupyter notebooks, successfully automating the scraping, transformation, and insertion of football data into Neo4j.

There is no mention of constraints, indexes (to speed up the performance of some queries), checking for consistency, uniqueness, before importing. Were any checks performed on the data (duplicate players, missing match links?)



---

## DATABASE USAGE (maximum 35 points)


- **Query 1** It seems that the injury is assumed here if a player missed a match - but could there be other reasons for the player to miss the game? Only one season is considered (also how many seasons are there in total?). The discussion of the query ends on a conclusion about the impact of the player and that they will be chosen to play (so not about injuries). The interpretation is weakened here by the fact that injury is not properly modeled
- **Query 2-4**  Perhaps some statistical testing could have been done, to compare the two distributions. For example in query 3, we cannot talk about statistical significance without that. Perhaps it would make sense to adjust for the strength of the opponent (maybe divide teams in groups based on their performance, to compare similar with similar). (Up to this point it is not clear from the text if it is Premier League only that is considered? ). Possible bias could be included if for some seasons the scraped that is not complete. Other metrics, like possesion etc, instead of the number of goals, could also be considered here. There is room for expanding this query. Query 4 is a good idea to expand the previous two.
- **Query 5** Good, this query generates a “dream team” (in 4-3-3 formation) by selecting the top defenders, midfielders, and forwards based on a user-selected performance statistic, also using a visualisation tool. Potential problem with this is that it does not adjust for the number of minutes played per game.
- **Query 6** This query constructs a “dream team” by calculating a performance score based on multiple weighted statistics, with different weightings for defenders, midfielders, and forwards. Not clear how the weights are chosen. There is no mention of the goalkeeper. Could the obtained results be verified - are the players recognised as best the same as those recognised as best by some existing rankings?
- **Query 6 (you have two Q6 in your report)** This query compares defenders’ performances across two consecutive seasons. Good - this query includes temporal change, not a static query like the other ones. Again, could these results be “verified”? Do the analysts or fans agree?
- **Query 7** Good. This query calculates and displays the league table standings for a selected season, ranking teams by total points and applying goal difference as a tiebreaker.


---

## DATABASE TECHNOLOGY (maximum 5 points)


It is argued that football data is inherently relational and that Neo4j allows these relationships to be modelled more naturally than in SQL. This is a fair point, especially since many queries involve traversing multiple hops between connected entities (e.g., player → match → team).

It would be useful if some queries were considered that would be very hard to do in SQL. For example traversing the graph (something like finding “neighbouring” nodes, with some degree of separation). Most of the implemented queries could still be expressed in SQL, which weakens the practical justification for using a graph database.

---

## DOCUMENTATION (maximum 5 points)

The report lacks more complete documentation of what exactly is scraped form fbref. Otherwise it is well-structured and clear, and covers most key elements of the project.


---

**Total Suggested Score: 94.5 / 100**


| Problem breakdown       | Max marks | Your marks |
|-------------------------|-----------|------------|
| (2) Topic/scenario      | 15        | 10         |
| (3) Data                | 10        | 6          |
| (4) Database modelling  | 20        | 12         |
| (5) Database creation   | 10        | 6          |
| (6) Database usage      | 35        | 22         |
| (7) Database technology | 5         | 2          |
| Documentation           | 5         | 3          |
| TOTAL                   | 100       | 61         |
