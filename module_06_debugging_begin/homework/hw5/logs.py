from datetime import datetime

with open('measure_me.log', 'r') as file:
    log_data = file.readlines()

durations = []

start_time = None
end_time = None

for line in log_data:
    parts = line.split(' - ')
    timestamp_str = parts[0]
    message = parts[2]

    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

    if "Enter measure_me" in message:
        start_time = timestamp
    elif "Leave measure_me" in message:
        end_time = timestamp
        duration = (end_time - start_time).total_seconds()
        durations.append(duration)

average_duration = sum(durations) / len(durations) if durations else 0
print(f"Среднее время выполнения функции measure_me: {average_duration:.6f} секунд")
