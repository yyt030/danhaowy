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
from wechat_sdk import WechatBasic
from weshop import csrf
from weshop.utils.account import signin_user, signout_user
from ..models import db, User, Discount, Brand, MyFavoriteBrand, Shop, Profile, GetTicketRecord
from ..forms import SigninForm
from ..utils.permissions import require_user, require_visitor
from ..utils.uploadsets import images, random_filename, process_question, avatars
from weshop.utils.helper import get_url_data
from weshop.wechat import WeixinHelper
from weshop.wechat.backends.flask_interface import wechat_login

bp = Blueprint('site', __name__)


@bp.route('/', methods=['GET'])
def index():
    return render_template('site/index.html')


@bp.route('/login', methods=['GET', 'POST'])
@require_visitor
def login():
    form = SigninForm()
    name = form.username.data
    if form.validate_on_submit():
        user = User.query.filter(User.name == name).first()
        if user:
            signin_user(user)
            return redirect(url_for('site.home'))
    return render_template('account/login.html', form=form)


@bp.route('/signin', methods=['GET', 'POST'])
@require_visitor
def signin():
    return render_template('account/user_data.html')


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


@bp.route('/switch_city/<int:city_id>')
def switch_city(city_id):
    """切换城市"""
    city = City.query.get_or_404(city_id)
    session['city'] = city.name
    session['city_id'] = city.id
    session['province_id'] = city.province_id
    return redirect(request.referrer or url_for('site.index'))


@bp.route('/get_resource')
def crossdomain_xml():
    """生成用于Flash跨域脚本的xml文件"""
    sitemap_xml = render_template('site/crossdomain.xml')
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response


@bp.route('/test')
def test():
    return str(zip(session.keys(), session.values()))

