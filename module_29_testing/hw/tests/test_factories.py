import pytest
from module_29_testing.hw.app import db
from factories import ClientFactory, ParkingFactory


@pytest.mark.usefixtures("client")
def test_create_client():
    client = ClientFactory()
    db.session.commit()

    assert client.id is not None  # Проверяем запись
    assert client.name is not None
    assert client.surname is not None


@pytest.mark.usefixtures("client")
def test_create_parking():
    parking = ParkingFactory()
    db.session.commit()

    assert parking.id is not None  # Проверяем парковку
    assert parking.count_available_places <= parking.count_places