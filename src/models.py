from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)

    #Relationships 
    favorites = db.relationship("Favorites", backref="favorites", lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    #Relationships
    people = db.relationship("People", backref="people", lazy=True)
    planets = db.relationship("Planets", backref="planets", lazy=True)
    vehicles = db.relationship("Vehicles", backref="vehicles", lazy=True)
    

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False) 
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)

    favorite_id = db.Column(db.Integer, db.ForeignKey("favorites.id"))

    def __repr__(self):
        return f"<Person: {self.name}>"
    
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

    favorite_id = db.Column(db.Integer, db.ForeignKey("favorites.id"))

    def __repr__(self):
        return f"<Planet: {self.name}>"
    
    def serialze(self):
        return {
            "id": self.id,
            "name": self.name,
            "orbital_period": self.orbital_period,
            "population": self.population
        }

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    manufacturer = db.Column(db.String(50), nullable=False)
    max_speed = db.Column(db.Integer, nullable=False)

    favorite_id = db.Column(db.Integer, db.ForeignKey("favorites.id"))

    def __repr__(self):
        return f"<Vehicle: {self.name}"
    
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "manufacturer": self.manufacturer,
            "max_speed": self.max_speed
        }