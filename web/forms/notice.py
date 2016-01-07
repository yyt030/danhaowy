#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import g
from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TextAreaField, SelectField, PasswordField, RadioField, TextField, HiddenField, \
    IntegerField
from wtforms.validators import DataRequired, Regexp, EqualTo, InputRequired


class NoticeForm(Form):
    title = TextField('标题', default='')
    desc = TextField('详情', default='')