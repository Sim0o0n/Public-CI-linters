"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys


def get_mean_size(ls_output: str) -> float:
    lines = ls_output.strip().split('\n')

    if lines and lines[0].startswith('total'):
        lines = lines[1:]

    sizes = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 5:
            try:
                size = int(parts[4])
                sizes.append(size)
            except ValueError:
                continue

    if sizes:
        return sum(sizes) / len(sizes)
    else:
        return 0.0


if __name__ == '__main__':
    try:
        data = sys.stdin.read()
        mean_size = get_mean_size(data)
        print(mean_size)
    except KeyboardInterrupt:
        print("Process was interrupted.")

