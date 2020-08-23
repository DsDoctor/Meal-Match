from DAO.DataBase.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column('username', db.String)
    password = db.Column('password', db.String)
    email = db.Column('email', db.String)
    exp = db.Column('exp', db.Integer, default=0)
    visit_time = db.Column('visit_time', db.DateTime)
    max_exp = db.Column('max_exp', db.Integer, default=0)
