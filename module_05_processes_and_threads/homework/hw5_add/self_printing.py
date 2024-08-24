import os

result = 0
for n in range(1, 11):
    result += n ** 2
# Secret magic code

file_path = os.path.abspath(__file__)

line_numbers = {3,4,5,6}

with open(file_path, 'r') as file:
    lines = file.readlines()

for i, line in enumerate(lines, start=1):
    if i in line_numbers:
        print(line.strip())

# Прочитал этот файл и вывел нужные строчки в консоль