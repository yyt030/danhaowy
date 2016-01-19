#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import g, render_template
from functools import wraps
from flask import abort, redirect, url_for, flash


def require_visitor(func):
    """Check if no user login"""

    @wraps(func)
    def decorator(*args, **kwargs):
        if not g.user:
            return redirect(url_for('site.login'))
        return func(*args, **kwargs)

    return decorator


def require_user(func):
    """Check if user login"""

    @wraps(func)
    def decorator(*args, **kwargs):
        if not g.user:
            # flash('此操作需要登录账户')
            return redirect(url_for('site.login'))
        return func(*args, **kwargs)

    return decorator

def require_seller(func):
    """Check if user login"""

    @wraps(func)
    def decorator(*args, **kwargs):
        if not g.user.is_seller:
            # flash('此操作需要登录账户')
            return redirect(url_for('login_user.upseller'))
        return func(*args, **kwargs)

    return decorator


def require_active(func):
    """需要激活"""

    @wraps(func)
    def decorator(*args, **kwargs):
        if not g.user.is_active:

            tip = "%s您当前账号还未激活,请先激活账号" % g.user.name
            return render_template('error.html', error=tip, url="wybjihuo")
        return func(*args, **kwargs)

    return decorator

def require_mobile_user(func):
    """Check if mobile user login"""

    @wraps(func)
    def decorator(*args, **kwargs):
        if not g.user:
            return redirect(url_for('wechat.signin'))
        return func(*args, **kwargs)

    return decorator





ADMIN_EMAIL = "admin"
ADMIN_PSW = "admin"


def require_admin(func):
    """Check if user is admin"""

    @wraps(func)
    def decorator(*args, **kwargs):
        if not g.user:
            # flash('此操作需要登录账户')
            return redirect(url_for('admin.login'))
        if g.user.name != 'admin':
            abort(403)
        return func(*args, **kwargs)

    return decorator