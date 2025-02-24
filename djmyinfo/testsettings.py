from .settings import *

ALLOWED_HOSTS = ["testserver"]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3.test',
    }
}
