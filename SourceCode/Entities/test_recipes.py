from DAO.DataBase.database import db


class TestRecipe(db.Model):
    __tablename__ = 'ScrapyData'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String)
    img_link = db.Column('img_link', db.String)
    text = db.Column('text', db.String)
    steps = db.Column('steps', db.String)
