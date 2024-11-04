import sqlite3


def get_top_students():
    db_path = '/home/simon/PycharmProjects/python_advanced/module_19_db4/homework.db'

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.full_name AS student_name, AVG(g.grade) AS avg_grade
            FROM students s
            JOIN assignments_grades g ON s.student_id = g.student_id
            GROUP BY s.student_id
            ORDER BY avg_grade DESC
            LIMIT 10;
        """)
        results = cursor.fetchall()
        return results if results else "No data found"


if __name__ == '__main__':
    top_students = get_top_students()
    print("Топ 10 студентов с лучшими средними оценками:")
    for student in top_students:
        print(f"Студент: {student[0]}, Средняя оценка: {student[1]:.2f}")