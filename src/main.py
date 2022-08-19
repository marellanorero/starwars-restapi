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
from models import db, User, Person, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200

@app.route('/people', methods=['GET'])
def get_people():
    people = Person.query.all()
    people = list(map(lambda person: person.serialize(), people))

    return jsonify(people), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_person(id):
 
    person = Person.query.get(id)

    if person is None:
        return jsonify({"msg":"This person doesn't exist"})

    return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))

    return jsonify(planets), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
 
    planet = Planet.query.get(id)

    if planet is None:
        return jsonify({"msg":"This planet doesn't exist"})

    return jsonify(planet.serialize()), 200

@app.route('/users/favorites', methods=['GET'])
def get_favorites_people():

    people = User.query.get('people')
    

    if people is None:
        return jsonify({"msg":"Favorite is empty"})

    return jsonify(people.serialize_with_favs()), 200


@app.route('/users/favorites/people/<int:id>', methods=['POST'])
def get_favorite_person(id):

    person = Person.query.get(id)

    if person is None:
        return jsonify({"msg":"This person doesn't exist"})

    return jsonify(person.serialize_with_users()), 201

@app.route('/users/favorites/people/<int:id>', methods=['DELETE'])
def delete_favorite_people(id):

    person = Person.query.get(id)

    if(person == id):
        db.session.delete(id)
        db.session.commit()
    else:
        return jsonify({ "msg": "This person doesn't exist here" })

    return jsonify(person.serialize_with_users()), 200



@app.route('/users/favorites', methods=['GET'])
def get_favorites_planets():

    planet = User.query.get('planet')
    
    if planet is None:
        return jsonify({"msg":"Favorite is empty"})

    return jsonify(planet.serialize_with_favs()), 200

@app.route('/users/favorites/planets/<int:id>', methods=['POST'])
def get_favorite_planet(id):

    planet = Planet.query.get(id)

    if planet is None:
        return jsonify({"msg":"This planet doesn't exist"})

    return jsonify(planet.serialize_with_users()), 201

@app.route('/users/favorites/planets/<int:id>', methods=['DELETE'])
def delete_favorite_planet(id):

    planet = Planet.query.get(id)

    if(planet == id):
        db.session.delete(id)
        db.session.commit()
    else:
        return jsonify({ "msg": "This planets doesn't exist here" })

    return jsonify(planet.serialize_with_users()), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)