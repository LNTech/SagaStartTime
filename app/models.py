"""Flask SqlAlchemy models"""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Location(db.Model):
    __tablename__ = "Locations"

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('Countries.id'))
    name = db.Column(db.String)
    lat = db.Column(db.String)
    lon = db.Column(db.String)


class Country(db.Model):
    __tablename__ = "Countries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
