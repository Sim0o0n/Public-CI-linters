from sqlalchemy.sql.functions import func
from datetime import datetime
from sqlalchemy import create_engine, event, extract
from sqlalchemy.orm import sessionmaker
import csv
from io import StringIO
from flask import Flask, request, jsonify
from sqlalchemy.exc import IntegrityError
import re
from orm_model_2 import Book, Author, Students, Receivingbooks

app = Flask(__name__)
engine = create_engine("sqlite:///python.db")
Session = sessionmaker(bind=engine)

# получить кол-во оставшихся в библиотеке книг по автору (GET -входной параметр - ID автора)
@app.route('/book/author/<int:author_id>', methods=['GET'])
def get_books_by_id(author_id):
    session_get = Session()
    books = session_get.query(Book).filter_by(author_id=author_id).all()
    books_count = sum(book.count for book in books)
    session_get.close()
    return jsonify({
        "author_id": author_id,
        "books": books_count
    })

# получить список книг, которые студент не читал,при этом другие книги этого автора студент уже брал (GET - входной параметр - ID студента).
@app.route("/book/not_read/<int:student_id>", methods=["GET"])
def get_books_not_read(student_id):
    session_get_2 = Session()
    get_students_books = session_get_2.query(Receivingbooks).filter_by(student_id=student_id).all()
    authors = set()

    for record in get_students_books:
        book = session_get_2.query(Book).filter_by(id=record.book_id).first()
        if book:
            authors.add(book.author_id)

    books_not_read = []
    for author_id in authors:
        books_by_author = session_get_2.query(Book).filter_by(author_id=author_id).all()
        for book in books_by_author:
            if not session_get_2.query(Receivingbooks).filter_by(student_id=student_id, book_id=book.id).first():
                books_not_read.append(book)

    session_get_2.close()

    return jsonify({
        "student_id": student_id,
        "books_not_read": [{"id": book.id, "name": book.name, "author_id": book.author_id} for book in books_not_read]
    })

# получить среднее кол-во книг, которые студенты брали в этом месяце (GET)
@app.route("/book/average_count", methods=["GET"])
def average_count_books():
    session_get_3 = Session()
    book_count_list = []
    current_date_now = datetime.now()
    current_month = current_date_now.month
    current_year = current_date_now.year

    get_total = session_get_3.query(Receivingbooks).all()

    for total in get_total:
        if total.date_of_issue.month == current_month and total.date_of_issue.year == current_year:
            book_count_list.append(total)

    if book_count_list:
        checker_average_number = len(book_count_list) / len(set(record.student_id for record in book_count_list))
    else:
        checker_average_number = 0

    session_get_3.close()

    return jsonify({
        "average_number_book_per_month": checker_average_number
    })

# получить самую популярную книгу среди студентов, у которых средний балл больше 4.0 (GET)
@app.route("/book/popular", methods=["GET"])
def get_most_popular_book():
    session_get_4 = Session()
    students_with_high_grades = session_get_4.query(Students).filter(Students.average_score > 4.0).all()

    popular_book = []
    for student in students_with_high_grades:
        books_borrowed = session_get_4.query(Receivingbooks).filter_by(student_id=student.id).all()
        for book in books_borrowed:
            popular_book.append(book.book_id)

    book_counts = {}
    for book_id in popular_book:
        if book_id in book_counts:
            book_counts[book_id] += 1
        else:
            book_counts[book_id] = 1
    most_popular_book_id = max(book_counts, key=book_counts.get)
    most_popular_book = session_get_4.query(Book).filter_by(id=most_popular_book_id).first()

    session_get_4.close()

    if most_popular_book:
        return jsonify({
            "most_popular_book": {
                "id": most_popular_book.id,
                "name": most_popular_book.name,
                "author_id": most_popular_book.author_id
            }
        })
    else:
        return jsonify({"message": "No popular book found"})

# получить ТОП-10 самых читающих студентов в этом году (GET)
@app.route("/students/top_readers", methods=["GET"])
def get_top_10_readers():
    session_get_5 = Session()
    current_year = datetime.now().year

    results = session_get_5.query(
        Receivingbooks.student_id,
        func.count(Receivingbooks.book_id).label('book_count')
    ).filter(
        extract('year', Receivingbooks.date_of_issue) == current_year
    ).group_by(Receivingbooks.student_id).order_by(func.count(Receivingbooks.book_id).desc()).limit(10).all()

    top_students_info = []
    for student_id, book_count in results:
        student = session_get_5.query(Students).filter_by(id=student_id).first()
        if student:
            top_students_info.append({
                "student_id": student.id,
                "name": student.name,
                "book_count": book_count
            })

    session_get_5.close()

    return jsonify({
        "top_10_readers": top_students_info
    })

#Создайте роут, который будет принимать csv-файл с данными по студентам (разделитель ;). Используя csv.DictReader.
@app.route("/upload_students", methods=["POST"])
def upload_students():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided"}), 400

    try:
        file_content = file.stream.read().decode("utf-8")
        csv_reader = csv.DictReader(StringIO(file_content), delimiter=";")

        students_data = []
        for row in csv_reader:
            student = Students(
                name=row["name"],
                surname=row["surname"],
                phone=row["phone"],
                email=row["email"],
                average_score=float(row["average_score"]),
                scholarship=row["scholarship"].lower() == 'true'
            )
            students_data.append(student)

        session = Session()
        session.bulk_save_objects(students_data)
        session.commit()

        return jsonify({"message": "Students data successfully uploaded and inserted."}), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Создайте триггер на событие перед вставкой в таблицу students.
# Триггер должен проверять, что номер телефона имеет формат +7(9**) -*** - ** - **, где * - цифра от 0 до 9.
def check_phone_format(mapper, connection, target):
    phone = target.phone
    phone_regex = r'^\+7\(9[0-9]{2}\) \d{3}-\d{2}-\d{2}$'
    if not re.match(phone_regex, phone):
        raise IntegrityError('Invalid phone format. Expected format: +7(9**) ***-**-**')

event.listen(Students, 'before_insert', check_phone_format)

if __name__ == "__main__":
    app.run(debug=True)
