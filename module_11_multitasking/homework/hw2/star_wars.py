import requests
import sqlite3
import time
from typing import List


def create_db():
    conn = sqlite3.connect('starwars.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY,
            name TEXT,
            birth_year TEXT,
            gender TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_to_db(characters: List[dict]):
    conn = sqlite3.connect('starwars.db')
    cursor = conn.cursor()

    for char in characters:
        cursor.execute('''
            INSERT INTO characters (name, birth_year, gender) 
            VALUES (?, ?, ?)
        ''', (char['name'], char['birth_year'], char['gender']))

    conn.commit()
    conn.close()


def get_character_data(character_id: int) -> dict:
    url = f'https://swapi.dev/api/people/{character_id}/'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def fetch_characters_sequential():
    characters = []
    start_time = time.time()

    for i in range(1, 21):
        character = get_character_data(i)
        if character:
            characters.append({
                'name': character['name'],
                'birth_year': character['birth_year'],
                'gender': character['gender']
            })

    save_to_db(characters)

    end_time = time.time()
    print(f"Sequential execution took {end_time - start_time:.2f} seconds")


def main():
    create_db()

    print("Fetching characters sequentially...")
    fetch_characters_sequential()


if __name__ == "__main__":
    main()
