# Technical Report — NBA Player Injury & Performance Analysis
**Author:** Dylan James  
**Program:** Dev10 Data Engineering  
**Date:** July 2, 2026

---

## 1. Questions Asked

1. Which injury types are most common in the NBA?
2. Given a player's workload (minutes per game), what is the probability they get injured in a season?
3. Does age correlate with injury frequency?
4. Which injury types cause the most games missed?
5. Which teams have the most injury events?
6. How do injuries trend across NBA seasons (2013–2023)?
7. Which players have missed the most total days to injury?
8. Can workload tier predict injury likelihood?

---

## 2. Datasets Used

### Primary Dataset
**NBA Injury Stats (1951–2023)**  
- Source: Kaggle — loganlauton/nba-injury-stats-1951-2023  
- Accessed: June 22, 2026  
- Format: CSV  
- Shape: 37,667 rows × 6 columns  
- Key columns: `Date`, `Team`, `Acquired`, `Relinquished`, `Notes`  
- Description: Every IL transaction in NBA history — players being placed on or activated from the injured list, with injury notes

### Supplementary Dataset
**NBA Player Stats & Injuries (2013–2023)**  
- Source: Kaggle — icliu30/nba-player-stats-and-injured-data-from-13-to-23  
- Accessed: June 22, 2026  
- Format: CSV  
- Shape: 5,578 rows × 32 columns  
- Key columns: `PLAYER_ID`, `SEASON`, `AGE`, `MIN`, `USG_PCT`, `GP`, `INJURED ON`, `DAYS MISSED`, `INJURED_TYPE`, `TEAM`  
- Description: Season-level player performance stats merged with injury outcome data for the 2013–2023 NBA seasons

### Non-CSV Source
**NBA API (nba_api Python package)**  
- Source: github.com/swar/nba_api  
- Accessed: June 22, 2026  
- Format: JSON (REST API)  
- Description: Official NBA stats API wrapper used for supplementary player bio data and game logs

---

## 3. ETL Process

### Extract
Both raw CSV datasets were read into Pandas DataFrames using `pd.read_csv()`. The injury stats dataset contained 37,667 rows and the player stats dataset contained 5,578 rows.

### Transform
The following cleaning steps were applied to the player stats dataset:

- **Type conversion (numeric):** `PLAYER_HEIGHT_INCHES`, `PLAYER_WEIGHT`, `DIST_MILES`, and `AVG_SPEED` were stored as strings in the raw data. These were converted using `pd.to_numeric(errors='coerce')`, which converts invalid values to null rather than raising an error.
- **Type conversion (datetime):** `INJURED ON` and `RETURNED` were stored as strings. These were converted using `pd.to_datetime(errors='coerce')`.
- **Null handling:** Rows with null `Date` values were dropped from the injury dataset. Null values in the injury columns (`INJURED ON`, `DAYS MISSED`, `INJURED_TYPE`) were retained as they indicate players who were not injured that season — an expected and meaningful absence of data.

The cleaned dataset was saved to `data/cleaned/stats_cleaned.csv`.

### Load
Data was loaded into PostgreSQL in foreign key order to satisfy referential integrity constraints:

1. `team` — unique team names inserted first
2. `player` — player records inserted with `ON CONFLICT DO NOTHING` to avoid duplicates
3. `season_stats` — one record per player per season
4. `injury_event` — one record per injury occurrence, filtered to rows with non-null injury data

An additional UPDATE step linked each player's `team_id` foreign key based on their most recent team in the stats dataset.

### Join Logic
The two datasets are joined on `PLAYER_ID` and `SEASON`:

```sql
SELECT *
FROM season_stats ss
LEFT JOIN injury_event ie 
  ON ss.player_id = ie.player_id 
  AND ss.season = ie.season
```

This links each player's workload statistics to their injury outcome for that same season, enabling the core analytical question: does higher workload correlate with higher injury probability?

### Airflow DAG
The ETL pipeline is orchestrated by Apache Airflow v3.2.2 as a DAG with three tasks:

The DAG is scheduled `@daily` with `catchup=False`, meaning it runs once per day going forward without backfilling historical runs.

---

## 4. Technologies Used

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.14 | ETL scripting, data cleaning |
| Pandas | 2.x | Data transformation |
| PostgreSQL | 18.3 | Relational database |
| psycopg2 | 2.9 | PostgreSQL Python adapter |
| Apache Airflow | 3.2.2 | ETL orchestration |
| Dash | 4.x | Dashboard framework |
| Plotly | 5.x | Data visualization |
| DBeaver | 26.1 | Database management |
| Jupyter | 7.x | Exploratory data analysis |
| Git / GitHub | — | Version control |

---

## 5. ML Model (Optional — Stretch Goal)

A machine learning injury risk scoring model was planned but not implemented within the project timeline. The database schema includes an `injury_risk_score` table designed to receive ML output:

```sql
CREATE TABLE injury_risk_score (
    score_id     SERIAL PRIMARY KEY,
    player_id    INTEGER REFERENCES player(player_id),
    season       VARCHAR(10),
    workload_index FLOAT,
    risk_score   FLOAT,
    risk_tier    VARCHAR(20)
);
```

The planned approach would use scikit-learn to train a binary classifier (injured vs. not injured) on features including `minutes_per_game`, `age`, `usage_rate`, `games_played`, and `pace`. Model output (probability score and risk tier) would be written back to the `injury_risk_score` table and visualized in the dashboard.

---

## 6. Conclusions

**Q1 — Most common injury types:**
Sprained ankle (588 occurrences) and sore knee (353 occurrences) are by far the most common injury types in the dataset, together accounting for the majority of all recorded injury events.

**Q2 — Injury probability by workload:**
This is the strongest finding in the project. Players averaging more than 28 minutes per game face a 45.9% injury probability in a given season, compared to 30.1% for medium-minute players and 9% for low-minute players. High-minute players are over 5x more likely to be injured than low-minute players. This finding directly validates the load management strategies used by modern NBA teams.

**Q3 — Age and injury frequency:**
Prime-age players (23–28) account for the most total injuries, followed by veterans (over 28), then young players (under 23). This reflects playing time distribution more than age-related fragility — prime-age players carry the heaviest workloads.

**Q4 — Games missed by injury type:**
Knee injuries cause the most days missed on average (15 days), followed by sprained ankles (10 days). Frequency and severity tell different stories — ankles happen more often, but knees are more costly in terms of recovery time.

**Q5 — Teams with most injuries:**
The Mavericks (146), Nets (144), and Knicks (138) reported the most injury events. These teams share a pattern of carrying high-mileage star rosters — aging veterans, injury-prone superstars, and high-usage players — during the 2013–2023 window.

**Q6 — Season trends:**
Injuries rose steadily from the 2013–14 season through 2021–22, then dropped in 2022–23. The rise may reflect improved reporting or increased pace of play. The drop in 2022–23 may indicate load management policies taking effect at a league-wide scale.

**Q7 — Players with most days missed:**
Andre Roberson (600 days) and Jonathan Isaac (~520 days) lead the dataset. Both players suffered severe knee injuries that derailed their careers during this window.

**Q8 — Workload and injury likelihood:**
Confirmed by Q2 — workload tier is the single strongest predictor of injury probability in this dataset. A binary classification model using workload and age as primary features would be the logical next step.