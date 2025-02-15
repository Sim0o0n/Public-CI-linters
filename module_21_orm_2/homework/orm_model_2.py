from sqlalchemy import (
    create_engine, Column, Integer, String, Date,
    Float, Boolean, DateTime, ForeignKey
)
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from sqlalchemy.orm import declarative_base

# Создание сессии
engine = create_engine("sqlite:///python.db")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# таблица книг
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, nullable=False)
    release_date = Column(Date, nullable=False)
    key_author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", back_populates="books")
    receiving_books = relationship("Receivingbooks", back_populates="book")

#таблица авторов
class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    books = relationship("Book", back_populates="author", cascade="all, delete")

#таблица студентов
class Students(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    receiving_books = relationship("Receivingbooks", back_populates="student")

#таблица получения/возврата книг
class Receivingbooks(Base):
    __tablename__ = 'receiving_books'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="receiving_books")
    student = relationship("Students", back_populates="receiving_books")


if __name__ == "__main__":

    Base.metadata.drop_all(engine)  # Для тестирования (очистка bdшек)
    Base.metadata.create_all(engine)

# Пример для заполнения таблиц (для тестов приложения)

    # Создание авторов
    authors = [
        Author(name="Лев", surname="Толстой"),
        Author(name="Александр", surname="Пушкин"),
        Author(name="Фёдор", surname="Достоевский"),
    ]
    session.add_all(authors)
    session.commit()

    # Создание книг
    books = [
        Book(name="Война и мир", count=10, release_date=datetime(1869, 1, 1), key_author_id=authors[0].id),
        Book(name="Евгений Онегин", count=15, release_date=datetime(1833, 1, 1), key_author_id=authors[1].id),
        Book(name="Преступление и наказание", count=20, release_date=datetime(1866, 1, 1), key_author_id=authors[2].id),
    ]
    session.add_all(books)
    session.commit()

    # Создание студентов
    students = [
        Students(
            name="Иван", surname="Иванов", phone="+7(900) 123-45-67",
            email="ivan.ivanov@example.com", average_score=4.5, scholarship=True
        ),
        Students(
            name="Петр", surname="Петров", phone="+7(900) 234-56-78",
            email="petr.petrov@example.com", average_score=4.2, scholarship=False
        ),
        Students(
            name="Анна", surname="Антонова", phone="+7(900) 345-67-89",
            email="anna.antonova@example.com", average_score=4.8, scholarship=True
        ),
    ]
    session.add_all(students)
    session.commit()

    # Создание записей о получении книг
    receiving_books = [
        Receivingbooks(book_id=books[0].id, student_id=students[0].id, date_of_issue=datetime(2024, 11, 1)),
        Receivingbooks(book_id=books[1].id, student_id=students[1].id, date_of_issue=datetime(2024, 11, 2)),
        Receivingbooks(book_id=books[2].id, student_id=students[2].id, date_of_issue=datetime(2024, 11, 3)),
        Receivingbooks(book_id=books[0].id, student_id=students[1].id, date_of_issue=datetime(2024, 11, 4)),
    ]
    session.add_all(receiving_books)
    session.commit()

    print("Данные успешно добавлены")


