"""
Django settings for membermatters project.

Generated by "django-admin startproject" using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from collections import OrderedDict
from datetime import timedelta

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://2f4ae7b6c5444de7bc7093fdce72267e@o402264.ingest.sentry.io/5263074",
    environment=os.environ.get("PORTAL_ENV")
    if os.environ.get("PORTAL_ENV")
    else "UNKNOWN",
    integrations=[DjangoIntegration()],
    send_default_pii=True,
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.environ.get(
    "PORTAL_SECRET_KEY", "l)#t68rzepzp)0l#x=9mntciapun$whl+$j&=_@nl^zl1xm3j*"
)

# Default config is for dev environments and is overwritten in prod
DEBUG = True
ALLOWED_HOSTS = ["*"]
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = None
CSRF_COOKIE_SAMESITE = None

# this allows the frontend dev server to talk to the dev server
CORS_ORIGIN_WHITELIST = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "capacitor://localhost",
    "http://localhost",
]

if os.environ.get("PORTAL_ENV") == "Production":
    ENVIRONMENT = "Production"
    DEBUG = False
    ALLOWED_HOSTS = [
        os.environ.get("PORTAL_DOMAIN", "portal.example.org"),
        os.environ.get("PORTAL_DOMAIN_KIOSK", "kiosk.example.org"),
        "localhost",
    ]
    CORS_ORIGIN_WHITELIST = [
        "https://" + os.environ.get("PORTAL_DOMAIN", "portal.example.org"),
        "capacitor://localhost",
        "http://localhost",
    ]

    # Slightly hacky, but allows a direct IP while on the local network.
    # These may or may not be required for the interlocks, doors, etc. depending on your setup
    for x in range(1, 255):
        ALLOWED_HOSTS.append("http://10.0.0." + str(x))
        ALLOWED_HOSTS.append("10.0.0." + str(x))
        ALLOWED_HOSTS.append("http://10.0.1." + str(x))
        ALLOWED_HOSTS.append("http://192.168.0." + str(x))
        ALLOWED_HOSTS.append("http://192.168.1." + str(x))

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "profile",
    "access",
    "group",
    "memberbucks",
    "spacedirectory",
    "api_general",
    "api_access",
    "api_meeting",
    "api_admin_tools",
    "constance",
    "corsheaders",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "membermatters.middleware.ForceCsrfCookieMiddleware",
]

ROOT_URLCONF = "membermatters.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "constance.context_processors.config",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "membermatters.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("PORTAL_DB_LOCATION", "/usr/src/data/db.sqlite3"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": os.environ.get(
                "PORTAL_LOG_LOCATION", "/usr/src/logs/django.log"
            ),
        },
    },
    "loggers": {"django": {"handlers": ["file"], "level": "INFO", "propagate": True,},},
}

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "membermatters.custom_exception_handlers.fix_401",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer"),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-au"

TIME_ZONE = "Australia/Brisbane"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.environ.get(
    "PORTAL_STATIC_LOCATION", "/usr/src/app/memberportal/membermatters/static"
)
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/signin"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.environ.get("PORTAL_MEDIA_LOCATION", "/usr/src/data/media/")

AUTH_USER_MODEL = "profile.User"

REQUEST_TIMEOUT = 0.05

# Django constance configuration
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_ADDITIONAL_FIELDS = {"image_field": ["django.forms.ImageField", {}]}

CONSTANCE_CONFIG = {
    # General site info
    "SITE_NAME": (
        "MemberMatters Portal",
        "The title shown at the top of the page and as the tab title.",
    ),
    "SITE_OWNER": (
        "MemberMatters",
        "The name of the legal entity/association/club that is running this site.",
    ),
    "ENTITY_TYPE": (
        "Association",
        "This is the type of group you are such as an association, club, etc.",
    ),
    # Email config
    "EMAIL_SYSADMIN": (
        "example@example.com",
        "The default sysadmin email that should receive technical errors etc.",
    ),
    "EMAIL_ADMIN": (
        "example@example.com",
        "The default admin email that should receive administrative notifications.",
    ),
    "EMAIL_DEFAULT_FROM": (
        '"MemberMatters Portal" <example@example.org>',
        "The default email that outbound messages are sent from.",
    ),
    "SITE_MAIL_ADDRESS": (
        "123 Example St, Nowhere",
        "This address is used in the footer of all emails for anti spam.",
    ),
    # URLs
    "SITE_URL": (
        "https://membermatters.org",
        "The publicly accessible URL of your MemberMatters instance.",
    ),
    "MAIN_SITE_URL": ("https://membermatters.org", "The URL of your main website."),
    "INDUCTION_URL": (
        "https://eventbrite.com.au",
        "The URL members should visit to book in for a site induction.",
    ),
    # Logo and favicon
    "SITE_LOGO": ("img/logo/logo_small.png", "Site logo (rectangular)", "image_field"),
    "SITE_FAVICON": (
        "img/logo/logo_square_small.png",
        "Site favicon (square)",
        "image_field",
    ),
    # Localisation of terminology
    "MEMBERBUCKS_NAME": (
        "Memberbucks",
        "You can customise the name of the built in currency.",
    ),
    "GROUP_NAME": ("Group", "You can customise what we call a group."),
    "ADMIN_NAME": (
        "Administrators",
        "You can specify a different name for your admin group like executive or management committee.",
    ),
    "WEBCAM_PAGE_URLS": (
        "",
        "A JSON serialised array of URLs to pull webcam images from.",
    ),
    "HOME_PAGE_CARDS": (
        '[{"title": "Example", "description": "Example", "icon": "forum", "url": "https://membermatters.org/", "btn_text": "Click Here"}]',
        "You can specify cards that go on the home page with JSON. See https://github.com/MemberMatters/MemberMatters/blob/master/GETTING_STARTED.md.",
    ),
    "WELCOME_EMAIL_CARDS": (
        "",
        "Same syntax as HOME_PAGE_CARDS but icons are not used. If nothing is specified we will use HOME_PAGE_CARDS.",
    ),
    # Stripe config
    "STRIPE_PUBLISHABLE_KEY": ("", "Set this to your Stripe PUBLIC API key."),
    "STRIPE_SECRET_KEY": ("", "Set this to your Stripe PRIVATE API key."),
    "STRIPE_MEMBERBUCKS_TOPUP_OPTIONS": (
        "[1000, 2000, 3000]",
        "This is a JSON array of top-up amounts in cents.",
    ),
    "ENABLE_MEMBERBUCKS_STRIPE_INTEGRATION": (
        False,
        "Enable integration with stripe for adding memberbucks.",
    ),
    # Trello config
    "ENABLE_TRELLO_INTEGRATION": (
        False,
        "Enable the submit issue to trello integration. If disabled we'll send an email to EMAIL_ADMIN instead.",
    ),
    "TRELLO_API_KEY": ("", "Set this to your Trello API key."),
    "TRELLO_API_TOKEN": ("", "Set this to your Trello API token."),
    "TRELLO_ID_LIST": (
        "",
        "Set this to the ID of your card list you want issue " "to go to.",
    ),
    # Space API config
    "SPACE_DIRECTORY_ENABLED": (
        True,
        "Turn on the space directory API available at /api/spacedirectory.",
    ),
    "SPACE_DIRECTORY_OPEN": (False, "Sets the open state."),
    "SPACE_DIRECTORY_MESSAGE": (
        "This is the default MemberMatters (membermatters.org) space directory message.",
        "Sets the message.",
    ),
    "SPACE_DIRECTORY_ICON_OPEN": ("", "Sets the icon shown while in the open state."),
    "SPACE_DIRECTORY_ICON_CLOSED": (
        "",
        "Sets the icon shown while in the closed state.",
    ),
    "SPACE_DIRECTORY_LOCATION_ADDRESS": (
        "123 Setme St",
        "Sets the snail mail address.",
    ),
    "SPACE_DIRECTORY_LOCATION_LAT": (0, "Sets the latitude."),
    "SPACE_DIRECTORY_LOCATION_LON": (0, "Sets the longitude."),
    "SPACE_DIRECTORY_FED_SPACENET": (False, "Sets support for spacenet."),
    "SPACE_DIRECTORY_FED_SPACESAML": (False, "Sets support for spacesaml."),
    "SPACE_DIRECTORY_CAMS": (
        "[]",
        "A JSON list of strings (URLs) that webcam snapshots of the space can be found.",
    ),
    "SPACE_DIRECTORY_CONTACT_EMAIL": (
        "notset@example.com",
        "Sets the general contact email.",
    ),
    "SPACE_DIRECTORY_CONTACT_TWITTER": ("", "Sets the twitter handle."),
    "SPACE_DIRECTORY_CONTACT_FACEBOOK": ("", "Sets the Facebook page URL."),
    "SPACE_DIRECTORY_CONTACT_PHONE": (
        "",
        "Sets the general contact phone number, include country code with a leading +.",
    ),
    "SPACE_DIRECTORY_PROJECTS": (
        "[]",
        "A JSON list of strings (URLs) to project sites like wikis, GitHub, etc.",
    ),
}

CONSTANCE_CONFIG_FIELDSETS = OrderedDict(
    [
        ("General", ("SITE_NAME", "SITE_OWNER", "ENTITY_TYPE",)),
        (
            "Contact Information",
            (
                "EMAIL_SYSADMIN",
                "EMAIL_ADMIN",
                "EMAIL_DEFAULT_FROM",
                "SITE_MAIL_ADDRESS",
            ),
        ),
        ("URLs", ("SITE_URL", "MAIN_SITE_URL", "INDUCTION_URL")),
        ("Images", ("SITE_LOGO", "SITE_FAVICON")),
        (
            "Group Localisation",
            (
                "MEMBERBUCKS_NAME",
                "GROUP_NAME",
                "ADMIN_NAME",
                "WEBCAM_PAGE_URLS",
                "HOME_PAGE_CARDS",
                "WELCOME_EMAIL_CARDS",
            ),
        ),
        (
            "Stripe Integration",
            (
                "STRIPE_PUBLISHABLE_KEY",
                "STRIPE_SECRET_KEY",
                "ENABLE_MEMBERBUCKS_STRIPE_INTEGRATION",
                "STRIPE_MEMBERBUCKS_TOPUP_OPTIONS",
            ),
        ),
        (
            "Trello Integration",
            (
                "ENABLE_TRELLO_INTEGRATION",
                "TRELLO_API_KEY",
                "TRELLO_API_TOKEN",
                "TRELLO_ID_LIST",
            ),
        ),
        (
            "Space Directory",
            (
                "SPACE_DIRECTORY_ENABLED",
                "SPACE_DIRECTORY_OPEN",
                "SPACE_DIRECTORY_MESSAGE",
                "SPACE_DIRECTORY_ICON_OPEN",
                "SPACE_DIRECTORY_ICON_CLOSED",
                "SPACE_DIRECTORY_LOCATION_ADDRESS",
                "SPACE_DIRECTORY_LOCATION_LAT",
                "SPACE_DIRECTORY_LOCATION_LON",
                "SPACE_DIRECTORY_FED_SPACENET",
                "SPACE_DIRECTORY_FED_SPACESAML",
                "SPACE_DIRECTORY_CAMS",
                "SPACE_DIRECTORY_CONTACT_EMAIL",
                "SPACE_DIRECTORY_CONTACT_TWITTER",
                "SPACE_DIRECTORY_CONTACT_FACEBOOK",
                "SPACE_DIRECTORY_CONTACT_PHONE",
                "SPACE_DIRECTORY_PROJECTS",
            ),
        ),
    ]
)
