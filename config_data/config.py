from aiogram import Bot, Dispatcher

from dotenv import load_dotenv
import os


# Загружаем переменные из файла .env
load_dotenv()

# Получаем значения переменных
token = os.getenv('TOKEN')

# Создаем объекты бота и диспетчера
bot = Bot(token=token)
dp = Dispatcher()
