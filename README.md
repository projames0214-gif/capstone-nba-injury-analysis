# capstone-nba-injury-analysis
---

## Database Schema

5-table PostgreSQL schema:

- `player` — player ID, name, height, weight, team
- `team` — team name, conference, division
- `season_stats` — per-season workload metrics (minutes, usage rate, age, pace)
- `injury_event` — injury date, type, days missed, season
- `injury_risk_score` — ML output table (stretch goal)

---

## ETL Pipeline

1. **Extract** — read both raw CSVs into Pandas DataFrames
2. **Transform** — convert string columns to numeric/datetime, handle nulls, save cleaned CSV
3. **Load** — insert into PostgreSQL tables in foreign key order (team → player → season_stats → injury_event)

Orchestrated by Apache Airflow — `extract_task >> transform_task >> load_task`

---

## Dashboard

Built with Dash and Plotly, connected to PostgreSQL. 8 visualizations:

- Most common injury types
- Injuries by player workload tier
- Injuries by age group
- Injury probability by workload tier
- Average days missed by injury type
- Injury trends by season (2013–2023)
- Top 10 players by total days missed
- Teams with most injury events

### Screenshots

![Dashboard Header](screenshots/Screenshot%202026-06-30%20at%204.34.53%20PM.png)
![Workload Chart](screenshots/Screenshot%202026-06-30%20at%204.35.22%20PM.png)
![Age Group Chart](screenshots/Screenshot%202026-06-30%20at%204.35.30%20PM.png)
![Days Missed Chart](screenshots/Screenshot%202026-06-30%20at%204.35.39%20PM.png)
![Season Trend](screenshots/Screenshot%202026-06-30%20at%204.35.46%20PM.png)
![Top Players](screenshots/Screenshot%202026-06-30%20at%204.36.03%20PM.png)
![Teams Chart](screenshots/Screenshot%202026-06-30%20at%204.36.13%20PM.png)
![Injury Probability](screenshots/Screenshot%202026-06-30%20at%204.36.22%20PM.png)

---

## Key Findings

- **Ankle and knee injuries dominate** — sprained ankles (588) and sore knees (353) account for the majority of all recorded injury events
- **Workload is the strongest predictor** — high-minute players (>28 min/game) are injured at 45.9% vs 9% for low-minute players
- **Prime-age players (23–28) get injured most** — reflecting their heavier playing time
- **Mavericks, Nets, and Knicks** report the highest injury counts across the dataset
- **Knee injuries cause the most missed time** — averaging 15 days missed vs 10 for ankle sprains

---

## How to Run

### Prerequisites
- Python 3.10+
- PostgreSQL 18
- Apache Airflow 3.2.2

### Setup

```bash
# Clone the repo
git clone https://github.com/projames0214-gif/capstone-nba-injury-analysis.git
cd capstone-nba-injury-analysis

# Install dependencies
pip3 install pandas psycopg2-binary dash plotly apache-airflow

# Create the database
psql -U your_username -d postgres -c "CREATE DATABASE nba_injury_analysis;"

# Run the schema
psql -U your_username -d nba_injury_analysis -f sql/schema.sql

# Run the ETL
python3 etl/etl.py

# Launch the dashboard
python3 dashboard/app.py
# Open http://127.0.0.1:8050
```

---

## Author

**Dylan James** — Dev10 Data Engineering Trainee
GitHub: [@projames0214-gif](https://github.com/projames0214-gif)