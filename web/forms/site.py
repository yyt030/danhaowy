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
    qq = TextField('客服QQ', default='')
    logo = TextField('网站LOGO图片', default='logo.png')
    alipay = TextField('支付宝账号', default='')

class QQInfo(Form):
    qq1 = TextField('注册咨询', default='')
    qq2 = TextField('问题咨询', default='')
    qq3 = TextField('淘宝维权', default='')
    qq4 = TextField('投诉与建议', default='')


class PacketSettingForm(Form):
    packet_id = TextField('空包ID', default='')
    tracking_no = TextField('单号', default='')
    send_time = TextField('发货时间', default='')
