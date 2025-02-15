import sys
from utils import string_to_operator
from logger_helper import LevelFileHandler
import logging


def conf_logger():
    logger = logging.getLogger('hw3_app_logger')
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler("app_errors.log")
    file_handler.setLevel(logging.ERROR)

    debug_file_handler = LevelFileHandler(logging.DEBUG, 'calc_debug.log')
    error_file_handler = LevelFileHandler(logging.ERROR, 'calc_error.log')

    formatter = logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    debug_file_handler.setFormatter(formatter)
    error_file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(debug_file_handler)
    logger.addHandler(error_file_handler)

def calc(args):
    logger = logging.getLogger('hw3_app_logger')
    logger.info(f"Arguments: {args}")

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.error("Error while converting number 1")
        logger.exception(e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.error("Error while converting number 2")
        logger.exception(e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)


    logger.info(f"Result: {result}")
    logger.debug(f"{num_1} {operator} {num_2} = {result}")


if __name__ == '__main__':
    conf_logger()
    try:
        calc(sys.argv[1:])
    except Exception as e:
        logger = logging.getLogger('hw3_app_logger')
        logger.error("An error occurred while executing the calculation")
        logger.exception(e)
    calc('2+3')
