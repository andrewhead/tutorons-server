from defaults import *
import os.path


# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = open(SECRET_KEY_FILE).read()
DEBUG = True
TEMPLATE_DEBUG = True

STATIC_ROOT = os.path.join(BASE_DIR, os.path.pardir, 'static')
