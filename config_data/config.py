from aiogram import Bot, Dispatcher

from dotenv import load_dotenv
import os


# Загружаем переменные из файла .env
load_dotenv()

# Получаем значения переменных
token = os.getenv('TOKEN')

# Проверяем, установлен ли токен
if token is None:
    raise ValueError("Токен не установлен. Пожалуйста, проверьте файл .env.")

# Создаем объекты бота и диспетчера
bot = Bot(token=token)
dp = Dispatcher()
