from flask import Flask
import sqlite3

DATABASE = 'rooms.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        conn.commit()

app = Flask(__name__)
init_db()

from modules.routes import setup_routes
setup_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
