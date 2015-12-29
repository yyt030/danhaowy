# coding: utf-8
from flask import render_template, Blueprint

bp = Blueprint('', __name__)


@bp.route('/addshop',methods=['GET', 'POST'])
def index():
    return render_template('shop/setting.html')


