from application import db

class Equipment(db.Model):

    __tablename__ = 'equipment'

    equipment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(44), unique=True, nullable=False)

    observations = db.relationship("Observation", backref='equipment', lazy=True)

    def __init__(self, name):
        self.name = name