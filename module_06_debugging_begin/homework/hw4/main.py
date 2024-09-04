"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
import json
from typing import Dict
from collections import Counter

def task1() -> Dict[str, int]:
    """
    1. Сколько было сообщений каждого уровня за сутки.
    @return: словарь вида {уровень: количество}
    """
    with open("skillbox_json_messages.log", 'r') as file:
        log_levels = {
            "DEBUG": 0,
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0
        }
        for line in file:
            log_entry = json.loads(line)
            level = log_entry.get("level", "")
            if level in log_levels:
                log_levels[level] += 1

    return log_levels


def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час
    """
    with open("skillbox_json_messages.log", 'r') as file:
        hourly_logs = {}
        for line in file:
            log_entry = json.loads(line)
            time_str = log_entry.get("time")
            hour = time_str.split(':')[0]
            if hour in hourly_logs:
                hourly_logs[hour] += 1
            else:
                hourly_logs[hour] = 1
    if not hourly_logs:
        return 0
    max_hour = max(hourly_logs, key=hourly_logs.get)
    return int(max_hour)


def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """
    critical_count = 0
    start_time = "05:00:00"
    end_time = "05:20:00"

    with open("skillbox_json_messages.log", 'r') as file:
        for line in file:
            log_entry = json.loads(line)
            time_str = log_entry.get("time")
            level = log_entry.get("level")
            if level == "CRITICAL":
                if start_time <= time_str <= end_time:
                    critical_count += 1

        return critical_count

def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    dog_counter = 0
    with open("skillbox_json_messages.log", 'r') as file:
        for line in file:
            log_entry = json.loads(line)
            message_checker = log_entry.get("message")
            if "dog" in message_checker.lower():
                dog_counter += 1

    return dog_counter



def task5() -> str:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово
    """
    messages_list = []
    words_counter = Counter()
    with open("skillbox_json_messages.log", 'r') as file:
        for line in file:
            log_entry = json.loads(line)
            level = log_entry("level")
            message_checker = log_entry.get("message","")
            if level == "WARNING":
                words = message_checker.split()
                words_counter.update(words)

    common_word, _ = words_counter.most_common(1)[0]

    return common_word




if __name__ == '__main__':
    tasks = (task1, task2, task3, task4, task5)
    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')
