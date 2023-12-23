"""Flask API webserver to store and serve start times"""

from os.path import exists
from flask import Flask, request, jsonify, render_template
from astral import CivilTwilight
from models import db, Country, Location

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)


def check_values(*args):
    """Checks if any of the values provided are blank or none"""
    for arg in args:
        if arg == "" or arg is None:
            return True
    return False


@app.route("/api/countries", methods=["GET"])
def get_countries():
    """Returns all countries"""
    countries = Country.query.all()
    jsonified = []

    for country in countries:
        country = country.__dict__
        country.pop('_sa_instance_state')
        jsonified.append(country)

    return jsonified

@app.route("/api/countries", methods=["POST"])
def add_country():
    """Adds a country to the database"""
    name = request.form.get("name")

    if check_values(name):
        return jsonify({"message": "Invalid form data."}), 400

    if Country.query.filter_by(name=name).first():
        return jsonify({"message": "Country already present in database."}), 400

    country = Country(name=name)

    db.session.add(country)
    db.session.commit()
    db.session.refresh(country)

    return jsonify({"message": f"Added new country ID: {country.id}"}), 200

@app.route("/api/locations/by_country", methods=["GET"])
def locations_by_country():
    """Gets locations given a country ID"""
    country_id = request.args.get('country_id')

    if check_values(country_id):
        return jsonify({"message": "Invalid form data."}), 400

    if country_id.isdigit():
        country_id = int(country_id)
    else:
        return jsonify({"message": "Invalid country ID data."}), 400

    locations = Location.query.filter_by(country_id=country_id)
    jsonified = []

    for location in locations:
        location = location.__dict__
        location.pop('_sa_instance_state')
        jsonified.append(location)

    return {"country_id": country_id, "locations": jsonified}


@app.route("/api/locations", methods=["GET"])
def get_locations():
    """Gets all locations"""
    locations = Location.query.all()
    jsonified = []

    for location in locations:
        location = location.__dict__
        location.pop('_sa_instance_state')
        jsonified.append(location)

    return jsonified

@app.route("/api/locations", methods=["POST"])
def add_location():
    """Adds a location to the database"""
    name = request.form.get("name")
    lat = request.form.get("lat")
    lon = request.form.get("lon")
    country_id = request.form.get("country_id")

    if check_values(name, lat, lon, country_id):
        return jsonify({"message": "Invalid form data."}), 400

    if Location.query.filter_by(name=name, country_id=country_id).first():
        return jsonify({"message": "Location already present in database."})

    location = Location(country_id=country_id, name=name, lat=lat, lon=lon)

    db.session.add(location)
    db.session.commit()
    db.session.refresh(location)

    return jsonify({"message": f"Added new location ID: {location.id}"}), 200


@app.route("/api/start_time", methods=["GET"])
def get_start_time():
    """Get treatment start time"""
    location_id = request.args.get('loc_id')
    
    if check_values(location_id):
        return jsonify({"message": "Invalid form data."}), 400
    
    if location_id.isdigit():
        location_id = int(location_id)
    else:
        return jsonify({"message": "Invalid location ID data."}), 400

    location = Location.query.filter_by(id=location_id).first()
    if location is None:
        return jsonify({"message": "Cannot find location with that name."}), 400

    twilight = CivilTwilight()
    times = twilight.calculate(location.lat, location.lon)

    return jsonify({"location_id": location.id, "times": times}), 200


if __name__ == "__main__":
    if not exists("instance/database.db"):
        print("First time loading server, creating database and tables...")
        with app.app_context():
            db.create_all()

    app.run(host='0.0.0.0')
