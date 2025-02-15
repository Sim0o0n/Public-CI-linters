from typing import Union, Callable
from operator import sub, mul, truediv, add
import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('hw5_utils_logger')
logger.setLevel(logging.DEBUG)

handler = TimedRotatingFileHandler(
    'utils.log',
    when='H',
    interval=10,
    backupCount=0
)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

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

