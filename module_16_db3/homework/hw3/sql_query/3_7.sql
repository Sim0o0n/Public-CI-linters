SELECT
    p.model,
    CASE
        WHEN p.type = 'PC' THEN pc.price
        WHEN p.type = 'Laptop' THEN l.price
        WHEN p.type = 'Printer' THEN pr.price
    END AS price
FROM
    Product p
LEFT JOIN
    PC pc ON p.model = pc.model
LEFT JOIN
    Laptop l ON p.model = l.model
LEFT JOIN
    Printer pr ON p.model = pr.model
WHERE
    p.maker = 'B';