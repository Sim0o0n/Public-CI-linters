SELECT DISTINCT
    p.maker
FROM
    Product p
JOIN
    PC pc ON p.model = pc.model
WHERE
    pc.speed >= 450 AND p.type = 'PC';
