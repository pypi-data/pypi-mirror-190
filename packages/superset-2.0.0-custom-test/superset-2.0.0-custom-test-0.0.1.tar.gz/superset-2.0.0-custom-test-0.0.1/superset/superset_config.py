from datetime import timedelta
from typing import List
from celery.schedules import crontab
from cachelib.redis import RedisCache

MODE = "dev"

SECRET_KEY = "thisISaSECRET_1234"
SQLALCHEMY_TRACK_MODIFICATIONS = True

MAPBOX_API_KEY = "pk.eyJ1IjoidGVoLWxhYiIsImEiOiJjazhvbWR0YzkwMjdwM2xwbHhobGtydjIxIn0.psnZmkcLNFUHmVGOaAGPxg"

############################
# DEVELOPMENT #
############################

# CACHE_CONFIG = {
#     "CACHE_TYPE": "NullCache",
#     "CACHE_NO_NULL_WARNING": False
# }

if MODE == "dev":
    SUPERSET_WEBSERVER_PROTOCOL = "http"
    SUPERSET_WEBSERVER_ADDRESS = "192.168.1.231"
    SUPERSET_WEBSERVER_PORT = 9000
    LOGO_TARGET_PATH = "/"

    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://superset:superset@localhost:5435/superset"
    )

    REDIS_CACHE_CONFIG = {
        "CACHE_TYPE": "RedisCache",
        "CACHE_DEFAULT_TIMEOUT": 300,
        "CACHE_KEY_PREFIX": "superset_develop_",
        "CACHE_REDIS_HOST": "localhost",
        "CACHE_REDIS_PORT": 6379,
        "CACHE_REDIS_DB": 0,
        "CACHE_REDIS_URL": "redis://localhost:6379"
    }

# Default cache for Superset objects
# Здесь, например, хранится информация о дашборде. Когда вы открываете
# конкретный дашборд, все данные (графики, их ширина, статус дашборда
# (опуб./черновик) забираются из этого кэша.
# CACHE_CONFIG = {
#    "CACHE_TYPE": "RedisCache",
#    "CACHE_DEFAULT_TIMEOUT": 10,
#    "CACHE_KEY_PREFIX": "superset_develop_",
#    "CACHE_REDIS_HOST": "localhost",
#    "CACHE_REDIS_PORT": 6379,
#    "CACHE_REDIS_DB": 0,
#    "CACHE_REDIS_URL": "redis://localhost:6379"
# }


###########
# TESTING #
###########
if MODE == "test_local":
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://superset:superset@172.18.0.1:5432/superset"
    )

    # REDIS_CACHE_CONFIG = {
    #     "CACHE_TYPE": "NullCache",
    #     "CACHE_DEFAULT_TIMEOUT": 300,
    #     "CACHE_KEY_PREFIX": "superset_develop_",
    #     "CACHE_REDIS_HOST": "172.18.0.2",
    #     "CACHE_REDIS_PORT": 6379,
    #     "CACHE_REDIS_DB": 0,
    #     "CACHE_REDIS_URL": "redis://172.18.0.2:6379",
    # }

    REDIS_CACHE_CONFIG = {
        "CACHE_TYPE": "NullCache",
        "CACHE_NO_NULL_WARNING": True
    }

    CACHE_CONFIG = REDIS_CACHE_CONFIG


##############
# PRODUCTION #
##############
if MODE == "prod":
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://superset:fCfZbd9Mw7kX5aZx@192.168.100.4:5432/superset_develop"
    )

    REDIS_CACHE_CONFIG = {
        "CACHE_TYPE": "RedisCache",
        "CACHE_DEFAULT_TIMEOUT": 300,
        "CACHE_KEY_PREFIX": "superset_develop_",
        "CACHE_REDIS_HOST": "redis",
        "CACHE_REDIS_PORT": 6379,
        "CACHE_REDIS_DB": 1,
        "CACHE_REDIS_URL": "redis://192.168.100.5:6379/1",
    }

    CACHE_CONFIG = REDIS_CACHE_CONFIG


########
# MISC #
########
# Cache for datasource metadata and query results
# DATA_CACHE_CONFIG = {
#     **REDIS_CACHE_CONFIG,
#     "CACHE_DEFAULT_TIMEOUT": 120,
#     "CACHE_KEY_PREFIX": "superset_develop_data_",
# }

