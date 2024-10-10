--Найдите и выведите всю информацию о каждом заказе:
--имя покупателя,
--имя продавца,
--сумму,
--дату.

SELECT
    c.full_name AS customer_name,
    s.full_name AS seller_name,
    o.purchase_amount,
    o.date
FROM
    "order" o
JOIN
    customer c ON o.customer_id = c.customer_id
JOIN
    manager s ON o.manager_id = s.manager_id;