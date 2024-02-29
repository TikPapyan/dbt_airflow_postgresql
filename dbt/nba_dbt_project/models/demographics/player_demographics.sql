SELECT
    season,
    AVG(age) AS average_age,
    AVG("player height") AS average_height,
    AVG(CAST("player weight" AS numeric)) AS average_weight
FROM {{ source('public', 'nba_players') }}
GROUP BY season
ORDER BY season
