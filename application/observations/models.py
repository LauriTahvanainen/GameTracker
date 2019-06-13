from application import db
from sqlalchemy.sql import text
from flask_login import current_user
from application.equipments.models import Equipment
from application.animals.models import Animal


class Observation(db.Model):
    observation_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.account_id'), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    date_observed = db.Column(db.DateTime, nullable=False)
    city = db.Column(db.String(144), nullable=False)
    latitude = db.Column(db.Numeric, nullable=False)
    longitude = db.Column(db.Numeric, nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey(
        "animal.animal_id"), nullable=False)
    weight = db.Column(db.Numeric)
    sex = db.Column(db.Integer)
    observ_type = db.Column(db.Integer)
    equipment_id = db.Column(db.Integer, db.ForeignKey(
        "equipment.equipment_id"), nullable=False)
    info = db.Column(db.String(500))

    def __init__(self, account_id, date_observed, city, latitude, longitude, animal_id, weight, sex, observ_type, equipment_id, info):
        self.account_id = account_id
        self.date_observed = date_observed
        self.city = city
        if latitude is not None:
            self.latitude = latitude
        else:
            self.latitude = 404
        if longitude is not None:
            self.longitude = longitude
        else:
            self.longitude = 404
        self.animal_id = animal_id
        self.weight = weight
        if weight is not None:
            self.weight = weight
        else:
            self.weight = -404
        self.sex = sex
        self.observ_type = observ_type
        self.equipment_id = equipment_id
        self.info = info

    @staticmethod
    def list_users_own_observations_by_observ_date():
        stmt = text("SELECT Observation.observation_id,"
                    " Observation.date_created,"
                    " Observation.date_modified,"
                    " Observation.date_observed,"
                    " Observation.city,"
                    " Observation.latitude,"
                    " Observation.longitude,"
                    " Animal.name,"
                    " Observation.weight,"
                    " Observation.sex,"
                    " Observation.observ_type,"
                    " Equipment.name,"
                    " Observation.info"
                    " FROM Observation"
                    " LEFT JOIN Equipment ON Equipment.equipment_id = Observation.equipment_id"
                    " LEFT JOIN Animal ON Animal.animal_id = Observation.animal_id"
                    " WHERE (Observation.account_id = :cur_user)"
                    " GROUP BY Observation.date_observed, Observation.observation_id, Animal.name, Equipment.name").params(cur_user=current_user.account_id)

        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"Havaintonumero": row[0], "Luotu": row[1], "Muokattu": row[2],
                             "Havaittu": row[3], "Kaupunki": row[4], "Leveysaste": row[5],
                             "Pituusaste": row[6], "Elain": row[7], "Paino": row[8],
                             "Sukupuoli": row[9], "Havaintotapa": row[10], "Valine": row[11],
                             "Lisatiedot": row[12]})

        return response

    @staticmethod
    def list_filtered(form, cur_id=-1):
        query = db.session.query(Observation, Animal, Equipment.name).outerjoin(Animal).outerjoin(Equipment).group_by(Observation.observation_id)
        
        # Filters
        query = query.filter(Observation.account_id == cur_id)
        if form.date_observedLow.data is not None:
            query = query.filter(Observation.date_observed >= form.date_observedLow.data)
        if form.date_observedHigh.data is not None:
            query = query.filter(Observation.date_observed <= form.date_observedHigh.data)
        if form.city.data:
            query = query.filter(Observation.city.in_(form.city.data))
        if form.latitudeLow.data is not None:
            query = query.filter(Observation.latitude >= form.latitudeLow.data)
        if form.latitudeHigh.data is not None:
            query = query.filter(Observation.latitude >= form.latitudeHigh.data)
        if form.longitudeLow.data is not None:
            query = query.filter(Observation.longitude >= form.longitudeLow.data)
        if form.longitudeHigh.data is not None:
            query = query.filter(Observation.longitude >= form.longitudeHigh.data)
        if form.animal.data:
            query = query.filter(Animal.animal_id.in_(form.animal.data))
        if form.weightLow.data is not None:
            query = query.filter(Observation.weight >= form.weightLow.data)
        if form.weightHigh.data is not None:
            query = query.filter(Observation.weight >= form.weightHigh.data)
        if form.sex.data:
            query = query.filter(Observation.sex.in_(form.sex.data))
        if form.observ_type.data:
            query = query.filter(Observation.observ_type.in_(form.observ_type.data))
        if form.equipment.data:
            query = query.filter(Equipment.equipment_id.in_(form.equipment.data))
        if form.info.data != '':
            query = query.filter(Observation.info == form.info.data)

        res = query.order_by(Observation.date_observed.desc()).all() 

        response = []
        for row in res:
            response.append({"Havaintonumero": row[0].observation_id, "Luotu": row[0].date_created, "Muokattu": row[0].date_modified,
                             "Havaittu": row[0].date_observed, "Kaupunki": row[0].city, "Leveysaste": row[0].latitude,
                             "Pituusaste": row[0].longitude, "Elain": row[1].name, "Paino": row[0].weight,
                             "Sukupuoli": row[0].sex, "Havaintotapa": row[0].observ_type, "Valine": row[2],
                             "Lisatiedot": row[0].info})

        return response
