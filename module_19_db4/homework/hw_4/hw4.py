import sqlite3


def get_late_assignments_statistics():
    with sqlite3.connect('/home/simon/PycharmProjects/python_advanced/module_19_db4/homework.db') as conn:
        cursor = conn.cursor()

        query = """
        SELECT 
            sg.group_id,
            AVG(late_assignments.late_count) AS avg_late,
            MAX(late_assignments.late_count) AS max_late,
            MIN(late_assignments.late_count) AS min_late
        FROM students_groups sg
        JOIN (
            SELECT 
                s.group_id,
                COUNT(*) AS late_count
            FROM assignments a
            JOIN assignments_grades g ON a.assisgnment_id = g.assisgnment_id
            JOIN students s ON g.student_id = s.student_id
            WHERE g.date > a.due_date
            GROUP BY s.group_id
        ) AS late_assignments ON sg.group_id = late_assignments.group_id
        GROUP BY sg.group_id;
        """

        cursor.execute(query)

        results = cursor.fetchall()

        for group_id, avg_late, max_late, min_late in results:
            print(f"Group ID: {group_id}, Average Late: {avg_late}, Max Late: {max_late}, Min Late: {min_late}")


get_late_assignments_statistics()
