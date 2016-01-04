#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from . import db
from datetime import datetime


class ShopLog(db.Model):
    __tablename__ = 'shopLogs'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(15))
    remark = db.Column(db.Text)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)

    tracking_no = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship('Order', backref=db.backref('shoplog', lazy='dynamic'))

    def __repr__(self):
        return '<ShopLog %r>' % self.id
