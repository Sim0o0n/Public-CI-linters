from flask import Flask, jsonify, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from orm_model import Books, Students, ReceivingBooks

app = Flask(__name__)

engine = create_engine("sqlite:///python.db")
Session = sessionmaker(bind=engine)


@app.route('/books', methods=['GET'])
def get_all_books():
    """Получение всех книг в библиотеке"""
    session = Session()
    books = session.query(Books).all()
    session.close()
    return jsonify(
        [{'id': book.id, 'name': book.name, 'count': book.count, 'release_date': book.release_date.isoformat()} for book
         in books])


@app.route('/debtors', methods=['GET'])
def get_debtors():
    """Получение списка должников, держащих книги более 14 дней"""
    session = Session()
    overdue_date = datetime.now() - timedelta(days=14)
    debtors = session.query(ReceivingBooks).filter(
        ReceivingBooks.date_of_return is None,
        ReceivingBooks.date_of_issue < overdue_date
    ).all()
    session.close()
    return jsonify(
        [{'book_id': debt.book_id, 'student_id': debt.student_id, 'date_of_issue': debt.date_of_issue.isoformat()} for
         debt in debtors])


@app.route('/issue_book', methods=['POST'])
def issue_book():
    """Выдача книги студенту """
    data = request.json
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    if not book_id or not student_id:
        return jsonify({"error": "Необходимо передать ID книги и ID студента"}), 400

    session = Session()

    book = session.query(Books).filter_by(id=book_id).first()
    student = session.query(Students).filter_by(id=student_id).first()

    if not book:
        session.close()
        return jsonify({"error": "Книга с таким ID не найдена"}), 404
    if not student:
        session.close()
        return jsonify({"error": "Студент с таким ID не найден"}), 404

    if book.count <= 0:
        session.close()
        return jsonify({"error": "Все экземпляры книги выданы"}), 400

    new_receiving = ReceivingBooks(book_id=book_id, student_id=student_id, date_of_issue=datetime.now())
    book.count -= 1
    session.add(new_receiving)
    session.commit()

    session.close()
    return jsonify({'message': 'Книга успешно выдана студенту'}), 200


@app.route('/return_book', methods=['POST'])
def return_book():
    """Сдача книги в библиотеку"""
    data = request.json
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    if not book_id or not student_id:
        return jsonify({"error": "Необходимо передать ID книги и ID студента"}), 400

    session = Session()

    receiving_record = session.query(ReceivingBooks).filter_by(book_id=book_id, student_id=student_id,
                                                               date_of_return=None).first()

    if not receiving_record:
        session.close()
        return jsonify({"error": "Такой записи нет"}), 404

    receiving_record.date_of_return = datetime.now()
    book = session.query(Books).filter_by(id=book_id).first()
    book.count += 1
    session.commit()
    session.close()
    return jsonify({'message': 'Книга успешно сдана в библиотеку'}), 200


@app.route('/search_book', methods=['GET'])
def search_book():
    """Поиск книги по названию"""
    query = request.args.get('q', '')
    session = Session()
    books = session.query(Books).filter(Books.name.contains(query)).all()
    session.close()
    return jsonify([{'id': book.id, 'name': book.name} for book in books])


@app.route('/students/scholarship', methods=['GET'])
def students_with_scholarship():
    session = Session()
    students = Students.get_students_with_scholarship(session)
    session.close()
    return jsonify([{"id": student.id, "name": student.name, "surname": student.surname} for student in students])


@app.route('/students/high_score', methods=['GET'])
def students_with_high_score():
    min_score = request.args.get('min_score', type=float)
    if min_score is None:
        return jsonify({"error": "Parameter 'min_score' is required"}), 400

    session = Session()
    students = Students.get_students_with_high_score(session, min_score)
    session.close()
    return jsonify(
        [{"id": student.id, "name": student.name, "surname": student.surname, "average_score": student.average_score}
         for student in students])


if __name__ == "__main__":
    app.run(debug=True)

