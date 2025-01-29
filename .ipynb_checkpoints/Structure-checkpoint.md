# Project File Structure

This document explains the organization of the project files and directories.

├── config                     
│   ├── .env 
├── data                     
│   ├── season
│   │   └── 2024-2025
│   │       ├── fixtures.json
│   │       ├── players.json
│   │       └── teams.json
│   ├── [Additional season-specific files]
├── queries                     
│   ├── goalie_game_stats.cypher
│   └── match_creation.cypher
│   └── [Additional cypher query files]
├── utilities                     
│   ├── fbref.py
│   ├── cypher_query_loader.py

## Config
This directory contains the configuration file for this project. This is to store environment variables to connect with our neo4j instance.

## Data
This directory is structured to contain many other directories, labelled as as a premier league season. Within each of this season directories are the three files needed to create our graph database. 
* fixtures.json contains all matches, with general match statistics such as home and away team, time, venue, referee. But also contains player specific information for the players that were active in that match.
* players.json contains general player statistics for all players that feature in a team in this season.
* teams.json outlines all teams and which players were in their team for the season.

## Queries
This directory contains a set of files which are our cypher queries to be executed in any notebook. These are all of .cypher type

## Utilities
This directory contains any auxillary classes that are needed throughout our project. 
