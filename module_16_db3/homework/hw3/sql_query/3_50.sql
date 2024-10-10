SELECT DISTINCT
    b.name AS battle_name,
    b.date AS battle_date
FROM
    Ships s
JOIN
    Outcomes o ON s.name = o.ship
JOIN
    Battles b ON o.battle = b.name
WHERE
    s.class = 'Kongo';
