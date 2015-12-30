# coding: UTF-8

import os
import sys

# 将project目录加入sys.path
from flask.ext.cache import Cache

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.insert(0, project_path)
from flask import Flask, request, url_for, g, render_template, session
from flask_wtf.csrf import CsrfProtect
from flask.ext.uploads import configure_uploads
from utils._redis import set_user_active_time
from config import load_config
from web.utils.account import get_current_user

# convert python's encoding to utf8
reload(sys)
sys.setdefaultencoding('utf8')

csrf = CsrfProtect()

cache = Cache()


def create_app():
    """创建Flask app"""
    app = Flask(__name__)
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})
    cache.init_app(app)
    # Load config
    config = load_config()
    app.config.from_object(config)

    # CSRF protect
    csrf.init_app(app)

    # 注册组件
    register_db(app)
    register_routes(app)
    register_jinja(app)
    register_error_handle(app)
    register_logger(app)
    register_uploadsets(app)

    # before every request
    @app.before_request
    def before_request():
        """Do something before request"""
        # 记录用户的访问时间到redis
        g.user = get_current_user()
        if g.user:
            set_user_active_time(g.user.id)
        pass

    from .utils.devices import Devices

    devices = Devices(app)

    return app


def register_jinja(app):
    """注册filter，模板全局变量和全局函数"""
    from jinja2 import Markup
    from .models import db

    @app.context_processor
    def inject_vars():

        # site info
        g_site_info = {
            "url": "http://localhost:5000",
            "logo": "../static/images/logo.png",
            "title": "",
            "company": "济南锦粉世家商贸有限公司",
            "year": "2015",
            "icp": "沪ICP备11038770号",
            "qq": "8888888",
            "qqgroup": "1234567",
            "tel": "8888888",
            "email": "admin@admin.com",
        }

        return dict(
                website=g_site_info,

        )

    def url_for_other_page(page, key='page', params=None):
        """Generate url for pagination"""
        view_args = request.view_args.copy()
        args = request.args.copy().to_dict()
        combined_args = dict(view_args.items() + args.items())
        combined_args[key] = page
        if params:
            combined_args.update(params)
        return url_for(request.endpoint, **combined_args)

    def set_url_param(params):
        """Set param in url"""
        view_args = request.view_args.copy()
        args = request.args.copy().to_dict()
        combined_args = dict(view_args.items() + args.items())
        if params:
            combined_args.update(params)
        return url_for(request.endpoint, **combined_args)

    def static(filename):
        """生成静态资源url"""
        return url_for('static', filename=filename)

    def javascript(filename):
        """生成静态资源url"""
        return url_for('javascript', filename=filename)

    def bower(filename):
        """生成bower资源url"""
        return static("bower_components/%s" % filename)

    def script(path):
        """生成script标签"""
        return Markup("<script type='text/javascript' src='%s'></script>" % static(path))

    def link(path):
        """生成link标签"""
        return Markup("<link rel='stylesheet' href='%s'></script>" % static(path))

    def register_vars(dict):
        """生成用于后台传值的meta标签"""
        meta = ''
        for key, value in dict.items():
            meta += '<meta type=pv name="%s" content="%s" />' % (key, value)
        return Markup(meta)

    from random import randint

    def random_num_str(length):
        """生成指定长度的随机数字字符串"""
        return ''.join(["%s" % randint(0, 9) for num in range(0, length)])

    app.jinja_env.globals['url_for_other_page'] = url_for_other_page
    app.jinja_env.globals['set_url_param'] = set_url_param
    app.jinja_env.globals['static'] = static
    app.jinja_env.globals['bower'] = bower
    app.jinja_env.globals['script'] = script
    app.jinja_env.globals['link'] = link
    app.jinja_env.globals['random_num_str'] = random_num_str
    app.jinja_env.globals['register_vars'] = register_vars

    @app.template_filter('get_name')
    def get_name(template_reference):
        template_name = template_reference._TemplateReference__context.name
        return "page-%s" % template_name.replace('/', '-').split('.')[0]


def register_logger(app):
    """日志记录"""
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler

        # 创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        rfh = RotatingFileHandler('%s/web.log' % app.config.get('PROJECT_PATH'), 'a',
                                  1 * 1024 * 1024, 10)
        rfh.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        rfh.setFormatter(formatter)

        # 给logger添加handler
        logger.addHandler(rfh)
        logger.info('start logging...')
        for item in sys.path:
            logger.info(item)


def register_db(app):
    """注册Model"""

    from .models import db

    db.init_app(app)


def register_routes(app):
    """注册路由"""
    from controllers import site, login_user

    app.register_blueprint(site.bp, url_prefix='')
    app.register_blueprint(login_user.bp, url_prefix='/login_user')


def register_error_handle(app):
    """添加HTTP错误页面"""

    @app.errorhandler(403)
    def page_403(error):
        return render_template('site/403.html'), 403

    @app.errorhandler(404)
    def page_404(error):
        return render_template('site/404.html'), 404

    @app.errorhandler(500)
    def page_500(error):
        return render_template('site/500.html'), 500


def register_uploadsets(app):
    """注册UploadSets"""
    from web.utils.uploadsets import avatars, images, \
        id_images

    configure_uploads(app, (avatars, images, id_images))
