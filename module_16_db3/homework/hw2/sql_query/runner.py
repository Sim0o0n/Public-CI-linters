import sqlite3

db_path = '/home/simon/PycharmProjects/python_advanced/module_16_db3/homework/hw.db'

def execute_query(file_name):
    with open(file_name, 'r') as sql_file:
        sql_script: str = sql_file.read()

    with sqlite3.connect(db_path) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()

execute_query('2_1.sql')  # Запрос 1
execute_query('2_2.sql')  # Запрос 2
execute_query('2_3.sql')  # Запрос 3
execute_query('2_4.sql')  # Запрос 4
execute_query('2_5.sql')  # Запрос 5
