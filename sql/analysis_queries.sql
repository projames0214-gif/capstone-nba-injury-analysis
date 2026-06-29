-- NBA Injury & Performance Analysis Queries
-- Author: Dylan James

-- Q1: Which injury types are most common?
SELECT injury_type, COUNT(*) AS total
FROM injury_event
GROUP BY injury_type
ORDER BY total DESC
LIMIT 10;

-- Q2: Do players who play more minutes get injured more?
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
ORDER BY total_injuries DESC;

-- Q3: Does age correlate with injury frequency?
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
ORDER BY total_injuries DESC;

-- Q4: Which positions have the highest injury rates?
SELECT p.position, COUNT(ie.injury_id) AS total_injuries
FROM player p
LEFT JOIN injury_event ie ON p.player_id = ie.player_id
WHERE p.position IS NOT NULL
GROUP BY p.position
ORDER BY total_injuries DESC;

-- Q5: Which injury types cause the most games missed?
SELECT injury_type, ROUND(AVG(days_missed)) AS avg_days_missed, COUNT(*) AS occurrences
FROM injury_event
WHERE days_missed IS NOT NULL
GROUP BY injury_type
ORDER BY avg_days_missed DESC
LIMIT 10;

-- Q6: Which teams have the most injury events?
SELECT t.team_name, COUNT(ie.injury_id) AS total_injuries
FROM team t
JOIN player p ON t.team_id = p.team_id
JOIN injury_event ie ON p.player_id = ie.player_id
GROUP BY t.team_name
ORDER BY total_injuries DESC
LIMIT 10;

-- Q7: What is the average days missed per injury type?
SELECT injury_type, AVG(days_missed) AS avg_days_missed
FROM injury_event
WHERE days_missed IS NOT NULL AND injury_type IS NOT NULL
GROUP BY injury_type
ORDER BY avg_days_missed DESC;

-- Q8: How do injuries trend by season?
SELECT season, COUNT(*) AS total_injuries
FROM injury_event
WHERE season IS NOT NULL
GROUP BY season
ORDER BY season;

-- Q9: Top 10 players with most days missed
SELECT p.player_name, SUM(ie.days_missed) AS total_days_missed
FROM player p
JOIN injury_event ie ON p.player_id = ie.player_id
GROUP BY p.player_name
ORDER BY total_days_missed DESC
LIMIT 10;

-- Q10: High usage players vs injury rate
SELECT
    CASE
        WHEN usage_rate < 0.15 THEN 'Low usage'
        WHEN usage_rate BETWEEN 0.15 AND 0.25 THEN 'Medium usage'
        ELSE 'High usage'
    END AS usage_tier,
    COUNT(ie.injury_id) AS total_injuries,
    ROUND(AVG(ie.days_missed)) AS avg_days_missed
FROM season_stats ss
LEFT JOIN injury_event ie ON ss.player_id = ie.player_id
GROUP BY usage_tier
ORDER BY total_injuries DESC;