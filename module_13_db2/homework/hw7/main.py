import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO table_users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()


def hack() -> None:
    username: str = "'; SELECT * FROM table_users; --"
    password: str = "password"

    register(username, password)

    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM table_users")
        rows = cursor.fetchall()

        with open('stolen_data.txt', 'w') as f:
            for row in rows:
                f.write(f"ID: {row[0]}, Username: {row[1]}, Password: {row[2]}\n")

        cursor.execute("UPDATE table_users SET username = 'joke', password = 'joke'")
        conn.commit()


if __name__ == '__main__':
    register('wignorbo', 'sjkadnkjasdnui31jkdwq')
    hack()
