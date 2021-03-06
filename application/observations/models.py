from application import db
from sqlalchemy.sql import text
from sqlalchemy import Index
from flask_login import current_user
from application.equipments.models import Equipment
from application.animals.models import Animal
from application.auth.models import User
from application.models import Base
from datetime import datetime, time


class Observation(Base):
    observation_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.account_id'), nullable=False, index=True)
    datetime_observed = db.Column(db.DateTime, nullable=False, index=True)
    date_observed = db.Column(db.Date, nullable=False, index=True)
    time_observed = db.Column(db.Time, nullable=False, index=True)
    city = db.Column(db.String(144), nullable=False, index=True)
    latitude = db.Column(db.Numeric)
    longitude = db.Column(db.Numeric)
    animal_id = db.Column(db.Integer, db.ForeignKey(
        "animal.animal_id", ondelete='CASCADE'), nullable=False, index=True)
    weight = db.Column(db.Numeric)
    sex = db.Column(db.Integer)
    observ_type = db.Column(db.Integer, index=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey(
        "equipment.equipment_id", ondelete='SET NULL'), index=True)
    info = db.Column(db.String(500), index=True)

    Index('obsAndDate', observ_type, date_observed)
    Index('obsAndAnimal', observ_type, animal_id)
    Index('cityAndAnimal', city, animal_id)
    Index('equipAndAnimal', equipment_id, animal_id)

    def __init__(self, account_id, date_observed, time_observed, datetime_observed, city, latitude, longitude, animal_id, weight, sex, observ_type, equipment_id, info):
        self.account_id = account_id
        self.date_observed = date_observed
        self.time_observed = time_observed
        self.datetime_observed = datetime_observed
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.animal_id = animal_id
        self.weight = weight
        self.weight = weight
        self.sex = sex
        self.observ_type = observ_type
        self.equipment_id = equipment_id
        self.info = info

    # can be used for showing results of one user, filtered or all, and results of all users, filtered or all.
    @staticmethod
    def list_filtered(form, page_num, cur_id=-1):
        query = db.session.query(Observation, Animal, Equipment.name, User).outerjoin(Animal,Observation.animal_id == Animal.animal_id).outerjoin(Equipment,Observation.equipment_id == Equipment.equipment_id).outerjoin(
            User,User.account_id == Observation.account_id).group_by(Observation.observation_id, Animal.animal_id, Equipment.equipment_id, User.account_id)

        # Filters
        if cur_id != -1:
            query = query.filter(Observation.account_id == cur_id)
        if form.username.data is not None and form.username.data != "":
            query = query.filter(User.username == form.username.data)
        query = filter_dates(query, form)
        if form.city.data:
            query = query.filter(Observation.city.in_(form.city.data))
        if form.latitude_low.data is not None:
            query = query.filter(Observation.latitude >= form.latitude_low.data)
        if form.latitude_high.data is not None:
            query = query.filter(Observation.latitude <=
                                 form.latitude_high.data)
        if form.longitude_low.data is not None:
            query = query.filter(Observation.longitude >=
                                 form.longitude_low.data)
        if form.longitude_high.data is not None:
            query = query.filter(Observation.longitude <=
                                 form.longitude_high.data)
        if form.animal.data:
            query = query.filter(Animal.animal_id.in_(form.animal.data))
        if form.weight_low.data is not None:
            query = query.filter(Observation.weight >= form.weight_low.data)
        if form.weight_high.data is not None:
            query = query.filter(Observation.weight <= form.weight_high.data)
        if form.sex.data:
            query = query.filter(Observation.sex.in_(form.sex.data))
        if form.observ_type.data:
            query = query.filter(
                Observation.observ_type.in_(form.observ_type.data))
        if form.equipment.data:
            query = query.filter(
                Equipment.equipment_id.in_(form.equipment.data))
        if form.info.data != '' and form.info.data is not None:
            query = query.filter(Observation.info == form.info.data)

        if page_num == 0:
            return query.order_by(Observation.datetime_observed.desc())
        return query.order_by(Observation.datetime_observed.desc()).paginate(page_num, 10, False)

    @staticmethod
    def count_observations_on_user(account_id):
        stmt = text("SELECT COUNT(Observation.observation_id) as obs_count"
                    " FROM Observation WHERE Observation.account_id = :acc_id").params(acc_id=account_id)
        res = db.engine.execute(stmt)
        return res.fetchone()['obs_count']

    @staticmethod
    def list_top_users():
        stmt = text("SELECT Account.account_id, Account.username, COUNT(Observation.observation_id) AS count FROM Observation"
                    " LEFT JOIN Account ON Observation.account_id = Account.account_id"
                    " GROUP BY Account.account_id"
                    " ORDER BY count DESC"
                    " LIMIT 10")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append(
                {"id": row[0], "username": row[1], "count": row[2]})
        return response

    @staticmethod
    def list_users_without_observations():
        stmt = text("SELECT Account.account_id, Account.username, Account.date_created FROM Account"
                    " LEFT JOIN Observation ON Observation.account_id = Account.account_id"
                    " GROUP BY Account.account_id"
                    " HAVING COUNT(Observation.observation_id) = 0"
                    " ORDER BY Account.date_created ASC"
                    " LIMIT 10")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append(
                {"id": row[0], "username": row[1], "created": row[2]})
        return response

    @staticmethod
    def list_top_animals():
        stmt = text("SELECT Animal.animal_id, Animal.name, Animal.lat_name, Animal.info, COUNT(Observation.observation_id) as count, AVG(Observation.weight) as avg FROM Animal"
                    " LEFT JOIN Observation ON (Animal.animal_id = Observation.animal_id)"
                    " WHERE Animal.suggestion_flag = '0'"
                    " GROUP BY Animal.animal_id"
                    " ORDER BY count DESC, Animal.name"
                    " LIMIT 10")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append(
                {"id": row[0], "name": row[1], "lat_name": row[2], "info": row[3], "count": row[4], "avg":row[5]})
        return response

    @staticmethod
    def list_bottom_animals():
        stmt = text("SELECT Animal.animal_id, Animal.name, Animal.lat_name, Animal.info, COUNT(Observation.observation_id) as count, AVG(Observation.weight) as avg FROM Animal"
                    " LEFT JOIN Observation ON (Animal.animal_id = Observation.animal_id)"
                    " WHERE Animal.suggestion_flag = '0'"
                    " GROUP BY Animal.animal_id"
                    " ORDER BY count ASC, Animal.name"
                    " LIMIT 10")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append(
                {"id": row[0], "name": row[1], "lat_name": row[2], "info": row[3], "count": row[4], "avg":row[5]})
        return response

    @staticmethod
    def list_top_equipment():
        stmt = text("SELECT Equipment.equipment_id, Equipment.name, COUNT(Observation.observation_id) as count FROM Equipment"
                    " LEFT JOIN Observation ON (Equipment.equipment_id = Observation.equipment_id)"
                    " GROUP BY Equipment.equipment_id"
                    " ORDER BY count DESC, Equipment.name"
                    " LIMIT 10")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id": row[0], "name": row[1], "count": row[2]})
        return response

    @staticmethod
    def list_bottom_equipment():
        stmt = text("SELECT Equipment.equipment_id, Equipment.name, COUNT(Observation.observation_id) as count FROM Equipment"
                    " LEFT JOIN Observation ON (Equipment.equipment_id = Observation.equipment_id)"
                    " GROUP BY Equipment.equipment_id"
                    " ORDER BY count ASC, Equipment.name"
                    " LIMIT 10")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id": row[0], "name": row[1], "count": row[2]})
        return response

    @staticmethod
    def list_most_hunted_animals():
        stmt = text("SELECT Animal.animal_id, Animal.name, Animal.lat_name, Animal.info, COUNT(Observation.observation_id) as count, AVG(Observation.weight) as avg FROM Animal"
                    " LEFT JOIN Observation ON (Animal.animal_id = Observation.animal_id)"
                    " WHERE Observation.observ_type = 0 and Animal.suggestion_flag = '0'"
                    " GROUP BY Animal.animal_id"
                    " ORDER BY count DESC, Animal.name"
                    " LIMIT 10")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append(
                {"id": row[0], "name": row[1], "lat_name": row[2], "info": row[3], "count": row[4], "avg":row[5]})
        return response

def filter_dates(query, form):
    date_observed_low = form.date_observed_low.data
    date_observed_high = form.date_observed_high.data
    time_low1 = form.time_low1.data
    time_low2 = form.time_low2.data
    time_high1 = form.time_high1.data
    time_high2 = form.time_high2.data

    if date_observed_low is not None:
        if time_low1 is not None:
            dateFilter = datetime.combine(date_observed_low, time_low1)
        else:
            dateFilter = datetime.combine(date_observed_low, time(0,0))
        query = query.filter(Observation.datetime_observed >= dateFilter)
    if date_observed_high is not None:
        if time_high1 is not None:
            dateFilter = datetime.combine(date_observed_high, time_high1)
        else:
            dateFilter = datetime.combine(date_observed_high, time(23,59))
        query = query.filter(Observation.datetime_observed <= dateFilter)
    if time_low2 is not None:
        timeFilter = time_low2
        query = query.filter(Observation.time_observed >= timeFilter)
    if time_high2 is not None:
        timeFilter = time_high2
        query = query.filter(Observation.time_observed <= timeFilter)
    return query
