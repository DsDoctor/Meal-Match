from DAO.DataBase.database import db


class RelRecType(db.Model):
    __tablename__ = 'relation_rec_type'

    id = db.Column('id', db.Integer, primary_key=True)
    r_id = db.Column('r_id', db.Integer)
    t_id = db.Column('t_id', db.Integer)
