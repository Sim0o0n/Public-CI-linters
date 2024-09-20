import sqlite3

def analyze_income(cursor):
    # task1.
    cursor.execute("SELECT COUNT(*) FROM salaries WHERE salary < 5000")
    below_poverty_count = cursor.fetchone()[0]
    print(f'Количество человек за чертой бедности: {below_poverty_count}')

    # task2.
    cursor.execute("SELECT AVG(salary) FROM salaries")
    average_salary = cursor.fetchone()[0]
    print(f'Средняя зарплата: {average_salary:.2f}')

    # task3.
    cursor.execute("""
        SELECT salary FROM salaries
        ORDER BY salary
        LIMIT 1 OFFSET (SELECT COUNT(*) FROM salaries) / 2
    """)
    median_salary = cursor.fetchone()[0]
    print(f'Медианная зарплата: {median_salary:.2f}')

    # task4.
    cursor.execute("""
        SELECT 
            ROUND(100.0 * SUM(CASE WHEN rank <= 0.1 * total THEN salary ELSE 0 END) / 
            NULLIF(SUM(salary), 0), 2) AS inequality
        FROM (
            SELECT salary, 
                   ROW_NUMBER() OVER (ORDER BY salary DESC) AS rank, 
                   (SELECT COUNT(*) FROM salaries) AS total
            FROM salaries
        )
    """)
    inequality_percentage = cursor.fetchone()[0]
    print(f'Социальное неравенство F: {inequality_percentage:.2f}%')

with sqlite3.connect("hw_4_database.db") as conn:
    cursor = conn.cursor()
    analyze_income(cursor)
