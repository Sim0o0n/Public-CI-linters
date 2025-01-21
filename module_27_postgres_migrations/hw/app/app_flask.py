import random
from flask import Flask, jsonify, request
import os
import requests
from sqlalchemy import (create_engine, Column, Integer, String, ARRAY,
                        Boolean, JSON, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Определение моделей
class Coffee(Base):
    __tablename__ = 'coffee'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    origin = Column(String(200))
    intensifier = Column(String(100))
    notes = Column(ARRAY(String))


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    has_sale = Column(Boolean)
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey('coffee.id'))
    coffee = relationship('Coffee', backref='users')


# Создание таблиц
Base.metadata.create_all(engine)


# Генерация данных перед первым запросом
@app.before_first_request
def generate_test_data():
    if not session.query(Coffee).first():
        # Генерация данных кофе
        for _ in range(10):
            response = requests.get("https://random-data-api.com/api/coffee/random_coffee")
            coffee_data = response.json()
            new_coffee = Coffee(
                title=coffee_data['blend_name'],
                origin=coffee_data['origin'],
                intensifier=coffee_data['intensifier'],
                notes=coffee_data['notes']
            )
            session.add(new_coffee)

        # Генерация данных пользователей
        coffee_ids = [c.id for c in session.query(Coffee).all()]
        for _ in range(10):
            response_user = requests.get("https://random-data-api.com/api/users/random_user")
            response_address = requests.get("https://random-data-api.com/api/address/random_address")
            user_data = response_user.json()
            address_data = response_address.json()

            new_user = Users(
                name=user_data['first_name'],
                has_sale=user_data['subscription']['active'],
                address={
                    "country": address_data['country'],
                    "city": address_data['city'],
                    "street": address_data['street_name']
                },
                coffee_id=random.choice(coffee_ids)
            )
            session.add(new_user)
        session.commit()


# ендпоинты
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    new_user = Users(
        name=data.get('name'),
        has_sale=data.get('has_sale'),
        address=data.get('address'),
        coffee_id=data.get('coffee_id')
    )
    session.add(new_user)
    session.commit()
    return jsonify({'id': new_user.id, 'name': new_user.name, 'coffee_id': new_user.coffee_id})


@app.route('/search_coffee', methods=['GET'])
def search_coffee():
    title = request.args.get('title', '')
    coffee = session.query(Coffee).filter(Coffee.title.ilike(f'%{title}%')).all()
    return jsonify([{'id': c.id, 'title': c.title} for c in coffee])


@app.route('/unique_notes', methods=['GET'])
def unique_notes():
    unique_notes_list = session.query(Coffee.notes).all()
    unique_notes = set(note for sublist in unique_notes_list for note in sublist[0])
    return jsonify(list(unique_notes))


@app.route('/users_in_country', methods=['GET'])
def users_in_country():
    country = request.args.get('country', '')
    users = session.query(Users).filter(Users.address['country'].astext == country).all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users])


if __name__ == '__main__':
    app.run(debug=True)




