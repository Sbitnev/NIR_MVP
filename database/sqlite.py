import sqlite3
from config_data.config import sqlite

# https://github.com/ollama/ollama-python

base = sqlite3.connect(sqlite)
cursor = base.cursor()


def sql_start():
    if base:
        print('База данных подключена!')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tg_id INTEGER UNIQUE NOT NULL,
                    username VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INT REFERENCES users(user_id),
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_bot BOOLEAN DEFAULT FALSE
                   )''')
    base.commit()
    cursor.close()
    base.close
