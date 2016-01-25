# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import StringIO
import hashlib
import json
from datetime import datetime

from flask import render_template, Blueprint, redirect, url_for, g, session, request, \
    make_response
from web import csrf
from web.utils.account import signin_user, signout_user
from web.utils.code2 import getCodePiture
from web.utils.uploadsets import process_question, images
from ..forms import SigninForm, RegisterForm
from ..models import db, User, Notice, Paylog, Order
from ..utils.permissions import require_visitor, require_admin

bp = Blueprint('site', __name__)


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    form = SigninForm()
    user = g.user
    orders = Order.query.limit(30)
    helps = Notice.query.filter(Notice.type == 'help').limit(10)
    notices = Notice.query.filter(Notice.type == 'news').limit(10)
    hot_articles = Notice.query.order_by(Notice.visit.desc()).limit(10)
    return render_template('site/index.html', form=form, orders=orders, helps=helps, notices=notices,
                           hot_articles=hot_articles,
                           user=user)


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
@bp.route('/getpass', methods=['GET', 'POST'])
def get_pass():
    """找回密码: 1"""
    form = RegisterForm()
    return render_template('site/get_pass.html', form=form)


@bp.route('/GetPasstwo', methods=['GET', 'POST'])
def get_pass_two():
    """找回密码: 2"""
    form = RegisterForm()
    name = request.form.get('username', '')
    if name:
        user = User.query.filter(User.name == name).first()
        if not user:
            return render_template('tip.html', error=True, tip="没有该用户!", url="login")
        else:
            session['reset_username'] = name

    return render_template('site/get_pass_two.html', form=form)


@bp.route('/GetPassthree', methods=['GET', 'POST'])
def get_pass_three():
    """找回密码: 3"""
    form = RegisterForm()
    email = request.form.get('Email')
    # 页面传来的是手机号
    mobile = request.form.get('QQ')
    query = User.query.filter(User.name == session['reset_username'])

    if email:
        query = query.filter(User.email == email)
    if mobile:
        query = query.filter(User.mobile == mobile)
    if not email and not mobile:
        return render_template('tip.html', error=True, tip="邮箱或手机号错误!", url="login")

    if not query.first():
        return render_template('tip.html', error=True, tip="邮箱或手机号错误!", url="login")
    else:
        return render_template('tip.html', error=False, tip="重置成功，请检查邮件!", url="login")

    return redirect(url_for('.login'))


@bp.route('/Getuser', methods=['GET', 'POST'])
@bp.route('/get_user')
def get_user():
    """找回密码: 3"""
    form = RegisterForm()
    if request.method == 'POST':
        email = request.form.get('usermail')
        mobile = request.form.get('usermob')
        if email and mobile:
            user = User.query.filter(User.email == email, User.mobile == mobile).first()
            if user:
                return render_template('tip.html', error=False, tip="账户[%s],请牢记！" % user.name, url="login")
            else:
                return render_template('tip.html', error=True, tip="输入错误!", url="login")
        else:
            return render_template('tip.html', error=True, tip="输入错误!", url="login")

    return render_template('site/get_user.html', form=form)


@bp.route('/reg', methods=['GET', 'POST'])
def reg():
    """注册ajax 校验
        http:#localhost:5000/ajax.asp?c=user&clientid=username
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

@bp.route('/news_list', methods=['GET', 'POST'])
@require_visitor
def news_list():
    type = request.args.get("type", "news")
    if type:
        if type != 'hot':
            info = Notice.query.filter(Notice.type == type)
        else:
            info = Notice.query.order_by(Notice.visit.desc())

    else:
        info = {}
    return render_template('site/news_list.html', info=info)


@bp.route('/News', methods=['GET', 'POST'])
@bp.route('/news', methods=['GET', 'POST'])
@require_visitor
def news():
    id = request.args.get("id", type=int)
    type = request.args.get("type", "news")
    if id:
        info = Notice.query.get_or_404(id)
        if info.visit ==None:
            info.visit=1
        else:
            info.visit+=1
        db.session.add(info)
        db.session.commit()
    else:
        info = {}
    return render_template('site/news_detail.html', info=info)



@bp.route('/signout', methods=['GET', 'POST'])
@require_visitor
def signout():
    signout_user()
    return redirect(url_for('site.index'))


@bp.route('/loginout')
def loginout():
    signout_user()
    return redirect(url_for('site.index'))


@bp.route('/checkcode', methods=['GET'], defaults={"code": None})
@bp.route('/checkcode/<string:code>', methods=['GET'])
def get_code(code):
    # 把strs发给前端,或者在后台使用session保存
    mstream = StringIO.StringIO()
    # validate_code = create_validate_code()
    validate_code = getCodePiture()

    img = validate_code[0]
    img.save(mstream, "GIF")
    session['validate'] = validate_code[1]
    # print session['validate']
    # return (mstream.getvalue(), "image/gif")
    response = make_response(mstream.getvalue())
    response.headers['Content-Type'] = 'image/gif'
    return response


@csrf.exempt
@bp.route('/upload_image', methods=['POST'])
@require_admin
def upload_image():
    try:
        filename = process_question(request.files['file'], images, "")
    except Exception, e:
        return json.dumps({'status': 'no', 'error': e.__repr__()})
    else:
        return json.dumps({"status": 'ok', "url": filename})


@csrf.exempt
@bp.route('/test', methods=['GET', 'POST'])
def test():
    args = dict(request.form)
    key = "123456"
    sig = request.form['sig']  # 签名
    tradeNo = request.form['tradeNo']  # 交易号
    desc = request.form['desc']  # 交易名称（付款说明）
    time = request.form['time']  # 付款时间
    username = request.form['username']  # 客户名称
    userid = request.form['userid']  # 客户id
    amount = request.form['amount']  # 交易额
    status = request.form['status']  # 交易状态
    print "status,", status
    tmp_list = [tradeNo, desc, time, username, userid, amount, status, key]
    tmp_str = '|'.join(tmp_list)
    md5_str = (hashlib.md5(tmp_str.encode('utf-8')).hexdigest()).upper()
    # md5 校验
    if sig == md5_str:
        print "ok"
        query_log = Paylog.query.filter(Paylog.alipay_no == tradeNo, status == "待确认").first()
        if query_log:
            if status == "交易成功":
                query_log.status = "已支付"
                query_log.action = desc
                db.session.add(query_log)
                db.session.commit()
    print sig
    print md5_str
    import pprint
    pprint.pprint(args)
    return json.dumps({"status": 'ok'})
