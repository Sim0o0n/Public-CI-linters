import sqlite3


def ivan_sovin_the_most_effective(
        cursor: sqlite3.Cursor,
        name: str,
) -> None:
    query = """
    SELECT salary
    FROM table_effective_manager
    WHERE name = ? ;
    """
    cursor.execute(query, (name,))
    result = cursor.fetchone()

    query_first_salary = """
        SELECT salary
        FROM table_effective_manager
        ORDER BY id LIMIT 1;
        """
    cursor.execute(query_first_salary)
    first_salary_result = cursor.fetchone()
    first_salary = first_salary_result[0]

    if result is None:
        print(f"Сотрудник - {name} не найден")
        return

    current_salary = result[0]

    if current_salary >  first_salary:
        cursor.execute("DELETE FROM table_effective_manager WHERE name = ?", (name,))

    else:
        new_salary = round(current_salary * 1.1)
        cursor.execute("UPDATE table_effective_manager SET salary = ? WHERE name = ?", (new_salary, name))



if __name__ == '__main__':
    name: str = input('Введите имя сотрудника: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        ivan_sovin_the_most_effective(cursor, name)
        conn.commit()
