import threading
import time
from datetime import datetime
import requests
from queue import Queue


def fetch_timestamp():
    response = requests.get('http://127.0.0.1:8080/timestamp/{}'.format(int(time.time())))
    return response.text


def log_writer(log_queue):
    while True:
        log_entry = log_queue.get()
        if log_entry is None:
            break
        with open('logs.txt', 'a') as f:
            f.write(log_entry + '\n')
        log_queue.task_done()


def log_thread(log_queue):
    for _ in range(20):
        timestamp = fetch_timestamp()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} {current_time}"
        log_queue.put(log_entry)
        time.sleep(1)


if __name__ == "__main__":
    log_queue = Queue()

    writer_thread = threading.Thread(target=log_writer, args=(log_queue,))
    writer_thread.start()

    threads = []
    for _ in range(10):
        thread = threading.Thread(target=log_thread, args=(log_queue,))
        threads.append(thread)
        thread.start()
        time.sleep(1)

    for thread in threads:
        thread.join()

    log_queue.put(None)
    writer_thread.join()

    with open('logs.txt', 'r') as f:
        logs = f.readlines()

    logs.sort(key=lambda x: float(x.split()[0]))

    with open('sorted_logs.txt', 'w') as f:
        f.writelines(logs)

    print("Логи успешно записаны и отсортированы в sorted_logs.txt")
