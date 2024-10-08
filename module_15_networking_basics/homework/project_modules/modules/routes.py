from flask import request, jsonify
from .models import add_room, get_rooms, update_room, delete_room


def setup_routes(app):
    @app.route('/rooms', methods=['POST'])
    def add_room_route():
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({"error": "Room name is required"}), 400

        room_id = add_room(data['name'])
        return jsonify({"message": "Room added successfully", "room_id": room_id}), 201

    @app.route('/rooms', methods=['GET'])
    def get_rooms_route():
        rooms = get_rooms()
        room_list = [{"id": room[0], "name": room[1], "links": {
            "self": f"/rooms/{room[0]}",
            "update": f"/rooms/{room[0]}",
            "delete": f"/rooms/{room[0]}"
        }} for room in rooms]
        return jsonify(room_list), 200

    @app.route('/rooms/<int:id>', methods=['PUT'])
    def update_room_route(id):
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({"error": "Room name is required"}), 400

        updated = update_room(id, data['name'])
        if not updated:
            return jsonify({"error": "Room not found"}), 404
        return jsonify({"message": "Room updated successfully"}), 200

    @app.route('/rooms/<int:id>', methods=['DELETE'])
    def delete_room_route(id):
        deleted = delete_room(id)
        if not deleted:
            return jsonify({"error": "Room not found"}), 404
        return jsonify({"message": "Room deleted successfully"}), 204

