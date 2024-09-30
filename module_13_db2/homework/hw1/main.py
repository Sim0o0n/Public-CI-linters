import sqlite3


def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str
) -> bool:
    query ="""
    SELECT temperature_in_celsius
    FROM table_truck_with_vaccine
    WHERE truck_number = ?
    ORDER BY timestamp;
    """
    cursor.execute(query,(truck_number,))
    temperatures = cursor.fetchall()

    consecutive_violations = 0
    for temp in temperatures:
        if not (-20 <= temp[0] <= -16):
            consecutive_violations += 1
        else:
            consecutive_violations = 0

        if consecutive_violations >= 3:
            return True

    return False
if __name__ == '__main__':
    truck_number: str = input('Введите номер грузовика: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        print('Испортилась' if spoiled else 'Не испортилась')
        conn.commit()
