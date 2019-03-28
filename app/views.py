from flask import Flask, render_template, flash, request, redirect, url_for
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from flask_bootstrap import Bootstrap
from test import app
from flask_sqlalchemy import SQLAlchemy

app.config['SECRET_KEY'] = 'hello RobbiJiu'
login_manager = LoginManager()
login_manager.init_app(app)
bootstrap = Bootstrap(app)


# 构建登陆逻辑
class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    from .DBdata import get_user_list
    user_list = get_user_list()
    if username not in user_list:
        return None
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    from hashlib import md5
    from .DBdata import get_user_list, get_user_passwd
    user_list = get_user_list()
    login_username = request.form.get('loginname')
    if login_username not in user_list:
        return None
    user = User()
    user.id = login_username
    # is_authenticated : 当用户通过验证时，也即提供有效证明时返回 True 。（只有通过验证的用户会满足 login_required 的条件。）
    user.is_authenticated = md5(request.form['password'].encode()).hexdigest() == get_user_passwd(login_username)
    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '未登录错误访问，跳转到登陆界面')
    flash('未登录，请登录后操作')
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已安全退出')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    from .forms import LoginForm
    from .DBdata import get_user_list, get_user_passwd
    from hashlib import md5
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user_list = get_user_list()
        if username not in user_list:
            flash('用户不存在')
        else:
            password = md5(form.password.data.encode()).hexdigest()
            db_password = get_user_passwd(username)
            if password == db_password:
                auto_login = form.remember_me.data
                user = User()
                user.id = username
                login_user(user, auto_login)
                return redirect(url_for('index'))
            flash('密码错误')
    return render_template('login.html', form=form)


# 根目录
@app.route('/')
def root():
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'root节点，跳转到login')
    return redirect(url_for('login'))

@app.route('/index')
def index():
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'root节点，跳转到login')
    return render_template('index.html')


@app.route('/Marketing', methods=['GET', 'POST'])
@login_required
def Marketing():
    from .forms import FindData
    from molds import Month_2018
    form = FindData()
    filters = set()
    if form.validate_on_submit():
        if form.region.data:
            filters.add(Month_2018.region == form.region.data)
        if form.small_area.data:
            filters.add(Month_2018.small_area == form.small_area.data)
        if form.hospname.data:
            filters.add(Month_2018.hospname == form.hospname.data)
        if form.marketing_package.data:
            filters.add(Month_2018.marketing_package == form.marketing_package.data)
        if form.start_month.data:
            filters.add(Month_2018.month >= form.start_month.data)
        if form.stop_month.data:
            filters.add(Month_2018.month <= form.stop_month.data)
    page = request.args.get('page', 1, type=int)
    pagination = Month_2018.query.filter(*filters).paginate(page, per_page=12, error_out=False)
    list = pagination.items
    return render_template('Marketing.html', list=list, pagination=pagination, form=form)





@app.route('/ajaxPage', methods=['GET', 'POST'])
@login_required
def ajaxPage():
    from .forms import FindData
    from molds import Month_2018
    form = FindData()
    filters = set()
    page = request.args.get('page', 1, type=int)
    region = request.form.get('region')
    small_area = request.form.get('small_area')
    hospname = request.form.get('hospname')
    marketing_package = request.form.get('marketing_package')
    start_month = request.form.get('start_month')
    stop_month = request.form.get('stop_month')
    if region:
        filters.add(Month_2018.region == region)
    if small_area:
        filters.add(Month_2018.small_area == small_area)
    if hospname:
        filters.add(Month_2018.hospname == hospname)
    if marketing_package:
        filters.add(Month_2018.marketing_package == marketing_package)
    if start_month:
        filters.add(Month_2018.month >= start_month)
    if stop_month:
        filters.add(Month_2018.month <= stop_month)
    pagination = Month_2018.query.filter(*filters).paginate(page, per_page=12, error_out=False)
    list = pagination.items
    return render_template('Marketing.html', pagination=pagination, list=list, form=form)


@app.route('/viewshow', methods=['GET', 'POST'])
@login_required
def viewshow():
    from molds import Month_2018
    import pandas as pd
    from .deMethod import tool
    filters = set()
    region = request.form.get('region')
    small_area = request.form.get('small_area')
    hospname = request.form.get('hospname')
    marketing_package = request.form.get('marketing_package')
    start_month = request.form.get('start_month')
    stop_month = request.form.get('stop_month')
    if region:
        filters.add(Month_2018.region == region)
    if small_area:
        filters.add(Month_2018.small_area == small_area)
    if hospname:
        filters.add(Month_2018.hospname == hospname)
    if marketing_package:
        filters.add(Month_2018.marketing_package == marketing_package)
    if start_month:
        filters.add(Month_2018.month >= start_month)
    if stop_month:
        filters.add(Month_2018.month <= stop_month)
    data_one = []
    data_two = []
    data_month = []

    # ==================-----------------按所有查询大区数量------------=================

    if not region == '' and small_area == '':
        for data in Month_2018.query.filter(*filters).all():
            data_one.append(data.small_area)
            data_two.append(data.number)
            data_month.append(data.month)
        data_dict = {
            'small_area': data_one,
            'number': data_two,
            'month': data_month
        }
        showdataframe = pd.DataFrame(data_dict)
        htmlcont = tool.getShowData(showdataframe, 'small_area', 'number', start_month, stop_month)
        return htmlcont

        # ==================-----------------按大区查询小区数量------------=================
    if region == '' and small_area == ''and hospname=='':
        for data in Month_2018.query.filter(*filters).all():
            data_one.append(data.region)
            data_two.append(data.number)
            data_month.append(data.month)
        data_dict = {
            'region': data_one,
            'number': data_two,
            'month': data_month
        }
        showdataframe = pd.DataFrame(data_dict)
        htmlcont = tool.getShowData(showdataframe, 'region', 'number', start_month, stop_month)
        return htmlcont


    # ==================-----------------按小区查询客户数量------------=================
    if not region == '' and not small_area == '' and hospname=='':
        for data in Month_2018.query.filter(*filters).all():
            data_one.append(data.hospname)
            data_two.append(data.number)
            data_month.append(data.month)
        data_dict = {
            'hospname': data_one,
            'number': data_two,
            'month': data_month
        }
        showdataframe = pd.DataFrame(data_dict)
        htmlcont = tool.getShowData(showdataframe, 'hospname', 'number', start_month, stop_month)
        return htmlcont



    # ==================-----------------按客户查询营销套餐数量------------=================
    if not hospname=='' and  marketing_package=='':
        for data in Month_2018.query.filter(*filters).all():
            data_one.append(data.marketing_package)
            data_two.append(data.number)
            data_month.append(data.month)
        data_dict = {
            'marketing_package': data_one,
            'number': data_two,
            'month': data_month
        }
        showdataframe = pd.DataFrame(data_dict)
        htmlcont = tool.getShowData(showdataframe, 'marketing_package', 'number', start_month, stop_month)
        return htmlcont


    # ==================-----------------按客户查询营销套餐数量------------=================
    if not marketing_package=='':
        for data in Month_2018.query.filter(*filters).all():
            data_one.append(data.marketing_package)
            data_two.append(data.number)
            data_month.append(data.month)
        data_dict = {
            'marketing_package': data_one,
            'number': data_two,
            'month': data_month
        }
        showdataframe = pd.DataFrame(data_dict)
        htmlcont = tool.getShowData(showdataframe, 'marketing_package', 'number', start_month, stop_month)
        return htmlcont
    return 'OK'



