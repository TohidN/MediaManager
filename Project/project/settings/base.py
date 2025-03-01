import os
from decouple import config
from .settings import *  # Default and untuched django settings file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Secret Key
SECRET_KEY = config("SECRET_KEY")

# Application definition
INSTALLED_APPS += [
   # requirements
   'django_extensions',
   'sorl.thumbnail',
   # Applications
   'media',
]

MIDDLEWARE += [
	# Required middlewares
]
  
TEMPLATES = [
	{
		"BACKEND": "django.template.backends.django.DjangoTemplates",
		"DIRS": [
			os.path.join(BASE_DIR, "project", "templates"),
			os.path.join(BASE_DIR, "media", "templates"),
		],
		"APP_DIRS": True,
		"OPTIONS": {
			"context_processors": [
				"django.template.context_processors.debug",
				"django.template.context_processors.media",
				"django.template.context_processors.request",
				"django.contrib.auth.context_processors.auth",
				"django.contrib.messages.context_processors.messages",
			],
			"debug": True,
		},
	},
]

DATABASES = {
	"default": {
		"ENGINE": config("DB_ENGINE", default="django.db.backends.postgresql_psycopg2"),
		"NAME": config("DB_NAME", default="database"),
		"USER": config("DB_USER", default="postgres"),
		"PASSWORD": config("DB_PASSWORD", default="root"),
		"HOST": config("DB_HOST", default="localhost"),
		"PORT": config("DB_PORT", default="5432"),
	}
}

# Rest Framework
REST_FRAMEWORK = {
	"DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
	"DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
	"DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
	"PAGE_SIZE": 20,
}

# Email options
EMAIL_FORMAT_HTML = True  # if false plain text emails will be sent

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "project", "static_root")
STATICFILES_DIRS = (
	os.path.join(BASE_DIR, "project", "static"),
	os.path.join(BASE_DIR, "media", "static"),
)

# Media Files
MEDIA_URL = "files/"
MEDIA_ROOT = os.path.join(BASE_DIR, "project", "media")

# allows to load iframe from same hostname
X_FRAME_OPTIONS = "SAMEORIGIN"

# extend upload
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000