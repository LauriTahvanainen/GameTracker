from application import db
from application.models import Base

class Animal(Base):
    
    __tablename__ = 'animal'

    animal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(144), nullable=False, unique=True)
    lat_name = db.Column(db.String(144), unique=True)
    info = db.Column(db.String)

    observations = db.relationship("Observation", backref='animal', lazy=True)

    def __init__(self, name, lat_name, info):
        self.name = name
        self.lat_name = lat_name
        self.info = info

