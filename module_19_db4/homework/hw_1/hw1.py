import sqlite3


def get_toughest_teacher():
    db_path = '/home/simon/PycharmProjects/python_advanced/module_19_db4/homework.db'

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.full_name AS teacher_name, AVG(g.grade) AS avg_grade
            FROM teachers t
            JOIN assignments a ON t.teacher_id = a.teacher_id
            JOIN assignments_grades g ON a.assisgnment_id = g.assisgnment_id
            GROUP BY t.teacher_id
            ORDER BY avg_grade ASC
            LIMIT 1;
        """)
        result = cursor.fetchone()
        return result if result else "No data found"


if __name__ == '__main__':
    toughest_teacher = get_toughest_teacher()
    print("Преподаватель с самыми сложными заданиями:", toughest_teacher)
