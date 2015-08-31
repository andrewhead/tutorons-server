from defaults import *  # noqa


SECRET_KEY = open(SECRET_KEY_FILE).read()
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
REGEX_SVG_ENDPOINT = "http://127.0.0.1:8000/"

# Emulate an SSL server on localhost
INSTALLED_APPS += (
    "sslserver",
)

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
        },
        'regionfile': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '.regions.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'region': {
            'handlers': ['regionfile'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
