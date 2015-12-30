#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import g
from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TextAreaField, SelectField, PasswordField, RadioField, TextField, HiddenField, \
    IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, AnyOf, Length, Regexp, InputRequired
from ..models import User
from sqlalchemy import or_


class PayForm(Form):
    month = SelectField('充值时长', validators=[DataRequired('充值时长不能为空')],
                        choices=[(i, "%d个月" % i) for i in range(1, 13)], coerce=int)


class ChangePwdForm(Form):
    """Form for change password"""
    old_password = PasswordField('原密码', validators=[DataRequired('原密码不能为空')])
    new_password = PasswordField('新密码', validators=[DataRequired('新密码不能为空')])
    re_new_password = PasswordField('重复新密码', validators=[
        DataRequired('请再次输入新密码'),
        EqualTo('new_password', message='两次密码输入不一致')
    ])

    # 验证用户名是否重复
    def validate_old_password(self, field):
        if not g.user.check_password(field.data):
            raise ValueError('密码错误')


class SearchUserForm(Form):
    name = TextField('姓名', validators=[DataRequired()])


class UploadForm(Form):
    photo_types = (("0", "消费环境"), ("1", "菜品介绍"), ("2", "服务项目"), ("3", "套餐说明"), ("4", "营销广告"))
    types = SelectField("类型", choices=photo_types)


class SigninForm(Form):
    """登陆表单"""
    username = TextField('登录名:', validators=[DataRequired(u'邮箱不能为空')], description=u'用户名、QQ、邮件地址或手机号')
    password = PasswordField('密码:', validators=[DataRequired(u'密码不能为空')], description=u'密码')

    # 验证密码
    def validate_password(self, field):
        name = self.username.data.replace(' ', '')
        user = User.query.filter(or_(User.name == name, User.email == name, User.mobile == name)).first()

        if not user:
            raise ValueError(u'账户或密码错误')

        if user.check_password(field.data):
            self.user = user
        else:
            raise ValueError(u'账户或密码错误')


class RegisterForm(Form):
    """注册表单"""
    returnFlag = False
    name = TextField('登录名:', validators=[DataRequired('用户名不能为空')])
    qq = TextField('qq:', validators=[DataRequired('用户名不能为空')])
    mobile = TextField('手机号:', validators=[DataRequired('手机号不能为空')])
    email = TextField('邮箱地址:', description="用于验证账户及找回密码", validators=[DataRequired('邮箱不能为空'), Email('无效的邮箱')])
    address = TextField('发货地址:', description="发货详细地址或所在省市", validators=[DataRequired('邮箱不能为空'), Email('无效的邮箱')])
    password = PasswordField('密码:', validators=[DataRequired('密码不能为空')])
    repassword = PasswordField('确认密码:', validators=[DataRequired('请再次输入密码'),
                                                    EqualTo('password', message='两次密码输入不一致')])

    # 验证用户名是否重复
    def validate_name(self, field):
        if field.data == '':
            raise ValueError('用户名不能为空')

    # 验证密码是否重复
    def validate_email(self, field):
        field.data = field.data.lower()
        field.data = field.data.replace(' ', '')
        if User.query.filter(User.email == field.data).count() > 0:
            raise ValueError('邮箱已存在')
