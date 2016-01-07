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

    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<MailBox %r>' % self.id
