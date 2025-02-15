from sqlalchemy import (create_engine, Column, Integer, String, Date, Float, Boolean, DateTime, func)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime


engine = create_engine("sqlite:///python.db")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Books(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)

class Authors(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    schoolarship = Column(Boolean, nullable=False)

    @classmethod
    def get_students_with_scholarship(cls, session: Session):
        """получение списка студентов, которые имеют общежитие"""
        return session.query(cls).filter(cls.schoolarship == True).all()

    @classmethod
    def get_students_with_high_score(cls, session: Session, min_score: float):
        """получение списка студентов, у которых средний балл выше балла, который будет передан входным параметров в функцию """
        return session.query(cls).filter(cls.average_score > min_score).all()

class ReceivingBooks(Base):
    __tablename__ = "receiving_books"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime, nullable=True)

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return:
            return (self.date_of_return - self.date_of_issue).days
        else:
            return (datetime.now() - self.date_of_issue).days

    @count_date_with_book.expression
    def count_date_with_book(cls):
        return func.julianday(func.ifnull(cls.date_of_return, func.now())) - func.julianday(cls.date_of_issue)


if __name__ == "__main__":
    Base.metadata.create_all(engine)



