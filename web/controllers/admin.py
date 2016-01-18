# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from flask import render_template, Blueprint, redirect, url_for, g, session, request, \
    make_response, current_app, send_from_directory
from sqlalchemy import func
from web.forms.account import AdminloginForm
from web.forms.notice import NoticeForm
from web.forms.site import SiteInfo
from web.models.site import Site
from web.utils.account import signin_user, signout_user
from ..models import db, User, Notice
from ..forms import SigninForm, RegisterForm
from ..utils.permissions import require_user, require_visitor, require_admin
from datetime import datetime

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
    users = User.query.filter(User.name != 'admin')
    # users = User.query.all()
    return render_template("admin/users.html", users=users)


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