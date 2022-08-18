from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    people_user = db.relationship('Person', cascade="all, delete", secondary="people_user", lazy='joined',
        backref=db.backref('users', lazy=True)) # JOIN SQL MANY TO MANY
    planets_user = db.relationship('Planet', cascade="all, delete", secondary="planets_user", lazy='joined',
        backref=db.backref('users', lazy=True)) # JOIN SQL MANY TO MANY

    def serialize(self):
        return{
            "id" : self.id,
            "username": self.username,
            "email" : self.email 
        }
    def serializeFavorites(self):
        return {
            "id": self.id,
            "characterfavorites": list(map(lambda x: x.serializebyUser(), self.people_user)),
            "planetfavorites": list(map(lambda x: x.serializebyUser(), self.planets_user)),
            
        }
    
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

class PersonFavorite(db.Model):
    __tablename__ : 'person_favorite'
    id = db.Column(db.Integer, primary_key=True),
    userid = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    personid = db.Column(db.Integer, db.ForeignKey('people.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<PersonFavorite %r>' % self.userid

    def serializebyUser(self):
        return {
            "id": self.id,
            "personid": self.personid,            
            
        }

    def serializebyPerson(self):
        return {
            "id": self.id,
            "userid": self.userid,            
        }

class PlanetFavorite(db.Model):
    __tablename__ = 'planet_favorite'
    id = db.Column(db.Integer, primary_key=True),
    userid = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    planetid = db.Column(db.Integer, db.ForeignKey('planet.id', ondelete='CASCADE'))

    
    def __repr__(self):
        return '<PlanetFavorite %r>' % self.userid

    def serializebyUser(self):
        return {
            "id": self.id,
            "planetid": self.planetid,            
            
        }

    def serializebyPlanet(self):
        return {
            "id": self.id,
            "userid": self.userid
        }