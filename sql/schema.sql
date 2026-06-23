-- NBA Injury & Performance Analysis Schema

DROP TABLE IF EXISTS injury_risk_score;
DROP TABLE IF EXISTS injury_event;
DROP TABLE IF EXISTS season_stats;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS team;

-- Teams
CREATE TABLE team (
    team_id     SERIAL PRIMARY KEY,
    team_name   VARCHAR(100) NOT NULL UNIQUE,
    conference  VARCHAR(10),
    division    VARCHAR(50)
);

-- Players
CREATE TABLE player (
    player_id   INTEGER PRIMARY KEY,
    player_name VARCHAR(100) NOT NULL,
    position    VARCHAR(5),
    height_in   FLOAT,
    weight_lbs  FLOAT,
    draft_year  INTEGER,
    team_id     INTEGER REFERENCES team(team_id)
);

-- Season stats
CREATE TABLE season_stats (
    stat_id         SERIAL PRIMARY KEY,
    player_id       INTEGER REFERENCES player(player_id),
    season          VARCHAR(10),
    age             FLOAT,
    games_played    INTEGER,
    minutes_per_game FLOAT,
    usage_rate      FLOAT,
    points_per_game FLOAT,
    pace            FLOAT,
    drives          FLOAT,
    dist_miles      FLOAT
);

-- Injury events
CREATE TABLE injury_event (
    injury_id       SERIAL PRIMARY KEY,
    player_id       INTEGER REFERENCES player(player_id),
    injury_date     DATE,
    returned_date   DATE,
    days_missed     FLOAT,
    injury_type     VARCHAR(100),
    notes           TEXT,
    season          VARCHAR(10)
);

-- ML injury risk scores (stretch goal)
CREATE TABLE injury_risk_score (
    score_id        SERIAL PRIMARY KEY,
    player_id       INTEGER REFERENCES player(player_id),
    season          VARCHAR(10),
    workload_index  FLOAT,
    risk_score      FLOAT,
    risk_tier       VARCHAR(20)
);