#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'
from datetime import datetime

from . import db


class Paylog(db.Model):
    """充值记录"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    money = db.Column(db.Float, nullable=False)
    # 订单号
    seq_no = db.Column(db.Integer, nullable=False)
    # 支付宝交易号
    alipay_no = db.Column(db.String(50))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # 充值状态
    status = db.Column(db.Enum('已支付', '待确认', '未支付'), default='已支付')
    # 记录内容
    action = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('paylogs', lazy='dynamic'))

    def __repr__(self):
        return '<Paylog %r>' % self.id


class Fundslog(db.Model):
    """资金日志"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    change_wuyoubi = db.Column(db.Integer, default=0)
    change_wuyoujifen = db.Column(db.Integer, default=0)
    left_wuyoubi = db.Column(db.Integer, default=0)
    left_wuyoujifen = db.Column(db.Integer, default=0)
    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('fundslogs', lazy='dynamic'))
    # 记录内容
    action = db.Column(db.String(30), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return '<Fundslog %r>' % self.id


class Txlog(db.Model):
    """提现记录"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    money = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('txlogs', lazy='dynamic'))
    status = db.Column(db.Enum('0', '1', '2'), default='0')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @property
    def get_status(self):
        s = {
            '0': u'提现冻结',
            '1': u'提现成功',
            '2': u'提现失败'
        }
        return s[self.status]
