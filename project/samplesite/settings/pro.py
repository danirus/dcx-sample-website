import os

from .base import *

DEBUG = False

ADMINS = (
    (os.environ.get('ADMIN_NAME'), os.environ.get('ADMIN_EMAIL')),
)

ALLOWED_HOSTS = ['*']  # TODO.

DATABASES = {
    'default': {

    }
}