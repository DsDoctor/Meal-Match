from DAO.DataBase.database import db


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String)
    img_link = db.Column('img_link', db.String)
    steps = db.Column('steps', db.String)
    update_time = db.Column('update_time', db.DateTime)
    like = db.Column('like', db.Integer, default=0)
    author = db.Column('author', db.Integer)
    cook_time = db.Column('cook_time', db.Integer)
    describe = db.Column('describe', db.String)
    img_type = db.Column('img_type', db.String)
