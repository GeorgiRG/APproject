from extensions import db


class Workspace(db.Model):

    __tablename__ = 'workspace'
    id = db.Column(db.Integer, primary_key=True)
    workspace_number = db.Column(db.String(30), nullable=False, unique=True)
    turkuamk_only = db.Column(db.Boolean(), default=False)
    available_space = db.Column(db.Integer)

    def info(self):
        return {
            'id': self.id,
            'workspace_number': self.workspace_number,
            'turkuamk_only': self.turkuamk_only,
            'available_space': self.available_space
                }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, workspace_id):
        return cls.query.filter_by(id=workspace_id).first()

    @classmethod
    def get_by_number(cls, workspace_number):
        return cls.query.filter_by(workspace_number=workspace_number).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()