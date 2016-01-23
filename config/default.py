# coding: utf-8
import os


class Config(object):
    """配置基类"""
    # Flask app config

    DEBUG = True
    TESTING = False
    SECRET_KEY = "\xb5\xb3}#\xb7A\xcac\x9d0\xb6\x0f\x80z\x97\x00\x1e\xc0\xb8+\xe9)\xf0}"
    PERMANENT_SESSION_LIFETIME = 3600 * 1
    SESSION_COOKIE_NAME = 'dhwy_session'

    # Root path of project
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # SQLAlchemy config
    # See:
    # https://pythonhosted.org/Flask-SQLAlchemy/config.html#connection-uri-format
    # http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#database-urls
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/dhwy"

    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_DB_QUERY_TIMEOUT = 0.5

    # Redis
    REDIS = False  # 是否启用Redis
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 1
    # Uploadsets config
    # UPLOADS_DEFAULT_DEST = "/WebServer/Documents/uploads"  # 上传文件存储路径
    # UPLOADS_DEFAULT_DEST = "D:/xampp/htdocs/jeepsk_uploads"  # 上传文件存储路径
    UPLOADS_DEFAULT_DEST = os.path.join(PROJECT_PATH, 'web/static')  # 上传文件存储路径

    # UPLOADS_DEFAULT_URL = "http://localhost/jeepsk_uploads/"  # 上传文件访问URL
    UPLOADS_DEFAULT_URL = "static"  # 上传文件访问URL
    # Flask-DebugToolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Sentry config
    SENTRY_DSN = ''

    # 查询分页
    FLASKY_PER_PAGE = 20

    # Host string, used by fabric
    HOST_STRING = "ubuntu@182.254.152.46"

    DEVICES = [
        ('mobile',
         'iPhone|iPod|Android.*Mobile|Windows.*Phone|dream|blackberry|CUPCAKE|webOS|incognito'
         '|webmate'),
        ('tablet', 'iPad|Android'),
        ('pc', '.*')
    ]

    # 上传文件格式
    ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])
    # 16 M
    MAX_CONTENT_LENGTH = 16777216
