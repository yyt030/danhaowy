# !/usr/bin/env python
# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
import time
import json
import os
import string
import re, urllib2
import random
from PIL import Image
from coverage.html import STATIC_PATH
from flask import render_template, Blueprint, redirect, url_for, g, session, request, \
    make_response, current_app, send_from_directory
from web import csrf
from web.utils.account import signin_user, signout_user
from ..models import db, User
from ..forms import SigninForm, RegisterForm
from web.utils.permissions import require_user

bp = Blueprint('login_user', __name__)


@bp.route('/', methods=['GET'])
@bp.route('/user', methods=['GET'])
@require_user
def index():
    form = SigninForm()
    return render_template('login_user/index.html', form=form)


@bp.route('/ornumber', methods=['GET'])
@require_user
def ornumber():
    """单号领取"""
    form = SigninForm()
    return render_template('login_user/ornumber.html', form=form)


@bp.route('/ornumber', methods=['GET'])
@require_user
def shopnumber():
    """单号购买"""
    form = SigninForm()
    return render_template('site/index.html', form=form)


@bp.route('/ornumber', methods=['GET'])
@require_user
def seller():
    """发布单号"""
    form = SigninForm()
    return render_template('site/index.html', form=form)


@bp.route('/ornumber', methods=['GET'])
@require_user
def buykongbao():
    """空包大厅"""
    form = SigninForm()
    return render_template('site/index.html', form=form)


@bp.route('/tuiguang', methods=['GET'])
@require_user
def tuiguang():
    """推广大厅"""
    form = SigninForm()
    return render_template('site/index.html', form=form)


@bp.route('/paywyb', methods=['GET'])
@require_user
def paywyb():
    """账号充值"""
    form = SigninForm()
    return render_template('site/index.html', form=form)


@bp.route('/upseller', methods=['GET'])
@require_user
def upseller():
    """发布单号"""
    form = SigninForm()
    return render_template('login_user/upseller.html', form=form)


@bp.route('/woyaojihuo', methods=['GET'])
@require_user
def woyaojihuo():
    """激活账号"""
    return render_template('login_user/woyaojihuo.html')


@bp.route('/chgpwd', methods=['GET', 'POST'])
@require_user
def chgpwd():
    form = RegisterForm()
    user = g.user
    if request.method == 'POST':
        password = request.form.get('password')
        newpassword = request.form.get('newpassword')
        newpassword2 = request.form.get('newpassword2')
        if user.check_password(password):
            error = "用户名或密码错误"
            return render_template('error.html', error=error, url="")
        if newpassword != newpassword2:
            error = "新密码不一致"
            return render_template('error.html', error=error, url="")
        user.password = newpassword
        user.hash_password()
        db.session.add(user)
        db.session.commit()
        tip = "用户%s修改密码成功！" % user.name
        return render_template('error.html', error=tip, url="")
    return render_template('login_user/chgpwd.html', form=form, user=user)
