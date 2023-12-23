"""Flask SqlAlchemy models"""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Location(db.Model):
    """Sqlite model for 'Location'"""
    __tablename__ = "Locations"


    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('Countries.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    lat = db.Column(db.String, nullable=False)
    lon = db.Column(db.String, nullable=False)


class Country(db.Model):
    """Sqlite model for 'Country'"""
    __tablename__ = "Countries"


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
