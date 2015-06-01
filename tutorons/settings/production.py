from defaults import *  # noqa


SECRET_KEY = open(SECRET_KEY_FILE).read()
DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['tutorons.com', '.tutorons.com']
STATICFILES_DIRS += ((os.path.join(os.path.abspath(os.sep), 'var', 'www', 'tutorons')),)
STATIC_ROOT = os.path.join(os.path.abspath(os.sep), 'usr', 'local', 'tutorons', 'static')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S",
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/tutorons.log',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'gallery': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
