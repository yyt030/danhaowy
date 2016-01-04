#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from . import db
from datetime import datetime
from .shoplog import ShopLog


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    tracking_no = db.Column(db.String(100), unique=True, index=True)
    send_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    send_addr_province = db.Column(db.String(20))
    send_addr_city = db.Column(db.String(20))
    send_addr_county = db.Column(db.String(20))
    recv_addr_province = db.Column(db.String(20))
    recv_addr_city = db.Column(db.String(20))
    recv_addr_county = db.Column(db.String(20))
    recv_desc = db.Column(db.Text)
    tracking_company = db.Column(db.String(20))
    is_scan = db.Column(db.SmallInteger, default=0)
    is_sell = db.Column(db.SmallInteger, default=0)

    @property
    def seller(self):
        return self.shoplog.order_by(ShopLog.create_at.desc()).first()

    def __repr__(self):
        return '<Order %r>' % self.tracking_no
