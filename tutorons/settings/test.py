from defaults import *  # noqa

SECRET_KEY = open(SECRET_KEY_FILE).read()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_default.sqlite3')
    },
    'logging': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_logging.sqlite3'),
    }
}
