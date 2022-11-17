from flask import Blueprint, request, jsonify
from car_inventory.helpers import token_required
from car_inventory.models import db, Dog, dog_schema, dogs_schemas

api = Blueprint('api', __name__, url_prefix ='/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'some': 'value'}

# Crud = Create Dog Endpoint (POST)
@api.route('/dogs', methods = ['POST'])
@token_required
def create_dog(current_user_token):
    name = request.json['name']
    breed = request.json['breed']
    age = request.json['age']
    weight = request.json['weight']
    favorite_toy = request.json['favorite_toy']
    user_token = current_user_token.token

    print(f"User Token: {current_user_token.token}")
    
    dog = Dog(name, breed, age, weight, favorite_toy, user_token=user_token)
    db.session.add(dog)
    db.session.commit()

    response = dog_schema.dump(dog)
    return jsonify(response)

# cRud = Retrieve ALL Dogs Endpoints (GET)
@api.route('/dogs', methods=['GET'])
@token_required
def get_dogs(current_user_token):
    owner = current_user_token.token # current_user_token == user
    dogs = Dog.query.filter_by(user_token=owner).all()
    response = dogs_schemas.dump(dogs)
    return jsonify(response)

# cRud = Retrieve ONE Dog Endpoint via ID (GET)
@api.route('/dogs/<id>', methods=['GET'])
@token_required
def get_dog(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        dog = Dog.query.get(id)
        response = dog_schema.dump(dog)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401

# crUd = Update Dog Endpoint (PUT/POST)
@api.route('/dogs/<id>', methods = ['POST', 'PUT'])
@token_required
def update_dog(current_user_token, id):
    dog = Dog.query.get(id)
    dog.name = request.json['name']
    dog.breed = request.json['breed']
    dog.age = request.json['age']
    dog.weight = request.json['weight']
    dog.favorite_toy = request.json['favorite_toy']
    dog.user_token = current_user_token.token

    db.session.commit()
    response = dog_schema.dump(dog)
    return jsonify(response)

# cruD = Delete Dog Endpoing (DELETE)
@api.route('/dogs/<id>', methods = ['DELETE'])
@token_required
def delete_dog(current_user_token, id):
    dog = Dog.query.get(id)
    db.session.delete(dog)
    db.session.commit()
    response = dog_schema.dump(dog)
    return jsonify(response)