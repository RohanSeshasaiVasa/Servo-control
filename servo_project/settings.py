SECRET_KEY = 'fake-key'
DEBUG = True
ALLOWED_HOSTS = [
	'192.168.0.250',
	'hamaralabs-rl.hamaralabs.com',
    '127.0.0.1'
]

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'control',
]

MIDDLEWARE = []

ROOT_URLCONF = 'servo_project.urls'
STATIC_URL = '/static/'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {},
}]
WSGI_APPLICATION = 'servo_project.wsgi.application'
