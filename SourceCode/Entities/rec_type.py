from DAO.DataBase.database import db


class RecType(db.Model):
    __tablename__ = 'rec_type'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String)
