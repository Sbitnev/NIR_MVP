import sqlite3
from datetime import datetime
from config_data.config import sqlite, debug

# Функция для подключения к базе данных
def connect_db(db_name=sqlite):
    conn = sqlite3.connect(db_name)
    return conn

# Функция для определения нахождения пользователя по tg_id
def get_user_id_by_tg_id(tg_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT user_id FROM users WHERE tg_id = ?;', (tg_id,))
        user_id = cursor.fetchone()
        if user_id:
            return user_id[0]
        else:
            if debug:
                print("Пользователь не найден.")
            return None
    except Exception as e:
        print(f"Ошибка при получении user_id: {e}")
    finally:
        cursor.close()
        conn.close()

# Функция для регистрации пользователя
def register_user(username : str, tg_id : int):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, tg_id) VALUES (?, ?);', (username, tg_id))
        conn.commit()
        user_id = cursor.lastrowid
        if debug:
            print(f"Пользователь зарегистрирован с ID: {user_id} и tg_id: {tg_id}")
        return user_id
    except Exception as e:
        print(f"Ошибка при регистрации пользователя: {e}")
    finally:
        cursor.close()
        conn.close()

# Функция для добавления сообщения
def add_message(user_id : int, content : str, is_bot : bool=False) -> None:
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO messages (user_id, content, is_bot) VALUES (?, ?, ?);', (user_id, content, is_bot))
        conn.commit()
        if debug:
            print("Сообщение добавлено.")
    except Exception as e:
        print(f"Ошибка при добавлении сообщения: {e}")
    finally:
        cursor.close()
        conn.close()
