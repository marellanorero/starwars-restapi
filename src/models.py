from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


people_user = db.Table('people_user',
    db.Column('people_id', db.Integer, db.ForeignKey('people.id', ondelete='CASCADE'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
)

 
planets_user = db.Table('planets_user',
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id', ondelete='CASCADE'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
   
    people = db.relationship('Person', cascade="all, delete", secondary="people_user", lazy='joined',
        backref=db.backref('users', lazy=True)) # JOIN SQL MANY TO MANY
    planets = db.relationship('Planet', cascade="all, delete", secondary="planets_user", lazy='joined',
        backref=db.backref('users', lazy=True)) # JOIN SQL MANY TO MANY
    


    def __repr__(self):
        return '<User %r>' % self.usersname


    def serialize(self):
        return{
            "id" : self.id,
            "username": self.username,
            "email" : self.email,
        }
    
    def serialize_with_favs(self):
        return {
            "people": list(map(lambda person: person.serialize(), self.people)),
            "planets": list(map(lambda planet: planet.serialize(), self.planet))
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
    
    people_user = db.relationship('User', secondary="people_user", lazy='joined',
        backref=db.backref('people', lazy=True)) # JOIN SQL MANY TO MANY
    
    def __repr__(self):
        return '<Person %r>' % self.name

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
    planets_user = db.relationship('User', secondary="planets_user", lazy='joined',
        backref=db.backref('planets', lazy=True)) # JOIN SQL MANY TO MAN
    def __repr__(self):
        return '<Planet %r>' % self.name

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