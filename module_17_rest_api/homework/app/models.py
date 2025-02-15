from sqlite3 import connect
from dataclasses import dataclass
from typing import Optional, List, Dict

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'

@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None

@dataclass
class Book:
    title: str
    author_id: int
    id: Optional[int] = None

def init_db(initial_records: List[Dict], initial_authors: List[Dict]) -> None:
    with connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS `{AUTHORS_TABLE_NAME}`(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                middle_name TEXT
            );
        """)
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS `{BOOKS_TABLE_NAME}`(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author_id INTEGER,
                FOREIGN KEY(author_id) REFERENCES {AUTHORS_TABLE_NAME}(id) ON DELETE CASCADE
            );
        """)
        cursor.executemany(f"""
            INSERT INTO `{AUTHORS_TABLE_NAME}` (first_name, last_name, middle_name)
            VALUES (?, ?, ?)
        """, [(author['first_name'], author['last_name'], author.get('middle_name')) for author in initial_authors])
        cursor.executemany(f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` (title, author_id)
            VALUES (?, ?)
        """, [(book['title'], book['author_id']) for book in initial_records])

def get_all_books() -> List[Book]:
    with connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        return [Book(id=row[0], title=row[1], author_id=row[2]) for row in cursor.fetchall()]

def add_book(book: Book) -> Book:
    with connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` (title, author_id) 
            VALUES (?, ?)
        """, (book.title, book.author_id))
        book.id = cursor.lastrowid
        return book

def get_book_by_id(book_id: int) -> Optional[Book]:
    with connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        return Book(id=row[0], title=row[1], author_id=row[2]) if row else None

def update_book_by_id(book_id: int, new_title: str, author_id: int) -> Optional[Book]:
    with connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE `{BOOKS_TABLE_NAME}` SET title = ?, author_id = ? WHERE id = ?",
                       (new_title, author_id, book_id))
        conn.commit()
        return get_book_by_id(book_id)

def delete_book_by_id(book_id: int) -> None:
    with connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM `{BOOKS_TABLE_NAME}` WHERE id = ?", (book_id,))
        conn.commit()

def add_author(first_name: str, last_name: str, middle_name: Optional[str] = None) -> Author:
    with connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO `{AUTHORS_TABLE_NAME}` (first_name, last_name, middle_name)
            VALUES (?, ?, ?)
        """, (first_name, last_name, middle_name))
        return Author(id=cursor.lastrowid, first_name=first_name, last_name=last_name, middle_name=middle_name)

def get_author_by_id(author_id: int) -> Optional[Author]:
    with connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `{AUTHORS_TABLE_NAME}` WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        return Author(id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3]) if row else None

def delete_author_by_id(author_id: int) -> None:
    with connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM `{AUTHORS_TABLE_NAME}` WHERE id = ?", (author_id,))
        conn.commit()

def get_books_by_author_id(author_id: int) -> List[Book]:
    with connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE author_id = ?", (author_id,))
        return [Book(id=row[0], title=row[1], author_id=row[2]) for row in cursor.fetchall()]
