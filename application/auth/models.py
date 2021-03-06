from application import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text
from flask_login import current_user
from application.models import Base
import random
import string

class User(Base):
    __tablename__ = "account"

    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), nullable=False, unique=True)
    name = db.Column(db.String(144))
    password = db.Column(db.String, nullable=False)
    salt = db.Column(db.String(6), nullable=False)
    city = db.Column(db.String(144))
    age = db.Column(db.Integer)
    urole = db.Column(db.String(10))
    suggestions_accepted = db.Column(db.Integer, default=0)
    suggestions_deleted = db.Column(db.Integer, default=0)

    observations = db.relationship(
        "Observation", backref='account', cascade="all,delete", lazy=True)
    added_animals = db.relationship(
        "Animal", backref='account', lazy=True)
    votes = db.relationship(
        "Vote", backref='account', cascade="all,delete", lazy=True)

    def __init__(self, username, name, password, city, age, urole):
        self.username = username
        self.name = name
        self.set_password(password)
        self.city = city
        self.age = age
        self.urole = urole

    def set_password(self, password):
        self.salt = User.generate_salt()
        self.password = generate_password_hash(password + self.salt)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.account_id).encode("utf-8").decode("utf-8")

    def get_urole(self):
        return self.urole

    @staticmethod
    def find_current_user_information(cur_id):
        stmt = text("SELECT Account.name, Account.city, Account.age "
                    "FROM Account WHERE Account.account_id = :acc_id").params(acc_id=cur_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append(
                {"name": row[0], "city": row[1], "age": row[2]})
        return response

    @staticmethod
    def list_all_users():
        stmt = text("SELECT Account.account_id, Account.username, Account.name, Account.city, Account.age "
                    "FROM Account")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append(
                {"username": row[0], "name": row[1], "city": row[2], "age": row[3]})
        return response

    @staticmethod
    def generate_salt():
        char_set = string.ascii_letters + string.digits
        salt = set()
        while not (len(salt) > 5):
            salt.add(char_set[random.randint(0,61)])
        salt = list(salt)
        salt = "".join(salt)
        return salt