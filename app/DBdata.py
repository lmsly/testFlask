from molds import User, Month_2018


# 用户登录相关函数
def get_user_list():
    listuser = []
    try:
        admin = User.query.all()
        for i in admin:
            listuser.append(i.Uname)
        return listuser
    except BaseException:
        print("密码错误")


def get_user_passwd(login_name):
    try:
        admin = User.query.filter_by(Uname="%s" % login_name).all()
        rename = admin[0].Upassword
        return rename
    except BaseException:
        print('密码调用异常')


def get_monthlist():
    filters = set()
    if Month_2018:
        filters.add(Month_2018.index_id=='合作共建部东区')
    if Month_2018:
        filters.add(Month_2018.index_id=='1')
    if Month_2018:
        filters.add(Month_2018.index_id=='1')
    admin = Month_2018.query.filter(*filters).all()
    for i in admin:
        print(i.hospname)
    return "tts"