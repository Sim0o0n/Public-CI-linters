from flask import Blueprint, jsonify, request
from module_29_testing.hw.model import Client, Parking, ClientParking, db
from datetime import datetime

app_routes = Blueprint('app_routes', __name__)



@app_routes.route("/clients", methods=['GET'])
def get_clients():
    clients = Client.query.all()
    result = [
        {
            "id": client.id,
            "name": client.name,
            "surname": client.surname,
            "credit_card": client.credit_card,
            "car_number": client.car_number
        }
        for client in clients
    ]
    return jsonify(result)

@app_routes.route("/clients/<int:client_id>", methods=['GET'])
def get_client(client_id):
    client = Client.query.filter_by(id=client_id).first_or_404()
    result = {
        "id": client.id,
        "name": client.name,
        "surname": client.surname,
        "credit_card": client.credit_card,
        "car_number": client.car_number
    }
    return jsonify(result)

@app_routes.route("/clients", methods=['POST'])
def add_client():
    data = request.get_json()
    if not data or not all(key in data for key in ["name", "surname", "credit_card", "car_number"]):
        return jsonify({"error": "Missing required fields"}), 400

    new_client = Client(
        name=data["name"],
        surname=data["surname"],
        credit_card=data["credit_card"],
        car_number=data["car_number"]
    )
    db.session.add(new_client)
    db.session.commit()

    return jsonify({
        "id": new_client.id,
        "name": new_client.name,
        "surname": new_client.surname,
        "credit_card": new_client.credit_card,
        "car_number": new_client.car_number
    }), 201

@app_routes.route("/parkings", methods=['POST'])
def add_parking():
    data = request.get_json()
    required_fields = ["address", "opened", "count_places", "count_available_places"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_parking = Parking(
        address=data["address"],
        opened=data["opened"],
        count_places=data["count_places"],
        count_available_places=data["count_available_places"]
    )
    db.session.add(new_parking)
    db.session.commit()

    return jsonify({
        "id": new_parking.id,
        "address": new_parking.address,
        "opened": new_parking.opened,
        "count_places": new_parking.count_places,
        "count_available_places": new_parking.count_available_places
    }), 201

@app_routes.route("/client_parkings", methods=["POST"])
def usage_parking():
    data = request.get_json()

    if not data or "client_id" not in data or "parking_id" not in data:
        return jsonify({"error": "client_id and parking_id are required"}), 400

    client_id = data["client_id"]
    parking_id = data["parking_id"]

    parking = Parking.query.get(parking_id)
    if not parking:
        return jsonify({"error": "Parking not found"}), 404

    if not parking.opened:
        return jsonify({"error": "Parking is closed"}), 400

    if parking.count_available_places <= 0:
        return jsonify({"error": "No available places"}), 400

    new_usage = ClientParking(
        client_id=client_id,
        parking_id=parking_id,
        time_in=datetime.utcnow(),
        time_out=None
    )

    parking.count_available_places -= 1

    db.session.add(new_usage)
    db.session.commit()

    return jsonify({
        "message": "Client parked successfully",
        "client_id": client_id,
        "parking_id": parking_id,
        "time_in": new_usage.time_in.isoformat()
    }), 201

@app_routes.route("/client_parkings", methods=["DELETE"])
def leave_parking():
    data = request.get_json()

    if not data or "client_id" not in data or "parking_id" not in data:
        return jsonify({"error": "client_id and parking_id are required"}), 400

    client_id = data["client_id"]
    parking_id = data["parking_id"]

    client_parking = ClientParking.query.filter_by(
        client_id=client_id,
        parking_id=parking_id,
        time_out=None
    ).first()

    if not client_parking:
        return jsonify({"error": "No active parking record found for this client"}), 404

    client_parking.time_out = datetime.utcnow()

    parking = Parking.query.get(parking_id)
    if parking and parking.count_available_places < parking.count_places:
        parking.count_available_places += 1

    db.session.commit()

    return jsonify({
        "message": "Client successfully left the parking",
        "client_id": client_id,
        "parking_id": parking_id,
        "time_out": client_parking.time_out.isoformat()
    }), 200
