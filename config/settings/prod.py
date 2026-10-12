from .base import *  # noqa: F401,F403

DEBUG = False

# Адреса, с которых разрешён вход в админку (например, http://1.2.3.4)
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])  # noqa: F405

# Пока сайт работает по IP без HTTPS, эти параметры выключены.
# Когда появится домен и HTTPS, поставим True.
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
