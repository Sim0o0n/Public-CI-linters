import sqlite3

# Задание со звездочкой


def get_students_of_easiest_teacher_with_join():
    db_path = '/home/simon/PycharmProjects/python_advanced/module_19_db4/homework.db'

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.full_name AS student_name
            FROM students s
            JOIN students_groups sg ON s.group_id = sg.group_id
            JOIN teachers t ON sg.teacher_id = t.teacher_id
            JOIN assignments a ON t.teacher_id = a.teacher_id
            JOIN assignments_grades g ON a.assisgnment_id = g.assisgnment_id
            WHERE t.teacher_id = (
                SELECT t2.teacher_id
                FROM teachers t2
                JOIN assignments a2 ON t2.teacher_id = a2.teacher_id
                JOIN assignments_grades g2 ON a2.assisgnment_id = g2.assisgnment_id
                GROUP BY t2.teacher_id
                ORDER BY AVG(g2.grade) DESC
                LIMIT 1
            )
            GROUP BY s.student_id;
        """)
        results = cursor.fetchall()
        return results if results else "No data found"

if __name__ == '__main__':
    students_with_join = get_students_of_easiest_teacher_with_join()
    print("Студенты у преподавателя, задающего самые простые задания:")
    for student in students_with_join:
        print(student[0])
