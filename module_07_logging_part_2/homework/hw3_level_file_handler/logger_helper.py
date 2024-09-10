import logging


class LevelFileHandler(logging.Handler):
    def __init__(self, level, filename):
        super().__init__(level)
        self.filename = filename
        self.file_handler = logging.FileHandler(filename)
        self.file_handler.setLevel(level)
        self.formatter = logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s')
        self.file_handler.setFormatter(self.formatter)

    def emit(self, record):
        try:
            if self.filter(record):
                self.file_handler.emit(record)
        except Exception:
            self.handleError(record)


def get_logger(name: str) -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    debug_file_handler = LevelFileHandler(logging.DEBUG, 'calc_debug.log')
    error_file_handler = LevelFileHandler(logging.ERROR, 'calc_error.log')

    formatter = logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s')
    console_handler.setFormatter(formatter)
    debug_file_handler.setFormatter(formatter)
    error_file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(debug_file_handler)
    logger.addHandler(error_file_handler)

    return logger

