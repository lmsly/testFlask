from exts import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Uname = db.Column(db.String(20), nullable=False)
    Upassword= db.Column(db.String(100), nullable=False)

class Month_2018(db.Model):
    __tablename__ = "month_2018"
    index_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, nullable=True)
    region = db.Column(db.Text, nullable=True)
    small_area = db.Column(db.Text, nullable=True)
    hospname = db.Column(db.Text, nullable=True)
    marketing_package = db.Column(db.Text, nullable=True)
    department = db.Column(db.Text, nullable=True)
    doctor = db.Column(db.Text, nullable=True)
    number = db.Column(db.Integer, nullable=True)
    standard_price = db.Column(db.REAL, nullable=True)
    not_price = db.Column(db.REAL, nullable=True)
    ture_price = db.Column(db.REAL, nullable=True)
    actual_price = db.Column(db.REAL, nullable=True)
    month = db.Column(db.Integer, nullable=True)