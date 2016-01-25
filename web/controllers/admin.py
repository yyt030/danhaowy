# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import os
from flask import render_template, Blueprint, redirect, url_for, g, session, request, \
    make_response, current_app, send_from_directory
from sqlalchemy import func
from web.forms.account import AdminloginForm
from web.forms.notice import NoticeForm
from web.forms.site import SiteInfo, PacketSettingForm, QQInfo
from web.models.site import Site, qqKefu
from web.utils.account import signin_user, signout_user
from ..models import db, User, Notice, MailBox, ApplySellerRecord, Order, OrderList, NullPacket, Paylog, Fundslog, Txlog
from ..forms import SigninForm, RegisterForm
from ..utils.permissions import require_user, require_visitor, require_admin
from datetime import datetime, timedelta

bp = Blueprint('admin', __name__)


@bp.route("/", methods=('GET', 'POST'))
@bp.route("/login", methods=('GET', 'POST'))
def login():
    form = AdminloginForm()
    status = ""
    if g.user:
        return redirect("admin/home")
    if request.method == 'POST':
        if form.is_submitted():

            user = User.query.filter(User.name == form.admin_name.data).first()
            if user:
                if user.check_password(form.password.data):
                    signin_user(user)
                    return redirect("admin/home")
                else:
                    print "error username or password"
            else:
                status = "登录失败"
        else:
            status = "登录失败"
            print "error"
    return render_template("admin/login.html", form=form, status=status)


@bp.route("/site_info", methods=('GET', 'POST'))
@require_admin
def site_info():
    form = SiteInfo()
    info = Site.query.first()
    if request.method == 'POST':
        print "logo,", form.logo.data
        if not info:
            info = Site(url=form.url.data, name=form.name.data, sitelogo=form.logo.data,
                        alipay=form.alipay.data)
            db.session.add(info)
        else:
            info.url = form.url.data
            info.name = form.name.data
            info.alipay = form.alipay.data
            info.sitelogo = form.logo.data
        db.session.commit()
    else:
        if info:
            form.url.data = info.url
            form.name.data = info.name
            form.alipay.data = info.alipay
            form.logo.data = info.sitelogo
    return render_template("admin/site_info.html", form=form, admin_nav=1, info=info)


@bp.route("/qq_kefu", methods=('GET', 'POST'))
@require_admin
def qq_kefu():
    form = QQInfo()
    info = qqKefu.query.first()
    if request.method == 'POST':
        if not info:
            info = qqKefu(qq1=form.qq1.data, qq2=form.qq2.data, qq3=form.qq3.data, qq4=form.qq4.data)
            db.session.add(info)
        else:
            info.qq1 = form.qq1.data
            info.qq2 = form.qq2.data
            info.qq3 = form.qq3.data
            info.qq4 = form.qq4.data
        db.session.commit()
    else:
        if info:
            form.qq1.data = info.qq1
            form.qq2.data = info.qq2
            form.qq3.data = info.qq3
            form.qq4.data = info.qq4
    return render_template("admin/qq_info.html", form=form, admin_nav=1, info=info)


@bp.route("/home", methods=('GET', 'POST'))
@require_admin
def home():
    user_count = User.query.filter(User.name != 'admin').count()
    # orders = db.session.query(func.sum(PayLog.money)).filter(PayLog.alipay_no != "")
    # total_income = orders[0][0]
    return render_template("admin/home.html")


@bp.route("/notice/add", methods=('GET', 'POST'))
@require_admin
def notice_setting():
    form = NoticeForm()
    id = int(request.args.get("id", 0))
    notice_type = request.args.get("type", "news")
    if notice_type == 'news':
        admin_nav = 2
    else:
        admin_nav = 3
    info = Notice.query.get(id)
    if request.method == 'POST':
        if not info:
            info = Notice(title=form.title.data, type=notice_type, desc=form.desc.data)
        else:
            info.title = form.title.data
            info.desc = form.desc.data
        db.session.add(info)
        db.session.commit()
        return redirect(url_for('admin.notice_list'))
    else:
        if info:
            form.title.data = info.title
            form.desc.data = info.desc
        else:
            info = {}
    return render_template("admin/notice_setting.html", admin_nav=admin_nav, notice_type=notice_type, form=form,
                           info=info)


