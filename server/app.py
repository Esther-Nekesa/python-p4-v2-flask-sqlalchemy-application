#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from models import db, Pet

app = Flask(__name__)
# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Linking the database and migration tools to the app
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    # Basic home route
    response = make_response(
        '<h1>Welcome to the pet directory!</h1>',
        200
    )
    return response

@app.route('/pets/<int:id>')
def pet_by_id(id):
    # Query for a single pet by ID
    pet = Pet.query.filter(Pet.id == id).first()

    if pet:
        # Success: Pet exists
        response_body = f'<p>{pet.name} {pet.species}</p>'
        response_status = 200
    else:
        # Error: Pet does not exist (404 Not Found)
        response_body = f'<p>Pet {id} not found</p>'
        response_status = 404

    response = make_response(response_body, response_status)
    return response

@app.route('/species/<string:species>')
def pet_by_species(species):
    # Query for all pets matching a specific species
    pets = Pet.query.filter_by(species=species).all()

    size = len(pets)
    # Start building the HTML response string
    response_body = f'<h2>There are {size} {species}s</h2>'
    
    # Loop through the list of pet objects
    for pet in pets:
        response_body += f'<p>{pet.name}</p>'
        
    response = make_response(response_body, 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)