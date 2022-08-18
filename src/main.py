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

@app.route('/users', methods=['POST'])
def post_users():

    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    people = request.json.get('people')
    

    user = User()
    user.username =  username
    user.email = email
    user.password = password
    user.people = people
    
    user.save()

    return jsonify(user.serialize_with_favs()), 201

@app.route('/people', methods=['GET'])
def get_people():
    people = Person.query.all()
    people = list(map(lambda person: person.serialize(), people))

    return jsonify(people), 200

@app.route('/people', methods=['POST'])
def post_people():
    name = request.json.get('name')
    url = request.json.get('url')

    people = Person()
    people.name =  name
    people.url = url
    
    people.save()

    return jsonify(people), 201

@app.route('/people', methods=['PUT'])
def put_people(id):
    name = request.json.get('name')
    url = request.json.get('url')
    

    people = Person()
    people.name =  name
    people.url = url
    
    people.update()

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

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
