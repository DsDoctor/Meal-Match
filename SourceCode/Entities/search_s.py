from DAO.DataBase.database import db


class SearchS(db.Model):
    __tablename__ = 'search'

    id = db.Column('id', db.Integer, primary_key=True)
    string = db.Column('string', db.String)
    frequency = db.Column('frequency', db.Integer, default=1)
    has_recipe = db.Column('has_recipe', db.Boolean, default=False)
