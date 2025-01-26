import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-gfu7)#$1r5var0qef=jdhj8chd&uu8*m58taijb+qy+oot%n6("

DEBUG = True

ALLOWED_HOSTS = []
# "testserver", "localhost"



INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tag.apps.TagConfig",
    "recipe.apps.RecipeConfig",
    "django_browser_reload",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "SimplyRecipes.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "SimplyRecipes.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "SimplyRecipes",
        "USER": "user",
        "PASSWORD": "test123",
        "HOST": "localhost",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Casablanca"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "staticfiles",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

TESTING = "test" in sys.argv

if not TESTING:
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#disable-the-toolbar-when-running-tests-optional
    # the proposed way in the link for installed apps seems to be a bug for PYCHARM
    # https://stackoverflow.com/questions/48740345/pycharm-doesnt-recognize-min-css-file-unresolved-template-reference-django/79223508#79223508
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,
    ]
