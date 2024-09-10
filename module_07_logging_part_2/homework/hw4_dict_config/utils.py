from typing import Union, Callable
from operator import sub, mul, truediv, add
import logging
from logging_config import setup_logging

setup_logging()

logger = logging.getLogger('hw4_utils_logger')

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
