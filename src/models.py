from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PersonUser(db.Model):
    __tablename__ = 'people_user'
    people_name = db.Column(db.Integer, db.ForeignKey('people.name', ondelete='CASCADE'), primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)

class PlanetUser(db.Model):
    __tablename__ = 'planets_user'
    planets_name = db.Column(db.Integer, db.ForeignKey('planets.name', ondelete='CASCADE'), primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    people = db.relationship('Person', secondary="people_user") # JOIN SQL MANY TO MANY
    planets = db.relationship('Planet', secondary="planets_user") # JOIN SQL MANY TO MANY

    def serialize(self):
        return{
            "id" : self.id,
            "username": self.username,
            "email" : self.email 
        }

    def serialize_with_favs(self):
        return{
            "id" : self.id,
            "username": self.username,
            "email" : self.email,
            "people": self.get_fav_people(),
            
        }

    def get_fav_people(self):
        return list(map(lambda person:{"name": people.name}, self.people))
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    

class Person(db.Model):
    __tablename__ = 'people'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return{
            "id" : self.id,
            "name": self.name,
            "url" : self.url
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Planet(db.Model):
    __tablename__ = 'planets'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return{
            "id" : self.id,
            "name": self.name,
            "url" : self.url
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()