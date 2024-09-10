import configparser

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'fileFormatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S%Z',
        },
        'consoleFormatter': {
            'format': '%(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S%Z',
        },
    },
    'handlers': {
        'consoleHandler': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'consoleFormatter',
            'stream': 'ext://sys.stdout',
        },
        'fileHandler': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'fileFormatter',
            'filename': 'logfile.log',
        },
    },
    'loggers': {
        'root': {
            'level': 'DEBUG',
            'handlers': ['consoleHandler'],
        },
        'appLogger': {
            'level': 'DEBUG',
            'handlers': ['consoleHandler', 'fileHandler'],
            'propagate': False,
        },
    },
}

def ini_to_dict(ini_file):
    config = configparser.ConfigParser(interpolation=None)
    config.read(ini_file)

    def parse_args(args):
        return args.strip('()').split(',')

    dict_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {},
        'handlers': {},
        'loggers': {},
    }

    for key in config['formatters']['keys'].split(','):
        section = f'formatter_{key.strip()}'
        dict_config['formatters'][key.strip()] = {
            'format': config[section]['format'],
            'datefmt': config[section]['datefmt'],
        }

    for key in config['handlers']['keys'].split(','):
        section = f'handler_{key.strip()}'
        handler_class = config[section]['class']
        dict_config['handlers'][key.strip()] = {
            'class': f'logging.{handler_class}',
            'level': config[section]['level'],
            'formatter': config[section]['formatter'],
        }
        if handler_class == 'FileHandler':
            dict_config['handlers'][key.strip()]['filename'] = parse_args(config[section]['args'])[0]
        elif handler_class == 'StreamHandler':
            dict_config['handlers'][key.strip()]['stream'] = 'ext://sys.stdout'

    for key in config['loggers']['keys'].split(','):
        section = f'logger_{key.strip()}'
        dict_config['loggers'][key.strip()] = {
            'level': config[section]['level'],
            'handlers': config[section]['handlers'].split(','),
            'propagate': config.getboolean(section, 'propagate', fallback=False),
        }

    return dict_config

if __name__ == '__main__':
    ini_file = 'logging_conf.ini'
    dict_config = ini_to_dict(ini_file)
    print("Dict configuration converted from ini:")
    print(dict_config)
