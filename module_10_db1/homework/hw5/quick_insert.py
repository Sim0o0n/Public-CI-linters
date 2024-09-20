from itertools import count
from typing import Union, List

from module_09_docker.homework.task2.new_year_application.app import index

Number = Union[int, float, complex]


def find_insert_position(array: List[Number], number: Number) -> int:
    result = len(array)
    for i, num in enumerate(array):
        if num >= number:
            result = i
            break

    print(result)
    return result

if __name__ == '__main__':
    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    insert_position: int = find_insert_position(A, x)
    assert insert_position == 5

    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    A.insert(insert_position, x)
    assert A == sorted(A)
