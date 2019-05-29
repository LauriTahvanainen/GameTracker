from application import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text

class User(db.Model):
    __tablename__ = "account"

    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), nullable=False, unique=True)
    name = db.Column(db.String(144))
    password = db.Column(db.String, nullable=False)
    city = db.Column(db.String(144))
    age = db.Column(db.Integer)

    observations = db.relationship("Observation", backref='account', lazy=True)

    def __init__(self, username, name, password, city, age):
        self.username = username
        self.name = name
        self.set_password(password)
        self.city = city
        self.age = age

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.account_id).encode("utf-8").decode("utf-8")

    @staticmethod
    def find_current_user_information(cur_id):
        stmt = text("SELECT Account.username, Account.name, Account.city, Account.age "
                    "FROM Account WHERE Account.account_id = :acc_id").params(acc_id=cur_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"username":row[0], "name":row[1], "city":row[2], "age":row[3]})
        return response

    @staticmethod
    def list_all_users():
        stmt = text("SELECT Account.account_id, Account.username, Account.name, Account.city, Account.age "
                    "FROM Account")
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"username":row[0], "name":row[1], "city":row[2], "age":row[3]})
        return response