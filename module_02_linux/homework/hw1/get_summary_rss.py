"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""
import os


def get_summary_rss(ps_output_file_path: str) -> str:
    total_rss = 0
    with open(ps_output_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            parts = line.split()
            total_rss += int(parts[5])
    size = total_rss * 1024
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f'{size:.2f} {unit}'
        size /= 1024
    return f"{size:.2f} PB"


if __name__ == '__main__':
    path: str = '/home/simon/output_file.txt'
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
