SELECT
    p.maker,
    l.speed
FROM
    Product p
JOIN
    Laptop l ON p.model = l.model
WHERE
    l.hd >= 10;