# !/usr/bin/env python
# -*- coding: UTF-8 -*-
from datetime import datetime

from werkzeug import security
from . import db
from ..utils._redis import get_user_active_time


class User(db.Model):
    """用户：id，姓名，邮箱，密码，角色，创建时间，token
    角色：　admin
        　 member
        is_active 会员激活状态
        money 提现佣金
        address: 登录Ip
        wuyoubi 无忧币
        wuyoujifen 无忧积分
        jifen 发布积分
        role 当前等级
        max_order_num 每日可领取单号
        login_time 登录时间
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    qq = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    mobile = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(20))
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default='member')
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 是否激活
    is_active = db.Column(db.Boolean, default=False)
    # 是否卖家
    is_seller = db.Column(db.Boolean, nullable=False, default=False)
    token = db.Column(db.String(20), default='')
    money = db.Column(db.Float, default=0.0)

    fabujifen = db.Column(db.Float, nullable=False, default=0.0)

    wuyoubi = db.Column(db.Float, default=0)
    wuyoujifen = db.Column(db.Integer, default=0)
    max_order_num = db.Column(db.Integer, nullable=False, default=10)
    login_time = db.Column(db.DateTime, default=datetime.now)

    # 卖家中心设置默认发货城市
    send_addr_province = db.Column(db.String(20))
    send_addr_city = db.Column(db.String(20))
    send_addr_county = db.Column(db.String(20))

    # 空包中心　默认快递类型
    default_express_id = db.Column(db.Integer, db.ForeignKey('express.id'))
    default_express = db.relationship('Express', backref=db.backref('users', lazy='dynamic'))

    # 支付宝账户，姓名
    alipay_name = db.Column(db.String(50), default='')
    alipay_account = db.Column(db.String(50), default='')

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

    @property
    def is_active_num(self):
        if self.is_active == True:
            return 1
        else:
            return 0

    @property
    def role_name(self):
        roles = {"admin": u'管理员', "member": u'普通会员', "seller": u"普通卖家", "super_seller": u"超级卖家"}
        return roles.get(self.role)

    def __repr__(self):
        return '<User %r %r>' % (self.name, self.id)


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
    subscribe_time = db.Column(db.DateTime, default=datetime.now)
