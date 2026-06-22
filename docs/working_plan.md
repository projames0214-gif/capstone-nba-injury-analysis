# Working Plan — NBA Player Injury & Performance Analysis

## Project Overview
This project analyzes NBA player injury history and performance statistics to identify
patterns and risk factors associated with player injuries. Using historical injury
transaction data (1951–2023) and season-level player stats (2013–2023), I will build
a data pipeline that cleans, joins, and loads these datasets into PostgreSQL via an
Airflow ETL. The analysis will focus on correlating workload, age, position, and
performance metrics with injury frequency and severity. A Dash dashboard will visualize
findings across the league, and an optional machine learning model will score players
by predicted injury risk for a given season.

## Questions to Answer
1. Which body parts are most commonly injured in the NBA, and has that changed over the last decade?
2. Do players who average more minutes per game have a higher rate of injury?
3. Does age correlate with injury frequency — do older players get hurt more often?
4. Which positions (PG, SG, SF, PF, C) have the highest injury rates?
5. Do players with high usage rates in one season miss more games the following season?
6. How does injury frequency vary by team — are some franchises harder on their players?
7. What types of injuries result in the most games missed?
8. Is there a time of season when injuries peak — early, mid-season, or playoffs?
9. Can we predict whether a player will miss significant time based on workload and age?
10. How does a major injury affect a player's performance stats in seasons after they return?