# # Cache for dashboard filter state
# FILTER_STATE_CACHE_CONFIG = {
#     **REDIS_CACHE_CONFIG,
#     "CACHE_DEFAULT_TIMEOUT": 120,
#     "REFRESH_TIMEOUT_ON_RETRIEVAL": True,
#     "CACHE_KEY_PREFIX": "superset_develop_filter_",
# }

# # Cache for explore form data state
# # Даже при сохранении графика, после обновления выдает прошлые значения в
# # панели управления. Помог только рефреш кэша.
# EXPLORE_FORM_DATA_CACHE_CONFIG = {
#     **REDIS_CACHE_CONFIG,
#     # "CACHE_DEFAULT_TIMEOUT": int(timedelta(days=7).total_seconds()),
#     "CACHE_DEFAULT_TIMEOUT": 30,
#     "REFRESH_TIMEOUT_ON_RETRIEVAL": True,
#     "CACHE_KEY_PREFIX": "superset_develop_explore_",
# }

if MODE == "dev":  # or MODE == "test_local":
    THUMBNAIL_SELENIUM_USER = "admin"
    THUMBNAIL_CACHE_CONFIG = {
        **REDIS_CACHE_CONFIG,
        "CACHE_DEFAULT_TIMEOUT": 60 * 60 * 4,  # 4 часа
        "CACHE_KEY_PREFIX": "superset_develop_thumbnail_",
    }

APP_ICON = "/static/assets/images/tehlab-logo-horiz.svg"

FEATURE_FLAGS = {
    # jinja templating внутри sql lab и мб где-то еще
    "ENABLE_TEMPLATE_PROCESSING": True,
    # "DASHBOARD_CACHE": False,
    "DASHBOARD_CROSS_FILTERS": True,
    "ALERT_REPORTS": True,  # if MODE not in ['prod', 'test_local'] else False,
    # Позволяет делиться доступом с определенным ролями.
    "DASHBOARD_RBAC": True,
    # не знаю, что это
    # "UX_BETA": True if MODE not in ['prod', 'test_local'] else False,
    # Включает превью дашбордов и графиков
    "THUMBNAILS": True,  # if MODE not in ['prod', 'test_local'] else False,
    # Отображает карточки по дефолту вместо списка (для дашбордов и графиков)
    # "LISTVIEWS_DEFAULT_CARD_VIEW": True,
    # "ENABLE_FILTER_BOX_MIGRATION": True,
    # Allow to set non-timeseries column as X-Axis in Line Chart
    # https://fossies.org/linux/apache-superset/RELEASING/release-notes-1-5/README.md
    "GENERIC_CHART_AXES": True,
    # Обязательная фича для расчета мер для графиков
    "ALLOW_ADHOC_SUBQUERY": True,
}

BABEL_DEFAULT_LOCALE = "ru"
LANGUAGES = {
    "ru": {"flag": "ru", "name": "Русский"},
    "en": {"flag": "us", "name": "Английский"},
}

# Разрешить пользователям запрашивать доступ до отдельной таблицы (реализовано неудобно)
ENABLE_ACCESS_REQUEST = True

# Celery делает скриншоты дашбордов и исполняет асинхронные SQL запросы
if MODE == "dev1":  # or MODE == 'test_local':
    redis_url = (
        "redis://localhost:6379/0" if MODE == "dev" else "redis://172.18.0.2:6379/0"
    )

    class CeleryConfig:  # pylint: disable=too-few-public-methods
        broker_url = redis_url
        imports = (
            "superset.sql_lab",
            "superset.tasks",
        )
        result_backend = redis_url
        worker_log_level = "DEBUG"
        worker_prefetch_multiplier = 10
        task_acks_late = True
        task_annotations = {
            "sql_lab.get_sql_results": {"rate_limit": "100/s"},
            "email_reports.send": {
                "rate_limit": "1/s",
                "time_limit": int(timedelta(seconds=120).total_seconds()),
                "soft_time_limit": int(timedelta(seconds=150).total_seconds()),
                "ignore_result": True,
            },
        }
        beat_schedule = {
            "reports.scheduler": {
                "task": "reports.scheduler",
                "schedule": crontab(minute="*", hour="*"),
            },
            "reports.prune_log": {
                "task": "reports.prune_log",
                "schedule": crontab(minute=0, hour=0),
            },
        }

    CELERY_CONFIG = CeleryConfig  # pylint: disable=invalid-name

    WEBDRIVER_BASEURL = (
        "http://192.168.1.231:9000/" if MODE == "dev" else "http://172.18.0.2:8080/"
    )  # "http://0.0.0.0:8080/"
    WEBDRIVER_TYPE = "firefox"
    # for older versions this was  EMAIL_REPORTS_WEBDRIVER = "firefox"
    WEBDRIVER_OPTION_ARGS = ["--headless"]

