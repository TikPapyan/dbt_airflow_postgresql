SELECT
    "player name",
    MIN(season) AS first_season,
    MAX(season) AS last_season,
    COUNT(DISTINCT season) AS seasons_played,
    AVG(pts) AS career_avg_points
FROM {{ source('public', 'nba_players') }}
GROUP BY "player name"
HAVING COUNT(DISTINCT season) > 1 -- Filtering out players with only one season
ORDER BY seasons_played DESC
