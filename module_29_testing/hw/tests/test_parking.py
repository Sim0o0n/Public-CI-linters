from datetime import datetime

import pytest


@pytest.mark.parametrize("endpoint", ["/clients", "/clients/1"])
def test_get_methods(client, endpoint):
    """Проверяем, что все GET-методы возвращают статус 200"""
    response = client.get(endpoint)
    assert response.status_code == 200


def test_create_client(client):
    """Тест создания нового клиента"""
    new_client = {
        "name": "Иван",
        "surname": "Иванов",
        "credit_card": "1234-5678-9012-3456",
        "car_number": "B456CD77"
    }
    response = client.post("/clients", json=new_client)

    assert response.status_code == 201
    data = response.get_json()

    assert "id" in data
    assert data["name"] == new_client["name"]
    assert data["surname"] == new_client["surname"]
    assert data["credit_card"] == new_client["credit_card"]


def test_create_parking(client):
    """Тест создания новой парковки"""
    new_parking = {
        "address": "Центральная улица, 5",
        "opened": True,
        "count_places": 100,
        "count_available_places": 100
    }
    response = client.post("/parkings", json=new_parking)

    assert response.status_code == 201
    data = response.get_json()

    assert "id" in data
    assert data["address"] == new_parking["address"]
    assert data["count_places"] == new_parking["count_places"]
    assert data["count_available_places"] == new_parking["count_available_places"]


import pytest


def test_parking_entry(client):
    """Тест заезда на парковку"""

    client_data = {
        "name": "Иван",
        "surname": "Иванов",
        "credit_card": "1234-5678-9012-3456",
        "car_number": "B456CD77"
    }

    parking_data = {
        "address": "Центральная улица, 5",
        "opened": True,
        "count_places": 10,
        "count_available_places": 10
    }

    client_response = client.post("/clients", json=client_data)
    parking_response = client.post("/parkings", json=parking_data)

    client_id = client_response.get_json()["id"]
    parking_id = parking_response.get_json()["id"]

    entry_data = {
        "client_id": client_id,
        "parking_id": parking_id
    }

    # Проверка успешного заезда
    response = client.post("/client_parkings", json=entry_data)
    assert response.status_code == 201
    assert response.json["message"] == "Client parked successfully"




@pytest.mark.parking
def test_parking_exit(client):
    """Тест выезда с парковки"""
    new_client = {
        "name": "Иван",
        "surname": "Иванов",
        "credit_card": "1234-5678-9012-3456",
        "car_number": "B456CD77"
    }
    client_response = client.post("/clients", json=new_client)
    client_id = client_response.get_json()["id"]

    new_parking = {
        "address": "Центральная улица, 5",
        "opened": True,
        "count_places": 10,
        "count_available_places": 10
    }
    parking_response = client.post("/parkings", json=new_parking)
    parking_id = parking_response.get_json()["id"]

    new_entry = {
        "client_id": client_id,
        "parking_id": parking_id
    }
    client.post("/client_parkings", json=new_entry)

    exit_data = {
        "client_id": client_id,
        "parking_id": parking_id
    }
    response = client.delete("/client_parkings", json=exit_data)

    assert response.status_code == 200
    data = response.get_json()

    assert "message" in data
    assert data["message"] == "Client successfully left the parking"


