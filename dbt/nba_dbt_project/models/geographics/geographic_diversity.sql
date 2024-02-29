SELECT
    country,
    COUNT(DISTINCT "player name") AS number_of_players,
    MIN("draft year") AS first_draft_year
FROM {{ source('public', 'nba_players') }}
GROUP BY country
ORDER BY number_of_players DESC