@bp.route("/notices", methods=('GET', 'POST'))
@require_admin
def notice_list():
    notice_type = request.args.get("type", "news")
    if notice_type == 'news':
        admin_nav = 2
    else:
        admin_nav = 3
    notices = Notice.query.filter(Notice.type == notice_type)
    return render_template("admin/notice_list.html", admin_nav=admin_nav, notice_type=notice_type, notices=notices)


@bp.route('/notice/delete', methods=('GET', 'POST'))
@require_admin
def notice_delete():
    datas = request.form

    print dict(datas)
    for k in datas:
        id = int(datas[k])
        info = Notice.query.get(id)
        db.session.delete(info)
        db.session.commit()
    notices = Notice.query.all()
    return render_template('admin/notice_list.html', notice_type="news", notices=notices)


@bp.route("/userlist", methods=('GET', 'POST'))
@require_admin
def userlist():
    users = User.query.all()
    # users = User.query.all()
    return render_template("admin/users.html", admin_nav=4, users=users)


@bp.route('/userlist/delete', methods=('GET', 'POST'))
@require_admin
def user_delete():
    datas = request.form
    print dict(datas)
    for k in datas:
        id = int(datas[k])
        info = User.query.get(id)
        db.session.delete(info)
        db.session.commit()
    users = User.query.all()
    return render_template('admin/users.html', users=users)


@bp.route("/seller_list", methods=('GET', 'POST'))
@require_admin
def seller_list():
    """卖家列表"""
    handle = request.args.get("handle", False)
    type = request.args.get("type", "not_authed")
    action = request.args.get("action")
    msg_id = request.args.get('id', 0, type=int)
    users = ApplySellerRecord.query
    if type == 'not_authed':
        title = "待审核"
        users = users.filter(ApplySellerRecord.processed == False)
    else:
        title = "已审核"
        users = users.filter(ApplySellerRecord.processed == True)
    if action == 'yes':
        # 同意申请为卖家申请
        record = ApplySellerRecord.query.get_or_404(msg_id)
        record.processed = True
        record.passed = True
        seller = User.query.get_or_404(record.user_id)
        seller.is_seller = True

        db.session.add(record)
        db.session.add(seller)
        db.session.commit()
    if action == 'no':
        # 不同意申请为卖家申请
        record = ApplySellerRecord.query.get_or_404(msg_id)
        record.processed = True
        db.session.add(record)
        db.session.commit()
    return render_template("admin/sallers.html", admin_nav=5, users=users, title=title)


