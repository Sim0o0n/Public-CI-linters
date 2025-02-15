import pytest

@pytest.mark.parametrize("endpoint", ["/clients", "/parkings", "/logs"])
def test_get_methods(client, endpoint):
    """Проверяем, что все GET-методы возвращают статус 200"""
    response = client.get(endpoint)
    assert response.status_code == 200


def test_create_client(client):
    """Тест создания нового клиента"""
    new_client = {"name": "Иван Иванов", "card_attached": True}
    response = client.post("/clients", json=new_client)

    assert response.status_code == 201
    data = response.get_json()

    assert "id" in data
    assert data["name"] == new_client["name"]
    assert data["card_attached"] is True


def test_create_parking(client):
    """Тест создания новой парковки"""
    new_parking = {"name": "Центральная", "count_places": 100}
    response = client.post("/parkings", json=new_parking)

    assert response.status_code == 201
    data = response.get_json()

    assert "id" in data
    assert data["name"] == new_parking["name"]
    assert data["count_places"] == new_parking["count_places"]
    assert data["count_available_places"] == new_parking["count_places"]


@pytest.mark.parking
def test_parking_entry(client, db):
    """Тест заезда клиента на парковку"""
    parking_id = 1
    client_id = 1

    response = client.post(f"/parkings/{parking_id}/enter", json={"client_id": client_id})
    assert response.status_code == 200

    data = response.get_json()
    assert data["count_available_places"] < data["count_places"]
    assert data["is_open"] is True


@pytest.mark.parking
def test_parking_exit(client, db):
    """Тест выезда клиента с парковки"""
    parking_id = 1
    client_id = 1

    response = client.post(f"/parkings/{parking_id}/exit", json={"client_id": client_id})
    assert response.status_code == 200

    data = response.get_json()
    assert data["count_available_places"] > 0
    assert data["exit_time"] >= data["entry_time"]
