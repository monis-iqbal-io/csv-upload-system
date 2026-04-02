import os
from pathlib import Path



SECRET_KEY = 'dummy-secret-key'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'app',
]

MIDDLEWARE = []

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[],
        'APP_DIRS': True,
        'OPTIONS': {},
           
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {}





BASE_DIR = Path(__file__).resolve().parent.parent


STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "app/static"
]


print(os.listdir(BASE_DIR / "app/static/css"))
