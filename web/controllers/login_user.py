# !/usr/bin/env python
# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
from flask import render_template, Blueprint, redirect, url_for, g, session, request, \
    make_response, current_app, send_from_directory
from web.utils.account import signin_user, signout_user
from ..models import db, User, Order, ShopLog
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


@bp.route('/seller', methods=['GET', 'POST'])
@require_user
def seller():
    """发布单号
    ImmutableMultiDict([('dshenglist', u'\u56db\u5ddd\u7701'),
     ('csrf_token', u'1451659269.98##820fb0a1ab9ba8accff0e8f00b309b654128e1c1'),
      ('ashilist', u'\u5317\u4eac\u5e02'), ('scan', u'1'),
      ('ashenglist', u'\u5317\u4eac'), ('aqulist', u'\u4e1c\u57ce\u533a'),
      ('dqulist', u'\u9526\u6c5f\u533a'), ('dshilist', u'\u6210\u90fd\u5e02'),
       ('num', u'123123123123213'),('send_date', u'2016-01-01 21:41:14'), ('com', u'yuantong')])
    """
    form = SigninForm()
    print request.form
    if request.method == 'POST':
        order = Order()
        order.tracking_no = request.form.get('num')
        order.send_timestamp = request.form.get('send_date')

        order.send_addr_province = request.form.get('ashenglist')
        order.send_addr_city = request.form.get('ashilist')
        order.send_addr_county = request.form.get('aqulist')

        order.recv_addr_province = request.form.get('dshenglist')
        order.recv_addr_city = request.form.get('dshilist')
        order.recv_addr_county = request.form.get('dqulist')
        order.tracking_company = request.form.get('com')
        order.is_scan = request.form.get('scan', 0, type=int)
        db.session.add(order)
        db.session.commit()
        tip = "订单%s发布成功！" % order.tracking_no
        return render_template('error.html', error=tip, url="")

    return render_template('login_user/seller.html', form=form)


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
    """申请成为卖家"""
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


@bp.route('/sellerlist')
@require_user
def sellerlist():
    startdate = request.args.get('startdate', '')
    enddate = request.args.get('enddate', '')

    page = request.args.get('page', 1, type=int)

    query = Order.query
    if startdate and enddate:
        query = query.filter(datetime.strptime(startdate, '%Y-%m-%d') <= Order.send_timestamp,
                             Order.send_timestamp <= datetime.strptime(enddate, '%Y-%m-%d') + timedelta(days=1))

    page_all = query.count() / current_app.config['FLASKY_PER_PAGE'] + 1
    pagination = query.order_by(Order.send_timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_PER_PAGE'],
            error_out=False)
    orders = pagination.items

    return render_template('login_user/sellerlist.html', orders=enumerate(orders), page=page, page_all=page_all)


@bp.route('/shoplog', methods=['GET', 'POST'])
@require_user
def shoplog():
    startdate = request.args.get('startdate', '')
    enddate = request.args.get('enddate', '')

    page = request.args.get('page', 1, type=int)

    query = ShopLog.query
    if startdate and enddate:
        query = query.filter(datetime.strptime(startdate, '%Y-%m-%d') <= ShopLog.create_at,
                             ShopLog.create_at <= datetime.strptime(enddate, '%Y-%m-%d') + timedelta(days=1))
    page_all = query.count() / current_app.config['FLASKY_PER_PAGE'] + 1
    pagination = query.order_by(ShopLog.create_at.desc()).paginate(
            page, per_page=current_app.config['FLASKY_PER_PAGE'],
            error_out=False)
    shoplogs = pagination.items

    return render_template('login_user/shoplog.html', shoplogs=enumerate(shoplogs), page=page, page_all=page_all)


@bp.route('/sellerout', methods=['GET', 'POST'])
@require_user
def sellerout():
    startdate = request.args.get('startdate', '')
    enddate = request.args.get('enddate', '')

    page = request.args.get('page', 1, type=int)

    query = Order.query.filter(Order.is_sell == 1)
    if startdate and enddate:
        query = query.filter(datetime.strptime(startdate, '%Y-%m-%d') <= Order.send_timestamp,
                             Order.send_timestamp <= datetime.strptime(enddate, '%Y-%m-%d') + timedelta(days=1))

    page_all = query.count() / current_app.config['FLASKY_PER_PAGE'] + 1
    pagination = query.order_by(Order.send_timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_PER_PAGE'],
            error_out=False)
    orders = pagination.items
    return render_template('login_user/sellerout.html', orders=enumerate(orders), page=page, page_all=page_all)


@bp.route('/sellerset', methods=['GET', 'POST'])
@require_user
def sellerset():
    '''设置默认发货'''
    form = RegisterForm()
    return render_template('login_user/sellerset.html', form=form)


@bp.route('/sellerjf', methods=['GET', 'POST'])
@require_user
def sellerjf():
    '''发布积分兑换'''
    form = RegisterForm()
    user = g.user
    user = User.query.filter(User.id == user.id).first()

    from decimal import Decimal
    jifen = request.form.get('jifen', 0.0, type=Decimal)

    print '>>>', user.money, user.jifen

    if request.method == 'POST':
        user.money += user.money * Decimal(0.00005)
        user.jifen -= jifen
        print jifen, user.money, user.jifen
        db.session.add(user)
        db.session.commit()
    return render_template('login_user/sellerjf.html', form=form, user=user)
