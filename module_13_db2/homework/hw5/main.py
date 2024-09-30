import sqlite3
import random


def generate_test_data(cursor: sqlite3.Cursor, number_of_groups: int) -> None:
    strong_teams = [f"Strong Team {i + 1}" for i in range(number_of_groups)]
    medium_teams = [f"Medium Team {i + 1}" for i in range(number_of_groups * 2)]
    weak_teams = [f"Weak Team {i + 1}" for i in range(number_of_groups)]

    command_numbers = list(range(1, number_of_groups * 4 + 1))
    commands_data = []

    commands_data.extend((command_number, strong_teams[i], f"Country {i + 1}", 'strong') for i, command_number in
                         enumerate(command_numbers[:number_of_groups]))
    commands_data.extend(
        (command_number, medium_teams[i], f"Country {random.randint(1, number_of_groups)}", 'medium') for
        i, command_number in enumerate(command_numbers[number_of_groups:number_of_groups * 3]))
    commands_data.extend((command_number, weak_teams[i], f"Country {i + 1}", 'weak') for i, command_number in
                         enumerate(command_numbers[number_of_groups * 3:]))

    cursor.executemany(
        "INSERT INTO uefa_commands (command_number, command_name, command_country, command_level) VALUES (?, ?, ?, ?)",
        commands_data
    )

    draw_data = [
        (i + 1, group_number)
        for group_number in range(1, number_of_groups + 1)
        for i in [group_number - 1,
                  number_of_groups + (group_number - 1) * 2,
                  number_of_groups + (group_number - 1) * 2 + 1,
                  number_of_groups * 3 + group_number - 1]
    ]

    cursor.executemany(
        "INSERT INTO uefa_draw (command_number, group_number) VALUES (?, ?)",
        draw_data
    )


if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute("DELETE FROM uefa_commands")
        cursor.execute("DELETE FROM uefa_draw")

        generate_test_data(cursor, number_of_groups)

