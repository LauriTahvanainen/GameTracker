from application import db


class User(db.Model):
    __tablename__ = "account"

    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), nullable=False, unique=True)
    name = db.Column(db.String(144))
    password = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(144))
    age = db.Column(db.Integer)

    observations = db.relationship("Observation", backref='account', lazy=True)

    def __init__(self, username, name, password, city, age):
        self.username = username
        self.name = name
        self.password = password
        self.city = city
        self.age = age

    def get_id(self):
        return self.account_id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
