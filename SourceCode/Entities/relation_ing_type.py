from DAO.DataBase.database import db


class RelIngType(db.Model):
    __tablename__ = 'relation_ing_type'

    id = db.Column('id', db.Integer, primary_key=True)
    ingredient = db.Column('ingredient', db.Integer)
    type = db.Column('type', db.Integer)
