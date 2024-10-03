import sqlite3
from typing import Any, Optional, List

DATA: List[dict] = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 2, 'title': 'War and Peace', 'author': 'Leo Tolstoy'},
]


class Book:
    def __init__(self, id: int, title: str, author: str, view_count: int) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.view_count: int = view_count

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_books'; 
            """
        )
        exists: Optional[tuple[str]] = cursor.fetchone()

        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `table_books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, 
                    author TEXT, 
                    view_count INTEGER DEFAULT 0
                )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `table_books` (title, author) VALUES (?, ?)
                """,
                [
                    (item['title'], item['author'])
                    for item in initial_records
                ]
            )
        else:
            pass


def get_all_books() -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("SELECT * FROM `table_books`")
        return [Book(*row) for row in cursor.fetchall()]

