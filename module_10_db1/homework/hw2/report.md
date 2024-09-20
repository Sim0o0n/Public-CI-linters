# Исследование продаж телефонов


## Отчёт по продажам:

1. **Телефоны какого цвета чаще всего покупают?**

   Цвет телефона, который покупают чаще всего: `синий` с `500` покупками.

   Запрос:
   ```sql
   SELECT colour, COUNT(*) AS most_popular_colour
    FROM table_checkout
    JOIN table_phones ON table_checkout.phone_id = table_phones.id
    GROUP BY colour
    ORDER BY most_popular_colour DESC
    LIMIT 1;
    ```
   
2. **Какие телефоны чаще покупают: красные или синие?**

   `Синий` приобрели `500` раз, а `красный` - `429`, соотвественно - `синий` является наиболее популярным.

   Запрос:
   ```sql
    SELECT colour, COUNT(*) AS comparison
    FROM table_checkout
    JOIN table_phones ON table_checkout.phone_id = table_phones.id
    WHERE colour IN ('красный', 'синий')
    GROUP BY colour
    ORDER BY comparison DESC;
    ```
   

3. **Какой самый непопулярный цвет телефона?**

   Цвет телефона, который покупают реже всего: `золотой`, всего - `28` покупок.

   Запрос:
   ```sql
   SELECT colour, COUNT(*) AS outsider
    FROM table_checkout
    JOIN table_phones ON table_checkout.phone_id = table_phones.id
    GROUP BY colour
    ORDER BY outsider ASC
    LIMIT 1;

  
Всего было проанализированно 1000 покупок.
```sql
    SELECT COUNT(*) FROM table_checkout;