import sqlite3

def get_group_statistics():
    with sqlite3.connect('/home/simon/PycharmProjects/python_advanced/module_19_db4/homework.db') as conn:
        cursor = conn.cursor()

        query = """
        SELECT 
            sg.group_id,
            COUNT(s.student_id) AS total_students,
            AVG(g.grade) AS average_grade,
            SUM(CASE WHEN g.grade = 0 THEN 1 ELSE 0 END) AS not_submitted,
            SUM(CASE WHEN g.date > a.due_date THEN 1 ELSE 0 END) AS late_submissions,
            COUNT(DISTINCT g.student_id) - COUNT(DISTINCT g.grade_id) AS retry_attempts
        FROM 
            students_groups sg
        LEFT JOIN 
            students s ON sg.group_id = s.group_id
        LEFT JOIN 
            assignments_grades g ON s.student_id = g.student_id
        LEFT JOIN 
            assignments a ON g.assisgnment_id = a.assisgnment_id
        GROUP BY 
            sg.group_id;
        """

        cursor.execute(query)

        results = cursor.fetchall()

        for group_id, total_students, average_grade, not_submitted, late_submissions, retry_attempts in results:
            print(f"Group ID: {group_id}, Total Students: {total_students}, Average Grade: {round(average_grade,2)}, "
                  f"Not Submitted: {not_submitted}, Late Submissions: {late_submissions}, Retry Attempts: {retry_attempts}")

get_group_statistics()

