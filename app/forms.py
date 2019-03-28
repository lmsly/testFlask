from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Regexp, EqualTo
from molds import Month_2018

class LoginForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired(message="请输入账号！")])
    password = PasswordField('密码', validators=[DataRequired(message="请输入密码！")])
    # verify_code = StringField(label="验证码",validators=[DataRequired()])
    remember_me = BooleanField('下次自动登陆（请不要在公用电脑勾选此项）')
    submit = SubmitField('登陆')


class FindData(FlaskForm):
    regionlists=[('','')]
    small_arealists = [('', '')]
    # hospnamelists = [('', '')]
    # marketing_packagelists = [(None, '')]
    count = 1
    regionData = Month_2018.query.with_entities(Month_2018.region).distinct().all()
    for i in regionData:
        regionlists.append((i) + (i))
        count = count + 1
    region = SelectField(
        label='客户区域', render_kw={'class': 'form-control'},
        choices=regionlists
    )

    small_areaData = Month_2018.query.with_entities(Month_2018.small_area).distinct().all()
    for i in small_areaData:
        small_arealists.append((i) + (i))
        count = count + 1
    small_area = SelectField(
        label='客户小区', render_kw={'class': 'form-control'},
        choices=small_arealists
    )

    # hospnameData = Month_2018.query.with_entities(Month_2018.hospname).distinct().all()
    # for i in hospnameData:
    #     hospnamelists.append((i) + (i))
    #     count = count + 1
    # hospname = SelectField(
    #     label='客户名称', render_kw={'class': 'form-control'},
    #     choices=hospnamelists
    # )

    # marketing_packageData = Month_2018.query.with_entities(Month_2018.marketing_package).distinct().all()
    # for i in marketing_packageData:
    #     marketing_packagelists.append((i) + (i))
    #     count = count + 1
    # marketing_package = SelectField(
    #     label='营销套餐', render_kw={'class': 'form-control'},
    #     choices=marketing_packagelists
    # )
    # region = StringField('客户区域')
    # small_area = StringField('客户小区')
    hospname = StringField('客户名称')
    marketing_package = StringField('营销套餐')
    # start_month1 = StringField('开始月份')
    start_month = SelectField(
        label='起始月份', validators=[DataRequired('请选择标签')], render_kw={'class': 'form-control'},
        choices=[(1, '1月份'), (2, '2月份'), (3, '3月份'), (4, '4月份'), (5, '5月份'), (6, '6月份'), (7, '7月份'), (8, '8月份'), (9, '9月份'), (10, '10月份'), (11, '11月份'), (12, '12月份')],  coerce=int
    )
    stop_month = SelectField(
        label='结束月份', validators=[DataRequired('请选择标签')], render_kw={'class': 'form-control'},
        choices=[(1, '1月份'), (2, '2月份'), (3, '3月份'), (4, '4月份'), (5, '5月份'), (6, '6月份'), (7, '7月份'), (8, '8月份'), (9, '9月份'), (10, '10月份'), (11, '11月份'), (12, '12月份')],  coerce=int
    )
    submit = SubmitField('查询')

