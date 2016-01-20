# coding: utf-8
import os
# import daemon
from flask.ext.script import Manager
import random
from web import create_app
from web.models import db, User, Express
from web import create_app
from flask.ext.migrate import Migrate, MigrateCommand
from web.models import db

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    """启动网站"""
    app.run(host="localhost", port=5000, threaded=True)


@manager.command
def run_80():
    """启动网站"""
    app.run(host="0.0.0.0", port=80)


@manager.command
def create_admin():
    """Create admin."""

    user = User(name="admin", role="admin",qq=123456789, email="admin@qq.com", mobile="18812345678", address='localhost')

    user.password = "admin"
    user.hash_password()
    user.gene_token()
    db.session.add(user)
    db.session.commit()


@manager.command
def update_pwd():
    """reset admin pwd"""

    user = User.query.first()
    user.password = "admin"
    user.hash_password()
    user.gene_token()
    db.session.add(user)
    db.session.commit()


@manager.command
def createdb():
    """Create database."""
    db.create_all()


@manager.command
def reset_users_token():
    with app.app_context():
        for u in User.query:
            u.gene_token()
            db.session.add(u)
            db.session.commit()


@manager.command
def create_express():
    express_dict = {
        "35": (2.2, '天天快递', '天天快递(全国发全国)物流仅支持 淘宝 天猫 天天官网 查询物流，不支持 阿里 京东发货，下单后请立即发货。'),
        "40": (2, '优速快递', '优速快递(全国发全国)物流仅支持 淘宝 天猫 天天官网 查询物流，不支持 阿里 京东发货，下单后请立即发货。'),
        "26": (2, '快捷快递', '快捷快递(全国发全国)物流仅支持 淘宝 快捷官网，不支持京东 等其他第三方平台，*当天下单延迟1天出物流，介意的请勿下单！'),
        "10": (2.1, '龙邦快递', '龙邦快递(全国发全国)物流仅支持 淘宝 京东，不支持 阿里 等其他第三方平台，收发地址支持全国，下单后请立即发货。'),
        "34": (2, '飞远(爱彼西)', '飞远(爱彼西)配送(全国发全国)物流仅支持 淘宝 不支持飞远官网 阿里 京东等其他平台，收发地址支持全国 *非淘宝请勿下单'),
        "36": (2, '全峰快递', '全峰快递(京东专用)物流仅支持 京东 全峰官网 等其他第三方平台，淘宝禁止下单，收发地址 西藏 港澳台禁止下单(无网点)。'),
        "39": (2, '申通快递', '申通快递(全国发全国)物流仅支持 淘宝 天猫 申通官网 查询物流，不支持 阿里 京东发货，下单后请立即发货。')

    }
    for key in express_dict.iterkeys():
        express = Express(id=key, price=express_dict[key][0], type=express_dict[key][1], content=express_dict[key][2])
        db.session.add(express)
    db.session.commit()


if __name__ == "__main__":
    manager.run()
