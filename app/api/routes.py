from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Vehicle, vehicle_schema, vehicles_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee' : 'haw'}

@api.route('/vehicles', methods = ['POST'])
@token_required
def create_vehicle(current_user_token):
    vin = request.json['vin']
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    description = request.json['description']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    vehicle = Vehicle(vin, make, model, year, color, description, user_token = user_token )

    db.session.add(vehicle)
    db.session.commit()

    response = vehicle_schema.dump(vehicle)
    return jsonify(response)

@api.route('/vehicles', methods = ['GET'])
@token_required
def get_vehicle(current_user_token):
    a_user = current_user_token.token
    vehicles = Vehicle.query.filter_by(user_token = a_user).all()
    response = vehicles_schema.dump(vehicles)
    return jsonify(response)

@api.route('/vehicles/<id>', methods = ['GET'])
@token_required
def get_single_vehicle(current_user_token, id):
    vehicle = Vehicle.query.get(id)
    response = vehicle_schema.dump(vehicle)
    return jsonify(response)

@api.route('/vehicles/<id>', methods = ['POST','PUT'])
@token_required
def update_vehicle(current_user_token,id):
    vehicle = Vehicle.query.get(id) 
    vehicle.vin = request.json['vin']
    vehicle.make = request.json['make']
    vehicle.model = request.json['model']
    vehicle.year = request.json['year']
    vehicle.color = request.json['color']
    vehicle.description = request.json['description']
    vehicle.user_token = current_user_token.token

    db.session.commit()
    response = vehicle_schema.dump(vehicle)
    return jsonify(response)

@api.route('/vehicles/<id>', methods = ['DELETE'])
@token_required
def delete_vehicle(current_user_token, id):
    vehicle = Vehicle.query.get(id)
    db.session.delete(vehicle)
    db.session.commit()
    response = vehicle_schema.dump(vehicle)
    return jsonify(response)

