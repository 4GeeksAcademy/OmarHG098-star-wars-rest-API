"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorite_People, Favorite_Planet, People, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
     return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    serialized_users = [user.serialize() for user in users]
    return jsonify({"users": serialized_users}), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    favorites = Favorite.query.all()
    serialized_favorite = [favorite.serialize() for favorite in favorites]
    return jsonify({"favorites": serialized_favorite}), 200

@app.route('/favorite/people', methods=['POST'])
def add_person_to_favorites():
    body = request.json
    user_id = body.get("user_id", None)
    people_id = body.get("people_id", None)
    person = People.query.get(people_id)

    if not person:
        return jsonify({"error": "Person not found!"}), 404
    
    if user_id is None or people_id is None:
        return jsonify({"error": "Missing values!"}), 400

    new_favorite = Favorite_People(user_id, people_id)
    try:
        db.session.add(new_favorite)
        db.session.commit
        return jsonify({"message": "Person added to favorites"}), 200
        
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": f"{error}"}), 500


@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    serialized_people = [person.serialize() for person in people]
    return jsonify({"people": serialized_people}), 200

@app.route('/people', methods=['POST'])
def add_person():
    body = request.json
    name = body.get("name", None)
    height = body.get("height", None)
    mass = body.get("mass", None)

    if name is None or height is None or mass is None:
        return jsonify({"error": "Missing values"}), 400

    person_exists = People.query.filter_by(name=name).first()
    if person_exists is not None:
        return jsonify({"error": f"{name} already exists!"}), 400

    person = People(name=name, height=height, mass=mass)

    try:
        db.session.add(person)
        db.session.commit()
        db.session.refresh(person)
        return jsonify({"message": f"{person.name} created!"}), 201
        
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500

@app.route('/people/<int:id>', methods=['GET'])
def get_single_person(id):
    try:
        person = People.query.get(id)
        if person is None:
            return jsonify({"Character not found!"}), 404
        return jsonify({"person": person.serialize()}), 200
     
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500
    

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planets.query.all()
    serialized_planets = [planet.serialize() for planet in planets]
    return jsonify({"planets": serialized_planets}), 200

@app.route('/planets', methods=['POST'])
def add_planet():
    body = request.json
    name = body.get("name", None)
    orbital_period = body.get("orbital_period", None)
    population = body.get("population", None)

    if name is None or orbital_period is None or population is None:
        return jsonify({"error": "Missing values"}), 400

    planet_exists = Planets.query.filter_by(name=name).first()
    if planet_exists is not None:
        return jsonify({"error": f"{name} already exists!"}), 400

    planet = Planets(name=name, orbital_period=orbital_period, population=population)

    try:
        db.session.add(planet)
        db.session.commit()
        db.session.refresh(planet)
        return jsonify({"message": f"{planet.name} created!"}), 201
        
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500


@app.route('/planets/<int:id>', methods=['GET'])
def get_single_planet(id):
    try:
        planet = Planets.query.get(id)
        if planet is None:
            return jsonify({"Planet not found!"}), 400
        return jsonify({"planet": planet.serialize()}), 200
        
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
