from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.2.100"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
    'rosetta'
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.sql.SQLPanel',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

COMMENTS_APP = "django_comments_xtd"
COMMENTS_XTD_CONFIRM_EMAIL = True   # Set to False to disable confirmation
COMMENTS_XTD_SALT = b"es-war-einmal-una-bella-princesa-in-a-beautiful-castle"
COMMENTS_XTD_FROM_EMAIL = 'noreply@example.com'
COMMENTS_XTD_CONTACT_EMAIL = 'helpdesk@example.com'
COMMENTS_XTD_THREADED_EMAILS = False # default to True, use False to allow
                                     # other backend (say Celery based) send
                                     # your emails.

COMMENTS_XTD_REACTIONS_ENUM = "samplesite.enums.ReactionEnum"

# Quotes can have 1-level depth nested comments.
COMMENTS_XTD_MAX_THREAD_LEVEL = 1
# COMMENTS_XTD_MAX_THREAD_LEVEL_BY_APP_MODEL = {
#     'articles.article': 2,
# }

COMMENTS_XTD_LIST_ORDER = ('-thread_id', 'order')

# COMMENTS_XTD_APP_MODEL_OPTIONS = {
#     'articles.article': {
#         'who_can_post': 'all',
#         'allow_flagging': True,
#         'allow_feedback': True,
#         'show_feedback': True,
#     },
#     'quotes.quote': {
#         'who_can_post': 'all',
#         'allow_flagging': True,
#         'allow_feedback': True,
#         'show_feedback': True,
#     }
# }

COMMENTS_XTD_API_USER_REPR = lambda u: u.get_full_name()

SIGNUP_URL          = "/user/signup/"
LOGIN_URL           = "/user/login/"
LOGOUT_URL          = "/user/logout/"
LOGIN_REDIRECT_URL  = "/"
LOGOUT_REDIRECT_URL = "/"


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication'
    ]
}
