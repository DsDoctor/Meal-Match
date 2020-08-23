from DAO.DataBase.database import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column('id', db.Integer, primary_key=True)
    content = db.Column('content', db.String)
    user = db.Column('user', db.Integer)
    recipe = db.Column('recipe', db.Integer)
    update_time = db.Column('update_time', db.DateTime)