# Email configuration
SMTP_HOST = "smtp.yandex.ru"
SMTP_STARTTLS = False  # Выключаем шифрование StartTLS, иначе не будет работать
SMTP_SSL = True
SMTP_USER = "superset-reports@teh-lab.ru"  # User = почта
SMTP_PORT = 465
SMTP_PASSWORD = "y5DRSQFrybYsyCI"
SMTP_MAIL_FROM = "superset-reports@teh-lab.ru"


# ---------------------------------------------------
# Alerts & Reports
# ---------------------------------------------------
if MODE == "dev":  # or MODE == 'test_local':
    # Used for Alerts/Reports (Feature flask ALERT_REPORTS) to set the size for the
    # sliding cron window size, should be synced with the celery beat config minus 1 second
    ALERT_REPORTS_CRON_WINDOW_SIZE = 59
    ALERT_REPORTS_WORKING_TIME_OUT_KILL = True
    # if ALERT_REPORTS_WORKING_TIME_OUT_KILL is True, set a celery hard timeout
    # Equal to working timeout + ALERT_REPORTS_WORKING_TIME_OUT_LAG
    ALERT_REPORTS_WORKING_TIME_OUT_LAG = int(timedelta(seconds=10).total_seconds())
    # if ALERT_REPORTS_WORKING_TIME_OUT_KILL is True, set a celery hard timeout
    # Equal to working timeout + ALERT_REPORTS_WORKING_SOFT_TIME_OUT_LAG
    ALERT_REPORTS_WORKING_SOFT_TIME_OUT_LAG = int(timedelta(seconds=1).total_seconds())
    # If set to true no notification is sent, the worker will just log a message.
    # Useful for debugging
    ALERT_REPORTS_NOTIFICATION_DRY_RUN = False
    # Max tries to run queries to prevent false errors caused by transient errors
    # being returned to users. Set to a value >1 to enable retries.
    ALERT_REPORTS_QUERY_EXECUTION_MAX_TRIES = 1
    # A custom prefix to use on all Alerts & Reports emails
    EMAIL_REPORTS_SUBJECT_PREFIX = "Суперсет отчет: "

    # If enabled, it can be used to store the results of long-running queries
    # in SQL Lab by using the "Run Async" button/feature
    redis_url = "localhost" if MODE == "dev" else "172.18.0.2"
    RESULTS_BACKEND = RedisCache(
        host=redis_url, port=6379, key_prefix="superset_results_"
    )


# Название вкладки в браузере
APP_NAME = "Суперсет"
# Текст справа от логотипа (в верхнем левом углу)
LOGO_RIGHT_TEXT = "Суперсет"

# Send user to a link where they can report bugs
BUG_REPORT_URL = "https://jira.teh-lab.ru/"

# Send user to a link where they can read more about Superset
DOCUMENTATION_URL = "https://confluence.teh-lab.ru/"
DOCUMENTATION_TEXT = "Documentation"
DOCUMENTATION_ICON = (
    "/static/assets/images/superset-logo-horiz.png"  # Recommended size: 16x16
)

# Параметр отсутствует в основном конфиге, но требуется на фронте
SQLALCHEMY_DOCS_URL = "https://docs.sqlalchemy.org/"

CSV_EXPORT = {"encoding": "utf-8"}
EXCEL_EXPORT = {"encoding": "utf-8"}


# A list of preferred databases, in order. These databases will be
# displayed prominently in the "Add Database" dialog. You should
# use the "engine_name" attribute of the corresponding DB engine spec
# in `superset/db_engine_specs/`.
PREFERRED_DATABASES: List[str] = [
    "PostgreSQL",
    "MySQL",
]
