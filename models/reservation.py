from extensions import db
from sqlalchemy.sql import text


class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(), nullable=False)
    end_time = db.Column(db.DateTime(), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    reserved_by = db.Column(db.String(100), nullable=False)
    workspace = db.Column(db.String(30), nullable=False)

    @classmethod
    def show_all(cls):
        return cls.query.order_by(text('-id')).all()

    @classmethod
    def show_mine(cls, name):
        return cls.query.filter_by(reserved_by=name).all()

    @classmethod
    def find_by_id(cls, identity):
        return cls.query.filter_by(identity).first()

    @classmethod
    def find_by_user(cls, name):
        return cls.query.filter_by(reservered_by=name).all()

    @classmethod
    def find_by_workspace(cls, number):
        return cls.query.filter_by(workspace=number).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
