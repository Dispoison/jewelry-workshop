import os

from core.settings import BASE_DIR

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
