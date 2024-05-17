from pathlib import Path
import time

import bleach
from utils.arg_parse import LOCALHOST
from utils.ini import Ini
# from flask_security import uia_username_mapper  # noqa: F401


def uia_login_mapper(identity: str) -> str:
    # we allow pretty much anything - but we bleach it.
    return bleach.clean(identity, strip=True)


class ConfigIni(object):
    def __init__(self) -> None:
        ini_auth_name = Path('configs/auth_code.ini')
        self.ini_auth = Ini(ini_auth_name)

    def _err_config_ini(self, err_text) -> None:
        print(err_text)  # noqa: T201
        time.sleep(3)
        exit()

    def select_section(self, section: str = '') -> None:
        if not section or not self.ini_auth.set_name_section(section):
            self._err_config_ini(f'Не найдена секция [{section}] в ini')

    def get_mysql_authorization(self, section: str = '') -> dict[str, str]:
        self.select_section(section)
        return {
                'user': self.ini_auth.get_param('user'),
                'password': self.ini_auth.get_param('pass'),
                'host': self.ini_auth.get_param('host'),
                'database': self.ini_auth.get_param('database')
                }

    def get_mysql_authorization_sqlalchemy(self, section: str = '') -> str:
        _auth = self.get_mysql_authorization(section=section)
        return 'mysql+mysqlconnector://%(u)s:%(p)s@%(h)s/%(b)s' % {
                    'u': _auth['user'],
                    'p': _auth['password'],
                    'h': _auth['host'],
                    'b': _auth['database'],
                    }

    def section_config_sql(self) -> str:
        if LOCALHOST:
            return 'mysql_local'
        return 'mysql'

    def get_secret_key(self) -> str:
        self.select_section('flask')
        return self.ini_auth.get_param('secret_key')

    def get_password_salt(self) -> str:
        self.select_section('flask')
        return self.ini_auth.get_param('password_salt')


class ConfigurationGlobal(object):
    config_ini = ConfigIni()
    TEMPLATES_AUTO_RELOAD = True
    PROPAGATE_EXCEPTIONS = True  # выводить traceback Python в ответе
    JSON_AS_ASCII = False
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = config_ini.get_mysql_authorization_sqlalchemy(
                                section=config_ini.section_config_sql()
                                )
    SQLALCHEMY_NATIVE_UNICODE = 'utf-8'
    SQLALCHEMY_ECHO = False
    """
    STATIC_FOLDER = 'static'
    # USE_X_SENDFILE = True
    LOGGER_NAME = 'flask_log'

    # Security
    # Generate a nice key using secrets.token_urlsafe()
    SECRET_KEY = config_ini.get_secret_key()
    CSRF_ENABLED = True
    SESSION_COOKIE_NAME = 'FLSESSID'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_REFRESH_EACH_REQUEST = True
    # REMEMBER_COOKIE_HTTPONLY = True
    # REMEMBER_COOKIE_DURATION = 3600

    """
    # flask-security
    # Generate a good salt using: secrets.SystemRandom().getrandbits(128)
    # SECURITY_PASSWORD_SALT = config_ini.get_password_salt()
    # SECURITY_PASSWORD_SCHEMES = ['bcrypt']
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SINGLE_HASH = True  # ['bcrypt', 'pbkdf2_sha256', 'plaintext']
    SECURITY_USERNAME_ENABLE = True
    SECURITY_USERNAME_REQUIRED = True
    SECURITY_USERNAME_MAX_LENGTH = 40
    # SECURITY_USER_IDENTITY_ATTRIBUTES = [{'username': {'mapper': uia_login_mapper, 'case_insensitive': True}},]
    # SECURITY_LOGIN_USER_TEMPLATE = 'security/login_user.html'  # 'security/login_user_2.html'
    SECURITY_EMAIL_VALIDATOR_ARGS = {'check_deliverability': False}
    SECURITY_TRACKABLE = True
    # for test
    # LOGIN_DISABLED = True

    # Babel
    # LANGUAGES = ['en', 'es', 'ru']
    # BABEL_DEFAULT_LOCALE = 'ru'
    # BABEL_DEFAULT_TIMEZONE = 'Europe/Moscow'
    """


class Configuration(ConfigurationGlobal):
    if LOCALHOST:
        DEBUG = True
        SERVER_NAME = 'celery_flask.localhost:5020'
    else:
        DEBUG = False
        SERVER_NAME = 'celery_flask.vintets.ru'


class MainSettings(object):
    log_directory = Path('logs')
    log_debug_file = log_directory / 'debug.log'
    log_error_file = log_directory / 'errors.log'
    log_debug = True
