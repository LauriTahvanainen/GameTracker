from application import db

class Equipment(db.Model):

    __tablename__ = 'equipment'

    equipment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(44), unique=True, nullable=False)
    catch_type_allowed = db.Column(db.Boolean, nullable=False)
    road_accident_type_allowed = db.Column(db.Boolean, nullable=False)
    capture_type_allowed = db.Column(db.Boolean, nullable=False)
    sighting_type_allowed = db.Column(db.Boolean, nullable=False)
    accident_type_allowed = db.Column(db.Boolean, nullable=False)

    observations = db.relationship("Observation", backref='equipment', lazy=True)

    def __init__(self, name, catch_type_allowed, sighting_type_allowed, capture_type_allowed, road_accident_type_allowed, accident_type_allowed):
        self.name = name
        self.catch_type_allowed = catch_type_allowed
        self.sighting_type_allowed = sighting_type_allowed
        self.capture_type_allowed = capture_type_allowed
        self.road_accident_type_allowed = road_accident_type_allowed
        self.accident_type_allowed = accident_type_allowed

    def get_allowed_value_by_index(self, index):
        if index == 0:
            return self.catch_type_allowed
        elif index == 1:
            return self.sighting_type_allowed
        elif index == 2:
            return self.capture_type_allowed
        elif index == 3:
            return self.road_accident_type_allowed
        else:
            return self.accident_type_allowed