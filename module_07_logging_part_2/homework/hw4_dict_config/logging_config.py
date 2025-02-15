import logging
import logging.config

dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': logging.INFO
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'level': logging.ERROR,
            'filename': 'app_errors.log'
        },
        'debug_file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'level': logging.DEBUG,
            'filename': 'calc_debug.log'
        },
        'error_file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'level': logging.ERROR,
            'filename': 'calc_error.log'
        }
    },
    'loggers': {
        'hw4_app_logger': {
            'handlers': ['console', 'file', 'debug_file', 'error_file'],
            'level': logging.DEBUG
        },
        'hw4_utils_logger': {
            'handlers': ['console', 'file', 'debug_file', 'error_file'],
            'level': logging.DEBUG
        }
    }
}

def setup_logging():
    logging.config.dictConfig(dict_config)