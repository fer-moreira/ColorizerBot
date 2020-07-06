""" Main logging script, sterr, stdout, file """ 

import logging
import logging.config
import sys, os

class _ExcludeErrorsFilter(logging.Filter):
    def filter(self, record):
        return record.levelno > 0

config = {
    'version': 1,
    'filters': {
        'exclude_errors': {
            '()': _ExcludeErrorsFilter
        }
    },
    'formatters': {
        # Modify log message format here or replace with your custom formatter class
        'logger': {
            'format': '%(asctime)s %(name)s (line %(lineno)s) | %(levelname)-8s | %(message)s'
        }
    },
    'handlers': {
        'console_stderr': {
            # Sends log messages with log level ERROR or higher to stderr
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
            'formatter': 'logger',
            'stream': sys.stderr
        },
        'console_stdout': {
            # Sends log messages with log level lower than ERROR to stdout
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'logger',
            'filters': ['exclude_errors'],
            'stream': sys.stdout
        },
        'file': {
            # Sends all log messages to a file
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'logger',
            'filename': 'logs.log',
            'encoding': 'utf8'
        }
    },
    'root': {
        # In general, this should be kept at 'NOTSET'.
        # Otherwise it would interfere with the log levels set for each handler.
        'level': 'NOTSET',
        'handlers': ['console_stderr','console_stdout', 'file']
    },
}

logging.config.dictConfig(config)