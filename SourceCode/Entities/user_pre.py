from DAO.DataBase.database import db


class UserPre(db.Model):
    __tablename__ = 'user_pre'

    id = db.Column('id', db.Integer, primary_key=True)
    user = db.Column('user', db.Integer)
    pre = db.Column('pre', db.Integer)
