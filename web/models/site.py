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
