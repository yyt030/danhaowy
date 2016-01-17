# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from flask import render_template, Blueprint, redirect, url_for, g, session, request, \
    make_response, current_app, send_from_directory
from web.utils.account import signin_user, signout_user
from ..models import db, User, Notice
from ..forms import SigninForm, RegisterForm
from ..utils.permissions import require_user, require_visitor
from datetime import datetime

bp = Blueprint('site', __name__)


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    form = SigninForm()
    user = g.user
    return render_template('site/index.html', form=form, user=user)


@bp.route('/banner', methods=['GET'])
def banner():
    return render_template('site/banner.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = SigninForm()
    user = g.user
    if request.method == 'POST':
        value = form.username.data
        password = form.password.data
        if form.validate_on_submit():
            loginType = request.form.get('loginType')
            if loginType == 'uname':
                user = User.query.filter(User.name == value).first()
            elif loginType == 'mobile':
                user = User.query.filter(User.mobile == value).first()
            elif loginType == 'email':
                user = User.query.filter(User.email == value).first()
            else:
                user = User.query.filter(User.name == value).first()

            if user is not None and user.check_password(password):
                signin_user(user)
                user.address = request.headers.get('X-Real-Ip', request.remote_addr)
                user.login_time = datetime.now()
                db.session.add(user)
                db.session.commit()
                tip = "用户%s登录成功！" % user.name
                return render_template('tip.html', tip=tip, error=False, url="")
            else:
                error = "用户名或密码错误"
                return render_template('error.html', error=error, url="")
        else:
            return render_template('tip.html', error=True, tip="请仔细填写您的账号密码，如果忘记，请返回点击找回密码选项，或者联系客服！", url="login")
    else:

        return render_template('login.html', form=form, user=user)


@bp.route('/get_pass', methods=['GET', 'POST'])
@require_visitor
def GetPass():
    """找回密码"""
    return render_template('site/get_pass.html')


@bp.route('/reg', methods=['GET', 'POST'])
def reg():
    """注册ajax 校验
        http://localhost:5000/ajax.asp?c=user&clientid=username
        &rand=1451397827713&username=asfasf123123
        &Email=@&QQ=&sj=&_=1451397819278
        """
    form = RegisterForm()
    # if g.user:
    #     error = "您已经登录，不能注册账号！当前登录账号:%s" % g.user.name
    #     return render_template('error.html', error=error, url="/")
    if request.method == 'GET':
        clientid = request.args.get('clientid', '')
        res = ''
        if clientid == 'username':
            res = User.query.filter(User.name == request.args.get(clientid)).first()
        if clientid == 'email':
            res = User.query.filter(User.email == request.args.get(clientid)).first()
        if clientid == 'qq':
            res = User.query.filter(User.qq == request.args.get(clientid)).first()
        if clientid == 'sj':
            res = User.query.filter(User.mobile == request.args.get(clientid)).first()
        if res:
            return '0'

    if request.method == 'POST':
        user = User()
        user.name = request.form.get('username')
        user.email = request.form.get('Email')
        user.qq = request.form.get('QQ')
        user.password = request.form.get('password1')
        user.hash_password()
        user.mobile = request.form.get('sj')

        if User.query.filter(User.name == user.name).first():
            error = "用户名已存在:%s" % user.name
            return render_template('error.html', error=error, url="/")

        db.session.add(user)
        db.session.commit()
        return render_template('tip.html', tip="注册成功，请返回首页登录:%s" % user.name, error=False, url="/")
    return render_template('site/reg.html', form=form)


@bp.route('/news', methods=['GET', 'POST'])
@require_visitor
def news():
    id = request.args.get("id", type=int)
    type = request.args.get("type", "news")
    if id:
        info = Notice.query.get_or_404(id)
    else:
        info = {}
    return render_template('site/news_detail.html', info=info)


@bp.route('/news_list', methods=['GET', 'POST'])
@require_visitor
def news_list():
    type = request.args.get("type", "news")
    if type:
        info = Notice.query.filter(Notice.type == type)
    else:
        info = {}
    return render_template('site/news_list.html', info=info)


@bp.route('/signout', methods=['GET', 'POST'])
@require_visitor
def signout():
    signout_user()
    return redirect(url_for('site.index'))


@bp.route('/loginout')
def loginout():
    signout_user()
    return redirect(url_for('site.index'))


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
