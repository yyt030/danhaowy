#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from . import db
from . import User

from datetime import datetime


class MailBox(db.Model):
    """ 站内信箱
    """
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text)
    sender_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    sender = db.relationship('User', primaryjoin='User.id == MailBox.sender_id',
                             backref=db.backref('mailboxs_sender', lazy='dynamic'))

    recver_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    recver = db.relationship('User', primaryjoin='User.id == MailBox.recver_id',
                             backref=db.backref('mailboxs_recver', lazy='dynamic'))

    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    result = db.Column(db.String(10))
    msg_type = db.Column(db.String(10), nullable=False, default='通知')

    def __repr__(self):
        return '<MailBox %r>' % self.id


class ApplySellerRecord(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', primaryjoin='User.id == ApplySellerRecord.user_id',
                             backref=db.backref('apply_seller_users', lazy='dynamic'))
    qq = db.Column(db.String(20))
    email = db.Column(db.String(20))
    typ = db.Column(db.Integer,default=500)
    processed = db.Column(db.Float, default=False)
    passed=db.Column(db.Float, default=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    def __repr__(self):
        return '<ApplySellerRecord %r>' % self.id