#!/usr/bin/env python
# coding: utf8

__author__ = 'yueyt'

from datetime import datetime

from . import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_no = db.Column(db.String(100), unique=True, index=True, nullable=False)
    # 发货时间
    send_timestamp = db.Column(db.DateTime, default=datetime.now)
    # 发收货地址
    send_addr_province = db.Column(db.String(20))
    send_addr_city = db.Column(db.String(20))
    send_addr_county = db.Column(db.String(20))
    recv_addr_province = db.Column(db.String(20))
    recv_addr_city = db.Column(db.String(20))
    recv_addr_county = db.Column(db.String(20))
    recv_desc = db.Column(db.Text)
    tracking_company = db.Column(db.String(20), nullable=False)
    is_scan = db.Column(db.SmallInteger, default=0, nullable=False)

    # 是否出售
    is_sell = db.Column(db.SmallInteger, default=0, nullable=False)

    # 发布单号用户
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller = db.relationship('User', primaryjoin='User.id == Order.seller_id',
                             backref=db.backref('sell_orders', lazy='dynamic'))
    # 佣金余额
    seller_left_money = db.Column(db.Float, default=0.0, nullable=False)

    # 购买单号用户
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    buyer = db.relationship('User', primaryjoin='User.id == Order.buyer_id',
                            backref=db.backref('buy_orders', lazy='dynamic'))
    # 购买时间
    buy_time = db.Column(db.DateTime, default=datetime.now)

    # 录入时间
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    scan_time = db.Column(db.DateTime, default=datetime.now)
    # 单号价格
    price = db.Column(db.Float, nullable=False, default=0.5)

    @property
    def create_date(self):
        return self.create_time.date()

    @property
    def tracking_company_cn(self):
        com = {
            "yunda": u'韵达',
            "yuantong": u'圆通',
            "shentong": u'申通',
            "zhongtong": u'中通',
            "quanfeng": u'全峰',
            "huitong": u'汇通',
            "ems": 'EMS',
            "shunfeng": u'顺丰',
            "bgpyghx": u'邮政包裹',
            "yousu": u'优速',
            "tiantian": u'天天',
            "ems2": u'EMS经济',
            "zjs": u'宅急送',
            "kuaijie": u'快捷'
        }
        return com[self.tracking_company]

    @property
    def plan_scan_time(self):
        return '%s %s' % (self.create_time.date(), '19:00:00')

    @property
    def real_price(self):
        # 非扫描单号价格0.5 ,　扫描价格0.25
        if self.is_scan == 0:
            return self.price
        else:
            return self.price / 2

    @property
    def profit(self):
        # 每个单号卖家能获取0.95的钱
        return self.real_price * 0.95

    @property
    def tracking_no_sub(self):
        return '%s**' % (str(self.tracking_no)[:2])

    @property
    def seller_id_sub(self):
        return '%s**' % (str(self.seller_id)[:2])

    @property
    def seller_name_sub(self):
        return '%s**' % (str(self.seller.name)[:2])

    def __repr__(self):
        return '<Order %r>' % self.tracking_no


class OrderList(db.Model):
    """订单领取"""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.ForeignKey('order.id', ondelete='CASCADE'), nullable=False)
    order = db.relationship('Order', backref=db.backref('order_list', lazy='dynamic'))
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('order_lists', lazy='dynamic'))
    create_time = db.Column(db.DateTime, default=datetime.now)

    @property
    def create_date(self):
        return self.create_time.date()

    def __repr__(self):
        return '<OrderList %r>' % self.id
