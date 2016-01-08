#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from . import db
from datetime import datetime


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_no = db.Column(db.String(100), unique=True, index=True, nullable=False)
    # 发货时间
    send_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
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

    # 购买单号用户
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    buyer = db.relationship('User', primaryjoin='User.id == Order.buyer_id',
                            backref=db.backref('buy_orders', lazy='dynamic'))
    # 购买时间
    buy_time = db.Column(db.DateTime, default=datetime.now)

    # 录入时间
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return '<Order %r>' % self.tracking_no
