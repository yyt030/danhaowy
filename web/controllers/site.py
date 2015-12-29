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
from ..forms import SigninForm
from ..utils.permissions import require_user, require_visitor
from ..utils.uploadsets import images, random_filename, process_question, avatars

bp = Blueprint('site', __name__)


@bp.route('/', methods=['GET'])
def index():
    form = SigninForm()
    return render_template('site/index.html', form=form)


@bp.route('/banner', methods=['GET'])
def banner():
    return render_template('site/banner.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = SigninForm()
    if request.method == 'POST':
        name = form.username.data
        password = form.password.data
        print name, password
        if form.validate_on_submit():
            user = User.query.filter(User.name == name).first()
            if user:
                signin_user(user)
                tip = "用户%s登录成功！" % user.name
                return render_template('tip.html', tip=tip, error=False, url="")
        else:
            return render_template('tip.html', error=True, tip="请仔细填写您的账号密码，如果忘记，请返回点击找回密码选项，或者联系客服！", url="login")
    else:

        return render_template('login.html', form=form)


@bp.route('/get_pass', methods=['GET', 'POST'])
@require_visitor
def GetPass():
    """找回密码"""
    return render_template('site/get_pass.html')


@bp.route('/reg', methods=['GET', 'POST'])
def reg():
    """注册"""
    if g.user:
        error = "您已经登录，不能注册账号！当前登录账号:%s" % g.user.name
        return render_template('error.html', error=error, url="/")
    return render_template('site/reg.html')


@bp.route('/signout', methods=['GET', 'POST'])
@require_visitor
def signout():
    signout_user()
    return redirect(url_for('site.index'))


@bp.route('/home', methods=['GET', 'POST'])
@require_user
def home():
    return render_template('account/home.html')


@bp.route('/user_data', methods=['GET', 'POST'])
@require_user
def user_data():
    return render_template('account/user_data.html')


@bp.route('/resource/<string:folder1>/<string:filename>', defaults={"folder2": "", "folder3": ""}, methods=['GET'])
@bp.route('/resource/<string:folder1>/<string:folder2>/<string:filename>', defaults={"folder3": ""}, methods=['GET'])
@bp.route('/resource/<string:folder1>/<string:folder2>/<string:folder3>/<string:filename>', methods=['GET'])
def get_resourse(folder1, folder2, folder3, filename):
    if folder3 == "":
        BASE_URL = os.path.join(current_app.config.get('PROJECT_PATH'), 'resource/%s/%s') % (folder1, folder2)
        # print BASE_URL
        # print filename
    else:
        BASE_URL = os.path.join(current_app.config.get('PROJECT_PATH'), 'resource/%s/%s/%s') % (
            folder1, folder2, folder3)
    ext = os.path.splitext(filename)[1][1:]
    mimetypes = {"jpg": 'image/jpg', "css": 'text/css', "png": "image/png", "js": 'application/x-javascript',
                 "xml": 'application/xHTML+XML'}
    return send_from_directory(BASE_URL, filename, mimetype=mimetypes.get(ext))
