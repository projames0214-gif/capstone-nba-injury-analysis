from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import psycopg2

default_args = {
    'owner': 'dylanjames',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extract():
    print("Extracting raw data...")
    injury_df = pd.read_csv('/Users/dylanjames/capstone-nba-injury-analysis/data/raw/NBA Player Injury Stats(1951 - 2023).csv')
    stats_df = pd.read_csv('/Users/dylanjames/capstone-nba-injury-analysis/data/raw/nba_player_stats_injuries.csv')
    print(f"Injury records: {len(injury_df)}")
    print(f"Stats records: {len(stats_df)}")

def transform():
    print("Transforming data...")
    stats_df = pd.read_csv('/Users/dylanjames/capstone-nba-injury-analysis/data/raw/nba_player_stats_injuries.csv')
    stats_df['PLAYER_HEIGHT_INCHES'] = pd.to_numeric(stats_df['PLAYER_HEIGHT_INCHES'], errors='coerce')
    stats_df['PLAYER_WEIGHT'] = pd.to_numeric(stats_df['PLAYER_WEIGHT'], errors='coerce')
    stats_df['DIST_MILES'] = pd.to_numeric(stats_df['DIST_MILES'], errors='coerce')
    stats_df['AVG_SPEED'] = pd.to_numeric(stats_df['AVG_SPEED'], errors='coerce')
    stats_df['INJURED ON'] = pd.to_datetime(stats_df['INJURED ON'], errors='coerce')
    stats_df['RETURNED'] = pd.to_datetime(stats_df['RETURNED'], errors='coerce')
    cleaned_path = '/Users/dylanjames/capstone-nba-injury-analysis/data/cleaned/stats_cleaned.csv'
    stats_df.to_csv(cleaned_path, index=False)
    print(f"Cleaned data saved to {cleaned_path}")

def load():
    print("Loading data into PostgreSQL...")
    conn = psycopg2.connect(
        dbname="nba_injury_analysis",
        user="dylanjames",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    stats_df = pd.read_csv('/Users/dylanjames/capstone-nba-injury-analysis/data/cleaned/stats_cleaned.csv')

    teams = stats_df['TEAM'].dropna().unique()
    for team in teams:
        cur.execute(
            "INSERT INTO team (team_name) VALUES (%s) ON CONFLICT (team_name) DO NOTHING",
            (team,)
        )

    players = stats_df[['PLAYER_ID', 'PLAYER_NAME', 'PLAYER_HEIGHT_INCHES', 'PLAYER_WEIGHT']].drop_duplicates(subset='PLAYER_ID')
    for _, row in players.iterrows():
        cur.execute("""
            INSERT INTO player (player_id, player_name, height_in, weight_lbs)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (player_id) DO NOTHING
        """, (row['PLAYER_ID'], row['PLAYER_NAME'], row['PLAYER_HEIGHT_INCHES'], row['PLAYER_WEIGHT']))

    conn.commit()
    cur.close()
    conn.close()
    print("Load complete!")

with DAG(
    dag_id='nba_injury_etl',
    default_args=default_args,
    description='ETL pipeline for NBA injury and performance data',
    schedule='@daily',
    start_date=datetime(2026, 6, 1),
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
    )

    extract_task >> transform_task >> load_task