from application import db
from sqlalchemy.sql import text
from flask_login import current_user

class Observation(db.Model):
    observation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())
    date_observed = db.Column(db.DateTime, nullable=False)
    city = db.Column(db.String(144), nullable=False)
    latitude = db.Column(db.Numeric, nullable=False)
    longitude = db.Column(db.Numeric, nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey("animal.animal_id"), nullable=False)
    weight = db.Column(db.Numeric)
    sex = db.Column(db.Integer)
    observ_type = db.Column(db.Integer)
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.equipment_id"), nullable=False)
    info = db.Column(db.String(500))

    def __init__(self, account_id, date_observed, city, latitude, longitude, animal_id, weight, sex, observ_type, equipment_id, info):
        self.account_id = account_id
        self.date_observed = date_observed
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.animal_id = animal_id
        self.weight = weight
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
<<<<<<< HEAD
                     " GROUP BY Observation.date_observed, Observation.observation_id, Animal.name").params(cur_user=current_user.account_id)
=======
                     " GROUP BY Observation.date_observed, Observation.observation_id").params(cur_user=current_user.account_id)
>>>>>>> 6d3ebdbfb085c5217f123166ffbf4b7bfed2dbb3
        
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"Havaintonumero":row[0], "Luotu":row[1], "Muokattu":row[2], 
                            "Havaittu":row[3], "Kaupunki":row[4], "Leveysaste":row[5], 
                            "Pituusaste":row[6], "Elain":row[7], "Paino":row[8], 
                            "Sukupuoli":row[9], "Havaintotapa":row[10], "Valine":row[11], 
                            "Lisatiedot":row[12]})

        return response