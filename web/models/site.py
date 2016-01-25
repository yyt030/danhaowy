#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime
from . import db


class Site(db.Model):
    """站点信息"""
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100), default='')
    name = db.Column(db.String(100), default='')
    sitelogo = db.Column(db.String(100))
    title = db.Column(db.String(100), default='')
    alipay=db.Column(db.String(100), default='')

    def __repr__(self):
        return '<Site %s>' % self.url

class qqKefu(db.Model):
    """QQ客服"""
    id = db.Column(db.Integer, primary_key=True)
    qq1 = db.Column(db.String(20), default='')
    qq2 = db.Column(db.String(20), default='')
    qq3 = db.Column(db.String(20), default='')
    qq4 = db.Column(db.String(20), default='')


    def __repr__(self):
        return '<QQkefu %s>' % self.id