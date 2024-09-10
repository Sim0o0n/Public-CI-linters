from typing import Union, Callable
from operator import sub, mul, truediv, add
import logging
from logger_helper import LevelFileHandler


logger = logging.getLogger('hw3_utils_logger')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler("utils_errors.log")
file_handler.setLevel(logging.ERROR)

debug_file_handler = LevelFileHandler(logging.DEBUG, 'utils_debug.log')
error_file_handler = LevelFileHandler(logging.ERROR, 'utils_error.log')

formatter = logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
debug_file_handler.setFormatter(formatter)
error_file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(debug_file_handler)
logger.addHandler(error_file_handler)

OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    try:
        if not isinstance(value, str):
            logger.error(f"wrong operator type {value}")
            raise ValueError("wrong operator type")

        if value not in OPERATORS:
            logger.error(f"wrong operator value {value}")
            raise ValueError("wrong operator value")

        return OPERATORS[value]

    except ValueError as e:
        logger.error("Error in string_to_operator function")
        logger.exception(e)
        raise
