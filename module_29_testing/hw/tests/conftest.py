import pytest
from module_29_testing.hw.model import create_app, db, Client, Parking, ClientParking
from datetime import datetime



@pytest.fixture
def app():
    """Создание тестового приложения Flask"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Используем временную БД
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()

        test_client = Client(name="John", surname="Doe", credit_card="1234-5678-9012-3456", car_number="A123BC77")
        test_parking = Parking(address="Test Street 1", opened=True, count_places=10, count_available_places=5)
        db.session.add_all([test_client, test_parking])
        db.session.commit()

        parking_log = ClientParking(client_id=test_client.id, parking_id=test_parking.id, time_in=datetime.utcnow(),
                                    time_out=None)
        db.session.add(parking_log)
        db.session.commit()

        yield app

        with app.app_context():
            db.drop_all()

def client(app):
    """Создание тестового клиента для отправки HTTP-запросов"""
    return app.test_client()


@pytest.fixture
def db_session(app):
    """Фикстура для работы с БД внутри тестов"""
    with app.app_context():
        yield db
        db.session.rollback()