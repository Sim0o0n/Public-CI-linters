--Выведите номер заказа, имена продавца и покупателя, если место жительства продавца и покупателя не совпадают.

SELECT
    o.order_no,
    s.full_name AS seller_name,
    c.full_name AS customer_name
FROM
    "order" o
JOIN
    customer c ON o.customer_id = c.customer_id
JOIN
    manager s ON o.manager_id = s.manager_id
WHERE
    c.city <> s.city;
