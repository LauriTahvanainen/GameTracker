from application import db
from application.models import Base

class Animal(Base):
    
    __tablename__ = 'animal'

    animal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(144), nullable=False, unique=True)
    lat_name = db.Column(db.String(144), nullable=True, unique=True)
    info = db.Column(db.String)
    suggestion_flag = db.Column(db.Boolean, nullable=False)
    voted_flag = db.Column(db.Boolean, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.account_id"))
    votes_num = db.Column(db.Integer, default=0)

    votes =  db.relationship(
        "Vote", backref='animal', lazy=True)

    observations = db.relationship("Observation", backref='animal', lazy=True)

    def __init__(self, name, lat_name, info, suggestion_flag, voted_flag, account_id):
        self.name = name
        self.lat_name = lat_name
        self.info = info
        self.suggestion_flag = suggestion_flag
        self.voted_flag = voted_flag
        self.account_id = account_id
        self.votes_num = 0

## Might be used when implementing proposing for editing of existing animals 
# class AnimalSuggestion(Base):
    
#     __tablename__ = 'animal_suggestion'

#     suggestion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(144), nullable=False)
#     lat_name = db.Column(db.String(144))
#     info = db.Column(db.String)
#     account_id = db.Column(db.Integer, db.ForeignKey("account.account_id"), nullable=False)
#     votes_num = db.Column(db.Integer)

#     votes =  db.relationship(
#         "Vote", backref='animal_suggestion', lazy=True)


#     def __init__(self, name, lat_name, info, account_id):
#         self.name = name
#         self.lat_name = lat_name
#         self.info = info
#         self.account_id = account_id
#         self.votes_num = 0
