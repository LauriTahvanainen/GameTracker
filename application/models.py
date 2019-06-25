from application import db
from sqlalchemy import Index

class Base(db.Model):

    __abstract__ = True

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp(), index=True)
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())