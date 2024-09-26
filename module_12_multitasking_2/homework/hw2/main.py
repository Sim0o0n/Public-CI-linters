import psutil
import os


def process_count(username: str) -> int:
    current_user = os.getlogin()
    processes = psutil.process_iter()
    user_processes = [p for p in processes if p.username() == username]
    return len(user_processes)



def total_memory_usage(root_pid: int) -> float:
    root_process = psutil.Process(root_pid)
    all_processes = [root_process] + root_process.children(recursive=True)
    total_usage = sum(proc.memory_percent() for proc in all_processes)

    return total_usage


if __name__ == "__main__":
    print(process_count('simon'))
    print(total_memory_usage(14571))