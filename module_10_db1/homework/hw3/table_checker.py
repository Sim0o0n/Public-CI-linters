import sqlite3

def analyze_tables(cursor):
    for table in ['table_1', 'table_2', 'table_3']:
        cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
        count = cursor.fetchone()[0]
        print(f'Количество записей в {table}: {count}')

    cursor.execute("""
        SELECT value 
        FROM `table_1` 
        GROUP BY value 
        HAVING COUNT(*) = 1
    """)
    unique_records = cursor.fetchall()
    unique_count = len(unique_records)

    print(f'Уникальные записи в table_1: {unique_count if unique_count else 0}')

    if unique_count > 0:
        print('Уникальная запись:', unique_records[0][0])

    cursor.execute("""
        SELECT COUNT(*) 
        FROM `table_1` 
        WHERE value IN (SELECT value FROM `table_2`)
    """)
    task3_count = cursor.fetchone()[0]
    print(f'Записи из table_1, которые встречаются в table_2: {task3_count}')

    cursor.execute("""
        SELECT COUNT(*) 
        FROM `table_1` 
        WHERE value IN (SELECT value FROM `table_2`) 
        AND value IN (SELECT value FROM `table_3`)
    """)
    task4_count = cursor.fetchone()[0]
    print(f'Записи из table_1, которые встречаются и в table_2, и в table_3: {task4_count}')

with sqlite3.connect("hw_3_database.db") as conn:
    cursor = conn.cursor()
    analyze_tables(cursor)
