# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime
import random
import hashlib
import time
from werkzeug import security
from . import db
from ..utils.uploadsets import avatars, id_images, student_images, teacher_images, honor_images
from ..utils._redis import get_user_active_time


class User(db.Model):
    """用户：id，姓名，邮箱，密码，角色，创建时间，token
    角色：　admin
        　 member
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    qq = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    mobile = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(20))
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default='member')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    is_active = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(20), default='')
    money = db.Column(db.Float(10, 2), default=0.0)

    jifen = db.Column(db.Float(10, 2), default=0.0)

    wuyoubi = db.Column(db.Integer, default=0)
    wuyoujifen = db.Column(db.Integer, default=0)

    default_send_province = db.Column(db.String(20))
    default_send_city = db.Column(db.String(20))
    default_send_county = db.Column(db.String(20))

    @property
    def active_time(self):
        """从Redis中获取用户最后活跃时间，若不存在，则返回当前时间"""
        ac_time = get_user_active_time(self.id)
        return ac_time if ac_time else datetime.datetime.now()

    @property
    def is_admin(self):
        """判断是否为管理员"""
        return self.role == 'admin'

    @property
    def is_shopper(self):
        """判断是否为顾客"""
        return self.role == 'shopper'

    def hash_password(self):
        """对原始密码进行哈希计算"""
        self.password = security.generate_password_hash(self.password)

    def gene_token(self):
        """生成用户token"""
        self.token = security.gen_salt(20)

    def check_password(self, password):
        """检查密码是否正确"""
        return security.check_password_hash(self.password, password)

    def get_user_info_dict(self):
        ret = {}
        ret['uid'] = self.id
        ret['role'] = self.role
        ret['name'] = self.name

        return ret

    def __repr__(self):
        return '<User %r>' % self.name


class Profile(db.Model):
    """用户详细信息"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('profile', lazy='dynamic'))
    openid = db.Column(db.String(50), default='')
    city = db.Column(db.String(50), default='')
    country = db.Column(db.String(50), default='cn')
    headimgurl = db.Column(db.String(200), default='')
    language = db.Column(db.String(20))
    nickname = db.Column(db.String(50))
    province = db.Column(db.String(50))
    subscribe_time = db.Column(db.DateTime, default=datetime.datetime.now)
