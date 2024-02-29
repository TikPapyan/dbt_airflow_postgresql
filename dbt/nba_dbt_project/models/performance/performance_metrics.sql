SELECT
    season,
    SUM(gp) AS total_games_played,
    AVG(pts) AS average_points,
    AVG(reb) AS average_rebounds,
    AVG(ast) AS average_assists
FROM {{ source('public', 'nba_players') }}
GROUP BY season
ORDER BY season

