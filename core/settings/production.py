import os

from core.settings import BASE_DIR

DEBUG = False

ALLOWED_HOSTS = ["dispoison.pythonanywhere.com"]

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
