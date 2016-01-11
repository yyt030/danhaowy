# !/usr/bin/env python
# coding: utf-8
from datetime import datetime, timedelta

from flask import render_template, Blueprint, redirect, url_for, g, request, \
    current_app, make_response
from web.utils.permissions import require_user
from ..forms import SigninForm, RegisterForm
from ..models import db, User, Order, OrderList, MailBox

bp = Blueprint('login_user', __name__)


@bp.route('/', methods=['GET'])
@bp.route('/user', methods=['GET'])
@require_user
def index():
    form = SigninForm()
    user = g.user
    return render_template('login_user/index.html', form=form, user=user)


@bp.route('/ornumber', methods=['GET'])
@require_user
def ornumber():
    """单号领取"""
    form = SigninForm()
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

    return render_template('login_user/ornumber.html', orders=enumerate(orders), page=page, page_all=page_all)


@bp.route('/Qiso', methods=['GET', 'POST'])
@require_user
def qiso():
    """单号领取->提交查询"""
    user = g.user
    # 录单时间
    sja = request.args.get('sja', '')
    # 发货地址
    sa = request.args.get('sa', '')
    # 收货地址
    sb = request.args.get('sb', '')
    # 快递类型
    kd = request.args.get('kd', '')
    # 是否扫描
    sm = request.args.get('sm', '')
    query = Order.query
    if sja:
        query = query.filter(Order.create_time >= datetime.strptime(sja, '%Y-%m-%d'))
    if sa:
        send_addr_province, send_addr_city, send_addr_county = sa.split(' ')
        if send_addr_province:
            query = query.filter(Order.send_addr_province == send_addr_province)

        if send_addr_city:
            query = query.filter(Order.send_addr_city == send_addr_city)

        if send_addr_county:
            query = query.filter(Order.send_addr_county == send_addr_county)
    if sb:
        recv_addr_province, recv_addr_city, recv_addr_county = sb.split(' ')
        if recv_addr_province:
            query = query.filter(Order.recv_addr_province == recv_addr_province)

        if recv_addr_city:
            query = query.filter(Order.recv_addr_city == recv_addr_city)

        if recv_addr_county:
            query = query.filter(Order.recv_addr_county == recv_addr_county)
    if kd and kd != '0':
        query = query.filter(Order.tracking_company == kd)
    if sm and kd != '0':
        query = query.filter(Order.is_scan == sm)

    page = request.args.get('page', 1, type=int)
    all_num = query.count()
    page_all = all_num / current_app.config['FLASKY_PER_PAGE'] + 1
    pagination = query.order_by(Order.send_timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_PER_PAGE'],
            error_out=False)
    orders = pagination.items

    sitemap_xml = render_template('login_user/qiso.xhtml', orders=enumerate(orders),
                                  page_every=current_app.config['FLASKY_PER_PAGE'] or 40,
                                  page=page, page_all=page_all, user=user, all_num=all_num
                                  )
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "text/xml"
    return response


@bp.route('/Refund', methods=['GET', 'POST'])
@require_user
def refund():
    """快递单号检测"""
    qi = request.args.get('qi')
    ord = request.args.get('ord')
    ordlx1 = request.args.get('ordlx1')
    print '-' * 10, qi, ord, ordlx1
    return '0'


@bp.route('/Qikd', methods=['POST'])
@require_user
def qikd():
    """单号领取 -> 扫描时间"""
    com = request.form.get('com')
    id = request.form.get('id')
    qid = request.form.get('qid')
    q = request.form.get('q')

    return '2016/1/9 00:25,【广东佛山公司】的收件员【】已收件'


@bp.route('/GetNumber', methods=['GET', 'POST'])
@bp.route('/BatchGetNumber', methods=['GET', 'POST'])
@require_user
def getnumber():
    form = SigninForm()
    user = g.user
    uids = request.args.getlist('uid')
    type = request.args.get('type', '')

    left_num = user.max_order_num - OrderList.query.filter(OrderList.user_id == user.id,
                                                           OrderList.create_time >= datetime.today().date()).count()

    if left_num < len(uids) or left_num < 1:
        tip = "用户%s剩余领取次数%d不足！" % (user.name, left_num)
        return render_template('error.html', error=tip, url="number")
    if uids:
        if len(uids) > 1:
            for order_id in uids:
                orderlist = OrderList()
                orderlist.order_id = order_id
                orderlist.user_id = user.id
                db.session.add(orderlist)
            db.session.commit()

            orders = Order.query.filter(Order.id.in_(uids))
            return render_template('login_user/getbatchnumber.html', form=form, user=user, orders=orders)
        else:

            order = Order.query.get_or_404(request.args.get('uid', ''))
            return render_template('login_user/getnumber.html', form=form, user=user, order=order, left_num=left_num)
    if type == 'Success':
        orderlist = OrderList()
        uid = request.form.get('uid', 0, type=int)
        orderlist.order_id = uid
        orderlist.user_id = user.id
        db.session.add(orderlist)
        db.session.commit()
        tip = "用户%s 领取单号%d成功！" % (user.name, uid)
        return render_template('error.html', error=tip, url="ornumber")


