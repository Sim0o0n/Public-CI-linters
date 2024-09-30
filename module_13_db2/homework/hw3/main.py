import datetime
import sqlite3


def create_table(cursor: sqlite3.Cursor) -> None:
    create_table_query = """
    CREATE TABLE IF NOT EXISTS birds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date_time TEXT NOT NULL
    );
    """
    cursor.execute(create_table_query)


def log_bird(
        cursor: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
) -> None:
    if not check_if_such_bird_already_seen(cursor, bird_name):
        insert_query = """
            INSERT INTO birds (name, date_time)
            VALUES (?, ?);
        """
        cursor.execute(insert_query, (bird_name, date_time))


def check_if_such_bird_already_seen(
        cursor: sqlite3.Cursor,
        bird_name: str
) -> bool:
    check_query = """
        SELECT EXISTS (
            SELECT 1 FROM birds WHERE name = ?
        );
    """
    cursor.execute(check_query, (bird_name,))
    exists = cursor.fetchone()[0]
    return bool(exists)


if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        create_table(cursor)

        print("Программа помощи ЮНатам v0.1")
        name: str = input("Пожалуйста введите имя птицы\n> ")
        count_str: str = input("Сколько птиц вы увидели?\n> ")
        count: int = int(count_str)
        right_now: str = datetime.datetime.utcnow().isoformat()

        log_bird(cursor, name, right_now)

        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")
