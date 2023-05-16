-- Feature 1
-- Get all repositories and display
SELECT name, owner FROM Repository;

-- Test for Flask
CREATE INDEX language_index on File (language);

-- Get summary data for each repository
SELECT COUNT(*) FROM File
WHERE repo_name = 'zerorpc-python'
AND owner = '0rpc'
AND language = 'python';

SELECT COUNT(*) FROM Issue
WHERE repo_name = 'zerorpc-python'
AND owner = '0rpc'
AND path IN (
    SELECT path FROM File
    WHERE repo_name = 'zerorpc-python'
    AND owner = '0rpc'
);

SELECT COUNT(*) FROM User
WHERE name = '0rpc';

SELECT COUNT(*) FROM Organization
WHERE name = '0rpc';

-- Feature 2
SELECT repo_name, owner, num_issues
FROM (SELECT repo_name,
             Issue.owner,
             count(*) as num_issues,
             rank() over ( ORDER BY count(*) DESC ) as issue_rank
     FROM Repository
        LEFT JOIN Issue
               ON Repository.name = Issue.repo_name AND Repository.owner = Issue.owner
    GROUP BY Issue.repo_name, Issue.owner
    ) AS repo_issues
WHERE issue_rank <= 10
LIMIT 10;

-- Feature 3
INSERT INTO Owner (name) VALUES ('Some_Owner');
INSERT INTO User (name) VALUES ('Some_Owner');
INSERT INTO Repository (name, owner) VALUES ('Some_Repo', 'Some_Owner');
INSERT INTO File (name, language, path, repo_name, owner) VALUES ('hi.py', 'python', '/hi.py', 'Some_Repo', 'Some_Owner');
INSERT INTO Issue (check_id, start_line, end_line, category, impact, repo_name, owner, path) VALUES ('python.lang.security', '2', '5', 'lang', 'low', 'Some_Repo', 'Some_Owner', '/hi.py');


-- Feature 4
-- Calculate impact of each repo
DROP FUNCTION IF EXISTS QuantifyImpact;
DELIMITER //
CREATE FUNCTION QuantifyImpact( impact VARCHAR(255) )
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE res INT;
    IF UPPER(impact) = 'LOW' THEN SET res = 1;
    ELSEIF UPPER(impact) = 'MEDIUM' THEN SET res = 3;
    ELSE SET res = 5;
    END IF;
    RETURN res;
END //
DELIMITER ;

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
From (
    SELECT R.name AS repo_name, R.owner, R.stars, count(I.id) AS tot_issues, MAX(I.impact) AS max_impact, AVG(I.impact) AS avg_impact
    FROM Repository AS R
        JOIN (
            SELECT id, repo_name, owner, QuantifyImpact(impact) as impact
            FROM Issue
        ) AS I ON R.name = I.repo_name AND R.owner = I.owner
    GROUP BY R.name, R.owner, R.stars
) AS Repo_stat
LIMIT 10;

-- Feature 5
UPDATE Repository SET stars = 122 WHERE name = 'zerorpc-python' AND owner = '0rpc';
UPDATE Owner SET followers = 250 WHERE name = '0rpc';
UPDATE User SET following = 265 WHERE name = '0rpc';

-- Feature 6
-- Find repos with below average performance
WITH repo_impact as (
    SELECT * FROM (
        SELECT R2.name, R2.owner, SUM(I.impact) as ovr_impact FROM Respository as R2
        JOIN (
            SELECT repo_name, owner, QuantiyfyImpact(impact) as impact FROM Issue
        ) as I ON R2.name = I.repo_name and R2.owner = I.owner
        GROUP BY R2.name, R2.owner
    ) as R
)

SELECT * FROM repo_impact
WHERE ovr_impact > (
    SELECT AVG(ovr_impact) FROM repo_impact
) LIMIT 10 OFFSET 2;