@bp.route('/number')
@require_user
def number():
    """领取次数增加"""

    user = g.user
    form = SigninForm()

    return render_template('login_user/number.html', form=form, user=user)


@bp.route('/file', methods=['GET', 'POST'])
@require_user
def file():
    """领取次数增加"""
    user = g.user
    action = request.args.get('action', '')
    if request.method == 'POST':
        if action == 'cishu':
            count = request.form.get('Count', 0, type=int)
            pay = count * 5
        if action == 'cishution':
            count = request.form.get('hOutG', 0, type=int)
            pay = request.form.get('hInMoney', 0, type=float)

        if user.wuyoubi < pay:
            tip = "用户%s 无忧币不足！" % user.name
            return render_template('error.html', error=tip, url="number")

        user.wuyoubi -= pay
        user.max_order_num += count

        db.session.add(user)
        db.session.commit()

    tip = "用户%s 增加次数成功！" % user.name
    return render_template('error.html', error=tip, url="number")


@bp.route('/LookNumber', methods=['GET', 'POST'])
@require_user
def looknumber():
    """查看已领取单号"""
    user = g.user
    page = request.args.get('page', 1, type=int)
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')

    query = OrderList.query.filter(OrderList.user_id == user.id)
    if starttime:
        query = query.filter(datetime.strptime(starttime, '%Y-%m-%d') <= OrderList.create_time)
    if endtime:
        query = query.filter(datetime.strptime(endtime, '%Y-%m-%d') + timedelta(days=1) >= OrderList.create_time)

    page_all = query.count() / current_app.config['FLASKY_PER_PAGE'] + 1
    pagination = query.order_by(OrderList.create_time.desc()).paginate(
            page, per_page=current_app.config['FLASKY_PER_PAGE'],
            error_out=False)
    orderlists = pagination.items

    return render_template('login_user/looknumber.html', orderlists=enumerate(orderlists),
                           page_all=page_all, page=page)


@bp.route('/wybjihuo', methods=['GET', 'POST'])
@require_user
def wybjihuo():
    user = g.user
    form = RegisterForm()
    action = request.args.get('action', '')
    if request.method == 'POST' and action == 'jihuo':
        user.wuyoubi -= 50
        user.is_active = True
        db.session.add(user)
        db.session.commit()
        tip = "用户%s已激活！" % user.name
        return render_template('error.html', error=tip, url="ornumber")

    return render_template('login_user/wybjihuo.html', form=form, user=user)


@bp.route('/shopnumber', methods=['GET'])
@require_user
def shopnumber():
    """单号购买"""

    form = SigninForm()
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

    return render_template('login_user/ornumber.html', orders=enumerate(orders), page=page, page_all=page_all)


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
    user = g.user
    batch_flag = request.args.get('qi')
    if request.method == 'POST':
        seller_id = user.id
        send_timestamp = request.form.get('send_date')
        send_addr_province = request.form.get('ashenglist')
        send_addr_city = request.form.get('ashilist')
        send_addr_county = request.form.get('aqulist')
        tracking_company = request.form.get('com')
        is_scan = request.form.get('scan', 0, type=int)

        tracking_no = request.form.get('num')
        recv_addr_province = request.form.get('dshenglist')
        recv_addr_city = request.form.get('dshilist')
        recv_addr_county = request.form.get('dqulist')

        if batch_flag:
            send_addr_province = request.form.get('cshenglist')
            send_addr_city = request.form.get('cshilist')
            send_addr_county = request.form.get('cqulist')

            order_list = []
            success_count = 0
            failed_count = 0
            contents = request.form.get('r')
            content_list = contents.split('%0A')
            import re
            for record in content_list:
                order = Order(seller_id=seller_id, send_timestamp=send_timestamp, send_addr_province=send_addr_province,
                              send_addr_city=send_addr_city, send_addr_county=send_addr_county,
                              tracking_company=tracking_company, is_scan=is_scan)

                record = re.split(r'%7C|%20', record)
                if len(record) < 4:
                    failed_count += 1
                    continue
                order.tracking_no = record[0]

                if Order.query.filter(Order.tracking_no == order.tracking_no).first():
                    failed_count += 1
                    continue

                order.recv_addr_province = record[1]
                order.recv_addr_city = record[2]
                order.recv_addr_county = record[3]
                order_list.append(order)
                success_count += 1

            db.session.add_all(order_list)
            db.session.commit()
            return '成功%d条，错误%d条' % (success_count, failed_count)
        else:
            order = Order(seller_id=seller_id, send_timestamp=send_timestamp, send_addr_province=send_addr_province,
                          send_addr_city=send_addr_city, send_addr_county=send_addr_county,
                          tracking_company=tracking_company, is_scan=is_scan, tracking_no=tracking_no,
                          recv_addr_province=recv_addr_province,
                          recv_addr_city=recv_addr_city, recv_addr_county=recv_addr_county)

            db.session.add(order)
            db.session.commit()
            tip = "订单%s发布成功！" % order.tracking_no
            return render_template('error.html', error=tip, url="")

    return render_template('login_user/seller.html', form=form)


