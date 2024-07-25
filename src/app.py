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

@app.route('/users', methods=['POST'])
def create_user():
    body = request.json
    username = body.get("username", None)
    email = body.get("email", None)
    password = body.get("password", None)
    
    if username is None or email is None or password is None:
        return jsonify({"error": "Missing values!"}), 400
    
    email_exists = User.query.filter_by(email=email).first()
    if email_exists is not None:
        return jsonify({"error": "Email already in use!"}), 400
    
    user = User(username=username, email=email, password=password)
    try:
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return jsonify({"message": f"{user.username} created!"}), 201
    
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": f"{error}"}), 500


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    favorite_people = Favorite_People.query.all()
    favorite_planets = Favorite_Planet.query.all()
    serialized_people = [favorite_person.serialize() for favorite_person in favorite_people]
    serialized_planet = [favorite_planet.serialize() for favorite_planet in favorite_planets]
    return jsonify({"favorites": f"{serialized_people}" f"{serialized_planet}"}), 200

@app.route('/favorite/people', methods=['POST'])
def add_person_to_favorites():
    body = request.json
    user_id = body.get("user_id", None)
    people_id = body.get("people_id", None)
    
    person_exists = People.query.filter_by(id=people_id)
    if not person_exists:
        return jsonify({"error": "Person not found!"}), 404
    
    user_exists = User.query.filter_by(id=user_id)
    if not user_exists:
        return jsonify({"error": "User not found!"}), 404
    
    if user_id is None or people_id is None:
        return jsonify({"error": "Missing values!"}), 400
    
    favorite = Favorite_People.query.filter_by(user_id=user_id, id=people_id).first()
    if favorite:
        return jsonify({"message": "Person is already a favorite"}), 400

    new_favorite = Favorite_People(user_id=user_id, people_id=people_id)
    try:
        db.session.add(new_favorite)
        db.session.commit()
        db.session.refresh(new_favorite)
        return jsonify({"message": "Person added to favorites"}), 201
        
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": f"{error}"}), 500

@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_person_from_favorites(user_id, people_id):
    
    favorite = Favorite_People.query.filter_by(user_id=user_id, people_id=people_id).first()
    try:
        if not favorite:
            return jsonify({"error": "Person not in favorites"}), 404
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Person deleted from favorites!"}), 201
        
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500


@app.route('/favorite/planets', methods=['POST'])
def add_planet_to_favorites():
    body = request.json
    user_id = body.get("user_id", None)
    planet_id = body.get("planet_id", None)

    planet_exists = Planets.query.filter_by(id=planet_id)
    if not planet_exists:
        return jsonify({"error": "Planet not found!"}), 404

    user_exists = User.query.filter_by(id=user_id)
    if not user_exists:
        return jsonify({"error": "User not found!"}), 404

    if user_id is None or planet_id is None:
        return jsonify({"error": "Missing values!"}), 400
    
    favorite = Favorite_Planet.query.filter_by(user_id=user_id, id=planet_id).first()
    if favorite:
        return jsonify({"message": "Planet is already a favorite"}), 400
    
    new_favorite = Favorite_Planet(user_id=user_id, planet_id=planet_id)
    try:
        db.session.add(new_favorite)
        db.session.commit()
        db.session.refresh(new_favorite)
        return jsonify({"message": "Planet added to favorites"}), 200

    except Exception as error:
        db.session.rollback()
        return jsonify({"error": f"{error}"}), 500

@app.route('/users/<int:user_id>/favorite/planets/<int:planet_id>', methods=['DELETE'])
def remove_planet_from_favorites(user_id, planet_id):
    
    favorite = Favorite_Planet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    try:
        if not favorite:
            return jsonify({"error": "Planet not in favorites"}), 404
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Planet deleted from favorites!"}), 200
        
    except Exception as error:
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
        db.session.rollback()
        return jsonify({"error": f"{error}"}), 500

@app.route('/people/<int:id>', methods=['GET'])
def get_single_person(id):
    try:
        person = People.query.get(id)
        if person is None:
            return jsonify({"Person not found!"}), 404
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
        db.session.rollback()
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
