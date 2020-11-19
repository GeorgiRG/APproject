from extensions import db


class Timeframes(db.Model):
    __tablename__ = 'timeframes'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(), nullable=False)
    end_time = db.Column(db.DateTime(), nullable=False)
    workspace = db.Column(db.String(30), nullable=False,)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    @classmethod
    def get_all(cls, workspace):
        return cls.query.filter_by(workspace=workspace).all()

    @classmethod
    def get_for_this_workspace(cls, workspace, user_id):
        return cls.query.filter_by(workspace=workspace, user_id=user_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
