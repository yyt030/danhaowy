#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import g
from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TextAreaField, SelectField, PasswordField, RadioField, TextField, HiddenField, \
    IntegerField
from wtforms.validators import DataRequired, Regexp, EqualTo, InputRequired


class SiteInfo(Form):
    url = TextField('网站网址', default='')
    name = TextField('网站名称', default='')
    logo = TextField('网站LOGO图片', default='logo.png')
    alipay = TextField('支付宝账号', default='')


