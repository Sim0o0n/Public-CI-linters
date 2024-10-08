import sqlite3

db = 'rooms.db'

def add_room(name):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO rooms (name) VALUES (?)', (name,))
        conn.commit()
        return cursor.lastrowid

def get_rooms():
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rooms')
        return cursor.fetchall()

def update_room(id, name):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE rooms SET name = ? WHERE id = ?', (name, id))
        conn.commit()
        return cursor.rowcount > 0

def delete_room(id):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM rooms WHERE id = ?', (id,))
        conn.commit()
        return cursor.rowcount > 0
