import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import psycopg2

# Database connection
def get_connection():
    return psycopg2.connect(
        dbname="nba_injury_analysis",
        user="dylanjames",
        host="localhost",
        port="5432"
    )

# Load data
conn = get_connection()

# Q1: Most common injury types
injury_types = pd.read_sql("""
    SELECT injury_type, COUNT(*) AS total
    FROM injury_event
    WHERE injury_type IS NOT NULL
    GROUP BY injury_type
    ORDER BY total DESC
    LIMIT 10
""", conn)

# Q2: Workload vs injuries
workload = pd.read_sql("""
    SELECT
        CASE
            WHEN minutes_per_game < 15 THEN 'Low (<15 min)'
            WHEN minutes_per_game BETWEEN 15 AND 28 THEN 'Medium (15-28 min)'
            ELSE 'High (>28 min)'
        END AS workload_tier,
        COUNT(ie.injury_id) AS total_injuries
    FROM season_stats ss
    LEFT JOIN injury_event ie ON ss.player_id = ie.player_id
    GROUP BY workload_tier
    ORDER BY total_injuries DESC
""", conn)

# Q3: Age vs injuries
age_injuries = pd.read_sql("""
    SELECT
        CASE
            WHEN age < 23 THEN 'Young (under 23)'
            WHEN age BETWEEN 23 AND 28 THEN 'Prime (23-28)'
            ELSE 'Veteran (over 28)'
        END AS age_group,
        COUNT(ie.injury_id) AS total_injuries
    FROM season_stats ss
    LEFT JOIN injury_event ie ON ss.player_id = ie.player_id
    GROUP BY age_group
    ORDER BY total_injuries DESC
""", conn)

# Q4: Injury probability by workload tier
workload_probability = pd.read_sql("""
    SELECT
        CASE
            WHEN minutes_per_game < 15 THEN 'Low (<15 min)'
            WHEN minutes_per_game BETWEEN 15 AND 28 THEN 'Medium (15-28 min)'
            ELSE 'High (>28 min)'
        END AS workload_tier,
        COUNT(DISTINCT ss.player_id) AS total_players,
        COUNT(DISTINCT ie.player_id) AS injured_players,
        ROUND(COUNT(DISTINCT ie.player_id)::numeric / COUNT(DISTINCT ss.player_id) * 100, 1) AS injury_probability_pct
    FROM season_stats ss
    LEFT JOIN injury_event ie ON ss.player_id = ie.player_id AND ss.season = ie.season
    GROUP BY workload_tier
    ORDER BY injury_probability_pct DESC
""", conn)

# Q5: Avg days missed by injury type
days_missed = pd.read_sql("""
    SELECT injury_type, ROUND(AVG(days_missed)) AS avg_days_missed
    FROM injury_event
    WHERE days_missed IS NOT NULL AND injury_type IS NOT NULL
    GROUP BY injury_type
    ORDER BY avg_days_missed DESC
    LIMIT 10
""", conn)

# Q8: Injuries by season
season_trend = pd.read_sql("""
    SELECT season, COUNT(*) AS total_injuries
    FROM injury_event
    WHERE season IS NOT NULL
    GROUP BY season
    ORDER BY season
""", conn)

# Q9: Top 10 players with most days missed
top_players = pd.read_sql("""
    SELECT p.player_name, SUM(ie.days_missed) AS total_days_missed
    FROM player p
    JOIN injury_event ie ON p.player_id = ie.player_id
    GROUP BY p.player_name
    ORDER BY total_days_missed DESC
    LIMIT 10
""", conn)

# Q6: Teams with most injury events
team_injuries = pd.read_sql("""
    SELECT t.team_name, COUNT(ie.injury_id) AS total_injuries
    FROM team t
    JOIN player p ON t.team_id = p.team_id
    JOIN injury_event ie ON p.player_id = ie.player_id
    GROUP BY t.team_name
    ORDER BY total_injuries DESC
    LIMIT 10
""", conn)

conn.close()

# Build charts
fig1 = px.bar(injury_types, x='injury_type', y='total',
              title='Most Common Injury Types',
              labels={'injury_type': 'Injury Type', 'total': 'Total Injuries'},
              color='total', color_continuous_scale='Blues')

fig2 = px.bar(workload, x='workload_tier', y='total_injuries',
              title='Injuries by Player Workload (Minutes per Game)',
              labels={'workload_tier': 'Workload Tier', 'total_injuries': 'Total Injuries'},
              color='total_injuries', color_continuous_scale='Oranges')

fig3 = px.bar(age_injuries, x='age_group', y='total_injuries',
              title='Injuries by Age Group',
              labels={'age_group': 'Age Group', 'total_injuries': 'Total Injuries'},
              color='total_injuries', color_continuous_scale='Greens')

fig4 = px.bar(days_missed, x='injury_type', y='avg_days_missed',
              title='Average Days Missed by Injury Type',
              labels={'injury_type': 'Injury Type', 'avg_days_missed': 'Avg Days Missed'},
              color='avg_days_missed', color_continuous_scale='Reds')

fig5 = px.line(season_trend, x='season', y='total_injuries',
               title='Injury Trends by Season',
               labels={'season': 'Season', 'total_injuries': 'Total Injuries'},
               markers=True)

fig6 = px.bar(top_players, x='player_name', y='total_days_missed',
              title='Top 10 Players by Total Days Missed',
              labels={'player_name': 'Player', 'total_days_missed': 'Total Days Missed'},
              color='total_days_missed', color_continuous_scale='Purples')
fig7 = px.bar(team_injuries, x='team_name', y='total_injuries',
              title='Teams with Most Injury Events',
              labels={'team_name': 'Team', 'total_injuries': 'Total Injuries'},
              color='total_injuries', color_continuous_scale='Teal')
fig8 = px.bar(workload_probability, x='workload_tier', y='injury_probability_pct',
              title='Injury Probability by Player Workload',
              labels={'workload_tier': 'Workload Tier', 'injury_probability_pct': 'Injury Probability (%)'},
              color='injury_probability_pct', color_continuous_scale='Reds',
              text='injury_probability_pct')
# App layout
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(
        children='NBA Player Injury & Performance Analysis',
        style={'textAlign': 'center', 'fontFamily': 'Arial', 'color': '#1a1a2e'}
    ),
    html.P(
        children='Capstone Project — Dylan James | Dev10',
        style={'textAlign': 'center', 'fontFamily': 'Arial', 'color': 'gray'}
    ),
    html.Div(children=[dcc.Graph(figure=fig1)], style={'marginBottom': '30px'}),
    html.Div(children=[dcc.Graph(figure=fig2)], style={'marginBottom': '30px'}),
    html.Div(children=[dcc.Graph(figure=fig3)], style={'marginBottom': '30px'}),
    html.Div(children=[dcc.Graph(figure=fig4)], style={'marginBottom': '30px'}),
    html.Div(children=[dcc.Graph(figure=fig5)], style={'marginBottom': '30px'}),
    html.Div(children=[dcc.Graph(figure=fig6)], style={'marginBottom': '30px'}),
    html.Div(children=[dcc.Graph(figure=fig7)], style={'marginBottom': '30px'}),
    html.Div(children=[dcc.Graph(figure=fig8)], style={'marginBottom': '30px'}),
],  style={'backgroundColor': '#f5f0e6', 'padding': '20px'})
if __name__ == '__main__':
    app.run(debug=True)