@bp.route('/number_list', methods=('GET', 'POST'))
@require_user
def number_list():
    """已发布的单号"""
    user = g.user

    type = request.args.get('type', '')
    query = Order.query
    if request.method == 'POST':
        if type == 'query':
            pass
        elif type == 'delete':
            datas = request.form
            print dict(datas)
            for k in datas:
                id = int(datas[k])

                info = Order.query.get(id)
                order_list = info.order_list
                for l in order_list:
                    db.session.delete(l)
                db.session.delete(info)
                db.session.commit()
            return json.dumps({"status": "ok"})
    if type in ["not_paid", "paid"]:
        if type == 'paid':
            title = "已售出"
            query = query.filter(Order.is_sell == 1, Order.seller_id != 1)
        else:
            title = "未售出"
            query = query.filter(Order.is_sell == 0, Order.seller_id != 1)
    startdate = request.args.get('startdate', '')
    enddate = request.args.get('enddate', '')

    page = request.args.get('page', 1, type=int)

    if startdate and enddate:
        query = query.filter(datetime.strptime(startdate, '%Y-%m-%d') <= Order.send_timestamp,
                             Order.send_timestamp <= datetime.strptime(enddate, '%Y-%m-%d') + timedelta(days=1))

    page_all = query.count() / current_app.config['FLASKY_PER_PAGE'] + 1
    pagination = query.order_by(Order.send_timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_PER_PAGE'], error_out=False)
    orders = pagination.items
    if type in ["not_paid", "paid"]:
        return render_template('admin/sellerout_number_list.html', title=title, admin_nav=6, type=type, orders=orders,
                               page=page,
                               page_all=page_all)

    return render_template('admin/number_list.html', orders=orders, admin_nav=6, page=page, page_all=page_all)


@bp.route('/look_number_list', methods=('GET', 'POST'))
@require_user
def look_number_list():
    """单号领取记录"""
    query = OrderList.query
    page = request.args.get('page', 1, type=int)
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    if starttime:
        query = query.filter(datetime.strptime(starttime, '%Y-%m-%d') <= OrderList.create_time)
    if endtime:
        query = query.filter(datetime.strptime(endtime, '%Y-%m-%d') + timedelta(days=1) >= OrderList.create_time)

    page_all = query.count() / current_app.config['FLASKY_PER_PAGE'] + 1
    pagination = query.order_by(OrderList.create_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_PER_PAGE'],
        error_out=False)
    orderlists = pagination.items

    return render_template('admin/look_number_list.html', orderlists=orderlists,
                           page_all=page_all, page=page)


@bp.route('/sellerout', methods=['GET', 'POST'])
@require_user
def sellerout():
    """已售出的单号"""
    user = g.user
    if not user.is_seller:
        return redirect(url_for('.upseller'))

    startdate = request.args.get('startdate', '')
    enddate = request.args.get('enddate', '')

    page = request.args.get('page', 1, type=int)

    query = Order.query.filter(Order.seller_id == user.id, Order.is_sell == 1)
    if startdate and enddate:
        query = query.filter(datetime.strptime(startdate, '%Y-%m-%d') <= Order.buy_time,
                             Order.buy_time <= datetime.strptime(enddate, '%Y-%m-%d') + timedelta(days=1))

    page_all = query.count() / current_app.config['FLASKY_PER_PAGE'] + 1
    pagination = query.order_by(Order.buy_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_PER_PAGE'],
        error_out=False)
    orders = pagination.items

    return render_template('admin/sellerout.html', orders=enumerate(orders, start=1), page=page, page_all=page_all)


@bp.route('/null_packet', methods=['GET', 'POST'])
@require_user
def null_packet():
    """空包管理
    等待发货，
    已经发货
    """
    status = request.args.get("status", type=int)
    if not status:
        status = 0
    query = NullPacket.query.filter(NullPacket.status == status)
    page = request.form.get('page', 1, type=int)
    page_all = query.count() / current_app.config['FLASKY_PER_PAGE'] + 1
    pagination = query.order_by(NullPacket.create_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_PER_PAGE'],
        error_out=False)
    nullpackets = pagination.items
    return render_template('admin/null_packet_list.html', page=page, admin_nav=7, pages=page_all, status=status,
                           nullpackets=nullpackets)


@bp.route('/send_packet', methods=['GET', 'POST'])
@require_user
def send_packet():
    """空包管理"""
    packet_id = request.args.get("id", type=int)
    nullpacket = NullPacket.query.get(packet_id)
    form = PacketSettingForm()
    if request.method == 'POST':
        # print packet_id
        nullpacket.tracking_no = form.tracking_no.data
        nullpacket.status = 1
        nullpacket.send_time = datetime.now()
        db.session.add(nullpacket)
        db.session.commit()
        return redirect(url_for('admin.null_packet'))
    else:
        form = PacketSettingForm()
        form.packet_id.data = nullpacket.id
        form.tracking_no.data = nullpacket.tracking_no
    return render_template('admin/null_packet_setting.html', admin_nav=7, form=form, nullpacket=nullpacket)


@bp.route('/delete_packet', methods=['GET', 'POST'])
@require_user
def delete_packet():
    """删除空包"""
    datas = request.form
    print dict(datas)
    for k in datas:
        id = int(datas[k])
        info = NullPacket.query.get(id)
        db.session.delete(info)
        db.session.commit()
    return redirect(url_for('admin.null_packet'))


@bp.route('/pay_log', methods=['GET', 'POST'])
@require_user
def pay_log():
    """充值记录"""
    page = request.args.get('page', 1, type=int)
    type = request.args.get("type", "waiting")
    query = Paylog.query
    if type == 'waiting':
        query = query.filter(Paylog.status == '待确认')
    else:
        query = query.filter(Paylog.status == '已支付')
    page_all = query.count() / current_app.config['FLASKY_PER_PAGE'] + 1
    pagination = query.order_by(Paylog.create_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_PER_PAGE'],
        error_out=False)
    paylogs = pagination.items

    return render_template('admin/pay_logs.html', admin_nav=8, type=type, paylogs=paylogs, page=page, page_all=page_all)


@bp.route('/confirm_pay_log', methods=['GET', 'POST'])
@require_user
def confirm_pay_log():
    """确认支付订单"""
    id = request.args.get("id", type=int)
    pay_log = Paylog.query.get(id)
    pay_log.status = "已支付"
    pay_log.money_status = 1
    user = pay_log.user
    admin_user = User.query.filter(User.name == 'admin').first()
    msg = MailBox(sender_id=pay_log.user_id, recver_id=admin_user.id, msg_type='充值')
    msg.title = '充值结果'
    msg.body = '充值成功,%s金币已到账' % pay_log.money
    user.wuyoubi += pay_log.money
    db.session.add(pay_log)
    db.session.add(user)
    db.session.add(msg)
    db.session.commit()
    return redirect(url_for('admin.pay_log'))


@bp.route('/pay_log/delete', methods=['GET', 'POST'])
@require_user
def delete_pay_log():
    """删除充值订单"""
    datas = request.form
    print dict(datas)
    for k in datas:
        id = int(datas[k])
        info = Paylog.query.get(id)
        db.session.delete(info)
        db.session.commit()
    return redirect(url_for('admin.pay_log'))


@bp.route('/get_crash_log', methods=['GET', 'POST'])
def get_crash_log():
    """提现订单"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get("status", "0")
    query = Txlog.query
    page_all = query.count() / current_app.config['FLASKY_PER_PAGE'] + 1
    pagination = query.order_by(Txlog.create_time.desc()).paginate(
        page, per_page=current_app.config['FLASKY_PER_PAGE'],
        error_out=False)
    paylogs = pagination.items

    return render_template('admin/get_crash_logs.html', admin_nav=9, paylogs=paylogs, status=status, page=page,
                           page_all=page_all)


@bp.route('/crash_log/delete', methods=['GET', 'POST'])
@require_user
def delete_crash_log():
    """删除提现订单"""
    datas = request.form
    # print dict(datas)
    for k in datas:
        id = int(datas[k])
        info = Txlog.query.get(id)
        db.session.delete(info)
        db.session.commit()
    return redirect(url_for('admin.crash_log'))


@bp.route('/confirm_crash_log', methods=['GET', 'POST'])
@require_user
def handle_crash_log():
    """处理提现订单"""
    id = request.args.get("id", type=int)
    status = request.args.get("status","1")
    pay_log = Txlog.query.get(id)
    pay_log.status = status
    user = pay_log.user
    admin_user = User.query.filter(User.name == 'admin').first()
    msg = MailBox(sender_id=pay_log.user_id, recver_id=admin_user.id, msg_type='提现申请')
    msg.title = '提现申请处理结果'
    if status == "2":
        # 提现失败,佣金回滚到用户金额
        user.money += pay_log.money
        msg.body = '提现申请失败,有任何疑问请联系客服'
    elif status == '1':
        msg.body = '提现申请已处理,%s元已充值到您绑定的支付宝账号' % pay_log.money
    db.session.add(pay_log)
    db.session.add(user)
    db.session.add(msg)
    db.session.commit()
    return redirect(url_for('admin.get_crash_log'))
