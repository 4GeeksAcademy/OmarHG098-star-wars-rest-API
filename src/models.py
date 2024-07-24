from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False, default=True)

    #Relationships 
    favorite_people = db.relationship("Favorite_People", backref="user_favorite_people", lazy=True)
    favorite_planet = db.relationship("Favorite_Planet", backref="user_favorite_planet", lazy=True)

    def __repr__(self):
        return f"<Users {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
    
class Favorite_People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"))

class Favorite_Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False) 
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)

    #relationship
    favorite_people = db.relationship("Favorite_People", backref="favorite_people", lazy=True)

    def __repr__(self):
        return "<People %r>" % self.name 
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)

    favorite_planet = db.relationship("Favorite_Planet", backref="favorite_planet", lazy=True)

    def __repr__(self):
        return f"<Planet: {self.name}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "orbital_period": self.orbital_period,
            "population": self.population
        }
