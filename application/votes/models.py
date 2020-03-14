from application import db
from application.models import Base

class Vote(Base):
    vote_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Boolean, nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey("animal.animal_id"))
    account_id = db.Column(db.Integer, db.ForeignKey("account.account_id"), nullable=False)

    __table_args__ = (db.UniqueConstraint('animal_id', 'account_id', name='animal_account_unique_constraint'),)

    def __init__(self, value, animal_id, account_id):
        self.value = value
        self.animal_id = animal_id
        self.account_id = account_id
