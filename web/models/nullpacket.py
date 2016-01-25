#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from datetime import datetime

from . import db


class NullPacket(db.Model):
    """空包"""
    id = db.Column(db.Integer, primary_key=True)
    express_id = db.Column(db.Integer, db.ForeignKey('express.id'))
    express = db.relationship('Express', backref=db.backref('nullpackets', lazy='dynamic'))

    tracking_no = db.Column(db.String(100), unique=True, index=True)
    price = db.Column(db.Float)

    # 下单时间
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    create_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_user = db.relationship('User', backref=db.backref('nullpackets', lazy='dynamic'))

    # 发收货地址
    send_user_name = db.Column(db.String(20))
    send_user_mobile = db.Column(db.String(11))
    send_addr_province = db.Column(db.String(20))
    send_addr_city = db.Column(db.String(20))
    send_addr_county = db.Column(db.String(20))
    send_addr_detail = db.Column(db.Text)

    recv_user_name = db.Column(db.String(20))
    recv_user_mobile = db.Column(db.String(11))
    recv_addr_province = db.Column(db.String(20))
    recv_addr_city = db.Column(db.String(20))
    recv_addr_county = db.Column(db.String(20))
    recv_addr_detail = db.Column(db.Text)
    recv_addr_postcode = db.Column(db.String(10))

    # 空包状态
    status = db.Column(db.SmallInteger, default=0)
    # 发货时间
    send_time = db.Column(db.DateTime)

    @property
    def curr_status(self):
        status_list = {
            0: u'等待发货',
            1: u'已发货',
        }
        return status_list.get(self.status, 0)

    def __repr__(self):
        return '<NullPacket %r>' % self.id


class SendAddr(db.Model):
    """空包默认发货地址"""
    id = db.Column(db.Integer, primary_key=True)
    send_user_name = db.Column(db.String(20))
    send_user_mobile = db.Column(db.String(11))
    send_addr_province = db.Column(db.String(20))
    send_addr_city = db.Column(db.String(20))
    send_addr_county = db.Column(db.String(20))
    send_addr_detail = db.Column(db.Text)
    is_default = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('sendaddrs', lazy='dynamic'))

    create_time = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<SendAddr %r>' % self.id


class Express(db.Model):
    """快递公司"""
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), nullable=False)
    content = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, default=0.0)
    status = db.Column(db.SmallInteger, default=1)
