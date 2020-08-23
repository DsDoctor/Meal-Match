from DAO.DataBase.database import db


class IngType(db.Model):
    __tablename__ = 'ing_type'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String)
