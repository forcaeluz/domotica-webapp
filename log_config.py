LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] \t %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] \t %(module)s %(message)s'
        },
        'arduino': {
            'format': '%(asctime)s - %(message)s'
        }
    },
    'handlers': {
        'arduino': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'arduino.log',
            'backupCount': 5,
            'formatter': 'arduino'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'simple'
        },
        'stderr': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'application.log',
            'backupCount': 5,
            'formatter': 'verbose',
            'maxBytes': 10000000
        }
    },
    'loggers': {
        'arduino': {
            'handlers': ['arduino', 'console'],
            'level': 'DEBUG',
        },
        'application.usart_communication': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'application.message_parser': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'application': {
            'handlers': ['stderr', 'file'],
            'level': 'WARNING',
        }
    }
}