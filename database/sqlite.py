import sqlite3
from datetime import datetime


# https://github.com/ollama/ollama-python

base = sqlite3.connect('database/sqlite.db')
cursor = base.cursor()

def sql_start():
    if base:
        print('База данных подключена!')
    cursor.execute('CREATE TABLE IF NOT EXISTS users (tg_id INTEGER, name TEXT)')
    base.commit()