@bp.route('/ornumber_1', methods=['GET'])
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


@bp.route('/upseller', methods=['GET', 'POST'])
@require_user
def upseller():
    """申请成为卖家"""
    form = SigninForm()
    user = g.user

    if request.method == 'POST':
        # msg = MailBox(sender_id=user.id, recver_id=1)
        # msg.title = 'QQ:%s mail:%s 申请卖家' % (request.form.get('QQ', ''), request.form.get('Email', ''))
        # msg.body = '每日最低提供单号数[%s], 承诺发布的单号均为真实单号[%s], 承诺发布的单号均为唯一单号[%s]' % (
        # request.form.get('ag1', ''), request.form.get('ag2', ''), request.form.get('typ', ''))
        # db.session.add(msg)
        # db.session.commit()
        tip = "申请已发送，请联系管理员处理！"
        return render_template('error.html', error=tip, url="")
    return render_template('login_user/upseller.html', form=form, user=user)


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
        if not user.check_password(password):
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
    """已发布的单号"""
    user = g.user
    type = request.args.get('type', '')
    if type == 'delall':
        id_lists = request.args.getlist('uid')
        for id in id_lists:
            order = Order.query.get_or_404(id)
            db.session.delete(order)
        db.session.commit()
        tip = "删除成功！"
        return render_template('error.html', error=tip, url="sellerlist")

    startdate = request.args.get('startdate', '')
    enddate = request.args.get('enddate', '')

    page = request.args.get('page', 1, type=int)

    query = Order.query.filter(Order.seller_id == user.id)
    if startdate and enddate:
        query = query.filter(datetime.strptime(startdate, '%Y-%m-%d') <= Order.send_timestamp,
                             Order.send_timestamp <= datetime.strptime(enddate, '%Y-%m-%d') + timedelta(days=1))

    page_all = query.count() / current_app.config['FLASKY_PER_PAGE'] + 1
    pagination = query.order_by(Order.send_timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_PER_PAGE'],
            error_out=False)
    orders = pagination.items

    return render_template('login_user/sellerlist.html', orders=enumerate(orders), page=page, page_all=page_all)


@bp.route('/sellerout', methods=['GET', 'POST'])
@require_user
def sellerout():
    """已售出的单号"""
    user = g.user
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

    return render_template('login_user/sellerout.html', orders=enumerate(orders), page=page, page_all=page_all)


@bp.route('/shoplog', methods=['GET', 'POST'])
@require_user
def shoplog():
    """佣金记录"""
    user = g.user
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
    shoplogs = pagination.items

    return render_template('login_user/shoplog.html', shoplogs=enumerate(shoplogs), page=page, page_all=page_all)


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
    if request.method == 'POST':
        if user.jifen >= jifen:
            user.money += jifen * Decimal(.00005)
            user.jifen -= jifen
            db.session.add(user)
            db.session.commit()
            tip = "兑换积分成功！"
        else:
            tip = "兑换积分失败, 无足够积分!"
        return render_template('error.html', error=tip, url="")
    return render_template('login_user/sellerjf.html', form=form, user=user)


@bp.route('/msg', methods=['GET', 'POST'])
@require_user
def msg():
    """站内信箱"""
    form = RegisterForm()

    user = g.user
    msg_id = request.args.get('id', 0, type=int)
    action = request.args.get('nn', '')

    page = request.args.get('page', 1, type=int)

    query = MailBox.query.filter(MailBox.recver_id == user.id)

    if msg_id:
        msg = MailBox.query.get_or_404(msg_id)
        msg.is_read = True
        db.session.add(msg)
        db.session.commit()
        return render_template('login_user/msg_show.html', msg=msg)
    if action:
        if action == 'del':
            msgs = query.all()
            for msg in msgs:
                db.session.delete(msg)
        if action == 'yd':
            msgs = query.all()
            for msg in msgs:
                msg.is_read = True
            db.session.add_all(msgs)
        db.session.commit()
        return redirect(url_for('.msg'))

    count_all = query.count()
    page_all = count_all / current_app.config['FLASKY_PER_PAGE'] + 1
    pagination = query.order_by(MailBox.create_at.desc()).paginate(
            page, per_page=current_app.config['FLASKY_PER_PAGE'],
            error_out=False)
    msgs = pagination.items

    return render_template('login_user/msg.html', form=form, msgs=msgs, page=page, page_all=page_all,
                           count_all=count_all)
