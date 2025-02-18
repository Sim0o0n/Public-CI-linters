import factory
from faker import Faker
from module_29_testing.hw.routes import db
from module_29_testing.hw.model import Client, Parking

fake = Faker()

class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")  # Убедись, что поле называется правильно
    credit_card = factory.Faker("credit_card_number")
    car_number = factory.Faker('bothify', text='??-####-??')


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker('address')
    opened = factory.Faker('boolean')
    count_places = factory.Faker('random_int', min=10, max=100)
    count_available_places = factory.LazyAttribute(lambda obj: obj.count_places - fake.random_int(min=0, max=5))

