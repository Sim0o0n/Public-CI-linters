SELECT DISTINCT
    s.name AS flagship_name
FROM
    Ships s
JOIN
    Classes c ON s.class = c.class
WHERE
    s.name = c.class;
