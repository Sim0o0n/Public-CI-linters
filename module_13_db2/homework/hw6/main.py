import sqlite3


def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    sports = {
        0: "football",    # понедельник
        1: "hockey",      # вторник
        2: "chess",       # среда
        3: "SUP surfing",  # четверг
        4: "boxing",      # пятница
        5: "Dota2",       # суббота
        6: "chess-boxing"  # воскресенье
    }

    cursor.execute("DELETE FROM table_friendship_schedule")

    for day in range(366):
        training_day = day % 7
        employees_for_day = []

        for employee_id in range(1, 367):
            if (training_day == 2 and employee_id % 6 == 0) or (training_day == 4 and employee_id % 5 == 0):
                continue
            employees_for_day.append(employee_id)

        if len(employees_for_day) >= 10:
            working_employees = employees_for_day[:10]
            for emp_id in working_employees:
                cursor.execute("INSERT INTO table_friendship_schedule (employee_id, date) VALUES (?, ?)", (emp_id, day))


if __name__ == '__main__':
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        update_work_schedule(cursor)
        conn.commit()
