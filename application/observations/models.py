from application import db

class Observation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
        
