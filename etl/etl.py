import pandas as pd
import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname="nba_injury_analysis",
    user="dylanjames",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Load raw data
print("Loading raw data...")
injury_df = pd.read_csv('data/raw/NBA Player Injury Stats(1951 - 2023).csv')
stats_df = pd.read_csv('data/raw/nba_player_stats_injuries.csv')

# Clean stats dataset
print("Cleaning stats data...")
stats_df['PLAYER_HEIGHT_INCHES'] = pd.to_numeric(stats_df['PLAYER_HEIGHT_INCHES'], errors='coerce')
stats_df['PLAYER_WEIGHT'] = pd.to_numeric(stats_df['PLAYER_WEIGHT'], errors='coerce')
stats_df['DIST_MILES'] = pd.to_numeric(stats_df['DIST_MILES'], errors='coerce')
stats_df['AVG_SPEED'] = pd.to_numeric(stats_df['AVG_SPEED'], errors='coerce')
stats_df['INJURED ON'] = pd.to_datetime(stats_df['INJURED ON'], errors='coerce')
stats_df['RETURNED'] = pd.to_datetime(stats_df['RETURNED'], errors='coerce')

# Clean injury dataset
print("Cleaning injury data...")
injury_df['Date'] = pd.to_datetime(injury_df['Date'], errors='coerce')
injury_df = injury_df.dropna(subset=['Date'])

# Load teams
print("Loading teams...")
teams = stats_df['TEAM'].dropna().unique()
for team in teams:
    cur.execute(
        "INSERT INTO team (team_name) VALUES (%s) ON CONFLICT (team_name) DO NOTHING",
        (team,)
    )

# Load players
print("Loading players...")
players = stats_df[['PLAYER_ID', 'PLAYER_NAME', 'PLAYER_HEIGHT_INCHES', 'PLAYER_WEIGHT']].drop_duplicates(subset='PLAYER_ID')
for _, row in players.iterrows():
    cur.execute("""
        INSERT INTO player (player_id, player_name, height_in, weight_lbs)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (player_id) DO NOTHING
    """, (row['PLAYER_ID'], row['PLAYER_NAME'], row['PLAYER_HEIGHT_INCHES'], row['PLAYER_WEIGHT']))

# Load season stats
print("Loading season stats...")
for _, row in stats_df.iterrows():
    cur.execute("""
        INSERT INTO season_stats (player_id, season, age, games_played, minutes_per_game, usage_rate, pace, drives, dist_miles)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['PLAYER_ID'], row['SEASON'], row['AGE'], row['GP'], row['MIN'], row['USG_PCT'], row['PACE'], row['DRIVES'], row['DIST_MILES']))

# Load injury events
print("Loading injury events...")
injured = stats_df.dropna(subset=['INJURED ON'])
for _, row in injured.iterrows():
    cur.execute("""
        INSERT INTO injury_event (player_id, injury_date, returned_date, days_missed, injury_type, season)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (row['PLAYER_ID'], row['INJURED ON'], row['RETURNED'], row['DAYS MISSED'], row['INJURED_TYPE'], row['SEASON']))

conn.commit()
cur.close()
conn.close()
print("ETL complete!")