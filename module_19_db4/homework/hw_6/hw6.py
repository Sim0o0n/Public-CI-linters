import sqlite3


def get_average_reading_assignment_grade():
    database_path = '/home/simon/PycharmProjects/python_advanced/module_19_db4/homework.db'

    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()

        query = """
        SELECT AVG(grade) AS average_grade
        FROM assignments_grades
        WHERE assisgnment_id IN (
            SELECT assisgnment_id 
            FROM assignments 
            WHERE assignment_text LIKE '%прочитать%' OR assignment_text LIKE '%выучить%'
        )
        """

        cursor.execute(query)

        average_grade = cursor.fetchone()[0]

        if average_grade is not None:
            print(f'Средняя оценка заданий, где нужно было что-то прочитать или выучить: {average_grade:.2f}')
        else:
            print('Нет данных.')


if __name__ == '__main__':
    get_average_reading_assignment_grade()

