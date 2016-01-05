#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from . import db
from datetime import datetime


class Notice(db.Model):
    """
    type = 新手帮助，　网站新闻，　热门文章
       subtype ,子类型，可编辑
    """
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum('新手帮助', '网站新闻', '热门文章'), default='新手帮助')
    subtype = db.Column(db.String(10))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('user_notices', lazy='dynamic'))

    def __repr__(self):
        print '<%r>' % self.__class__.__name__
