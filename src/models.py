from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)

    #Relationships 

    followers = db.relationship("Followers", backref="user_followers") 
    favorites = db.relationship("Followers", backref="user_favorites")

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
    charcaters = db.relationship("Favorites", backref="charcaters")
    planets = db.relationship("Favorites", backref="planets")
    vehicles = db.relationship("Favorites", backref="vehicles")
    

class Followers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_from_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user_to_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False) 
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)

    favorite_id = db.Column(db.Integer, db.ForeignKey("favorites.id"))


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)

    favorite_id = db.Column(db.Integer, db.ForeingKey("favorites.id"))

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    manufacturer = db.Column(db.String(50), nullable=False)
    max_speed = db.Column(db.Integer, nullable=False)

    favorite_id = db.Column(db.Integer, db.ForeignKey("favorites.id"))