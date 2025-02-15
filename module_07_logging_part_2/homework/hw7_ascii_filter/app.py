import contextlib
import sys
from utils import string_to_operator
import logging
import logging_tree

class ASCIIFilter(logging.Filter):
    def filter(self, record):
        return record.getMessage().isascii()

def conf_logger():
    logger = logging.getLogger('hw7_app_logger')
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler("app_errors.log")
    file_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    ascii_filter = ASCIIFilter()
    console_handler.addFilter(ascii_filter)
    file_handler.addFilter(ascii_filter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

def calc(args):
    logger = logging.getLogger('hw7_app_logger')
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

    logger.info(f"Result:{result}")
    logger.debug(f"{num_1} {operator} {num_2} = {result}")


if __name__ == '__main__':
    conf_logger()

    with open("logging_tree.txt", "w") as f:
        with contextlib.redirect_stdout(f):
            logging_tree.printout()

    calc(['2', '+', '3'])
