#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TextAreaField, SelectField, PasswordField, RadioField, TextField, HiddenField, \
    IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, AnyOf, Length, Regexp, InputRequired


class OrderForm(Form):
    name = TextField('登录名:', validators=[DataRequired('用户名不能为空')])
    qq = TextField('qq:', validators=[DataRequired('用户名不能为空')])
    mobile = TextField('手机号:', validators=[DataRequired('手机号不能为空')])
    email = TextField('邮箱地址:', description="用于验证账户及找回密码", validators=[DataRequired('邮箱不能为空'), Email('无效的邮箱')])
    address = TextField('发货地址:', description="发货详细地址或所在省市", validators=[DataRequired('邮箱不能为空'), Email('无效的邮箱')])
    password = PasswordField('密码:', validators=[DataRequired('密码不能为空')])
    repassword = PasswordField('确认密码:', validators=[DataRequired('请再次输入密码'),
                                                    EqualTo('password', message='两次密码输入不一致')])
