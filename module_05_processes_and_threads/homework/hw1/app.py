"""
Консольная утилита lsof (List Open Files) выводит информацию о том, какие файлы используют какие-либо процессы.
Эта команда может рассказать много интересного, так как в Unix-подобных системах всё является файлом.

Но нам пока нужна лишь одна из её возможностей.
Запуск lsof -i :port выдаст список процессов, занимающих введённый порт.
Например, lsof -i :5000.

Как мы с вами выяснили, наш сервер отказывается запускаться, если кто-то занял его порт. Напишите функцию,
которая на вход принимает порт и запускает по нему сервер. Если порт будет занят,
она должна найти процесс по этому порту, завершить его и попытаться запустить сервер ещё раз.
"""
import os
import signal
from typing import List
import subprocess
from flask import Flask

app = Flask(__name__)


def get_pids(port: int) -> List[int]:
    """
    Возвращает список PID процессов, занимающих переданный порт
    @param port: порт
    @return: список PID процессов, занимающих порт
    """
    if not isinstance(port, int):
        raise ValueError

    pids: List[int] = []
    try:
        result = subprocess.check_output(["lsof", "-i", f":{port}"])
        lines = result.decode().splitlines()

        for line in lines[1:]:
            parts = line.split()
            pids.append(int(parts[1]))

    except subprocess.CalledProcessError:
        pass
    return pids


def free_port(port: int) -> None:
    """
    Завершает процессы, занимающие переданный порт
    @param port: порт
    """
    pids: List[int] = get_pids(port)
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"Процесс с PID {pid} завершен")
        except OSError as e:
            print(f"Ошибка при завершении процесса с PID {pid}: {e}")


def run(port: int) -> None:
    """
    Запускает flask-приложение по переданному порту.
    Если порт занят каким-либо процессом, завершает его.
    @param port: порт
    """
    free_port(port)
    app.run(port=port)
    try:
        app.run(port=port)
    except OSError as e:
        print(f"Ошибка при запуске сервера: {e}")


if __name__ == '__main__':
    run(5000)
