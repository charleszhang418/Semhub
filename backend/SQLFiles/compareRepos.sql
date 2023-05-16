-- Calculate impact of each repo
SELECT repo_name,
       owner,
       stars,
       tot_issues,
       max_impact,
       avg_impact,
       CASE -- WHEN stars >= (SELECT AVG(stars) FROM Repository)) THEN 'HIGH'
            WHEN tot_issues > 20 AND max_impact = 5 THEN 'HIGH'
            WHEN avg_impact > 3.6 THEN 'HIGH'
            WHEN avg_impact > 2.4 THEN 'MEDIUM'
            ELSE 'LOW'
        END AS impact
FROM (
    SELECT R.name AS repo_name, R.owner, R.stars, count(I.id) AS tot_issues, MAX(I.impact) AS max_impact, AVG(I.impact) AS avg_impact
    FROM Repository AS R
        JOIN (
            SELECT id, repo_name, owner, QuantifyImpact(impact) AS impact
            FROM Issue
        ) AS I ON R.name = I.repo_name AND R.owner = I.owner
    GROUP BY R.name, R.owner, R.stars
) AS Repo_stat
LIMIT 12
