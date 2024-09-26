import requests
import sqlite3
import time
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
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


def fetch_characters_with_process_pool():
    start_time = time.time()

    with Pool() as pool:
        characters = pool.map(get_character_data, range(1, 21))

    characters = [
        {
            'name': char['name'],
            'birth_year': char['birth_year'],
            'gender': char['gender']
        }
        for char in characters if char
    ]

    save_to_db(characters)
    end_time = time.time()
    print(f"Process Pool execution took {end_time - start_time:.2f} seconds")


def fetch_characters_with_thread_pool():
    start_time = time.time()

    with ThreadPoolExecutor() as executor:
        characters = list(executor.map(get_character_data, range(1, 21)))

    characters = [
        {
            'name': char['name'],
            'birth_year': char['birth_year'],
            'gender': char['gender']
        }
        for char in characters if char
    ]

    save_to_db(characters)
    end_time = time.time()
    print(f"Thread Pool execution took {end_time - start_time:.2f} seconds")


def main():
    create_db()

    print("Fetching characters sequentially...")
    fetch_characters_sequential()

    print("\nFetching characters with process pool...")
    fetch_characters_with_process_pool()

    print("\nFetching characters with thread pool...")
    fetch_characters_with_thread_pool()


if __name__ == "__main__":
    main()
