#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from . import db
from datetime import datetime


class Notice(db.Model):
    """
    type = 新手帮助，　网站新闻
    """
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(50),default='')
    type = db.Column(db.Enum('help', 'news', 'article'),default='news')

    desc = db.Column(db.Text)
    visit =db.Column(db.Integer,default=0)
    create_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        print '<%r>' % self.__class__.__name__

