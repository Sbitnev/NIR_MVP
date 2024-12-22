from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import load_dotenv
import os


# Загружаем переменные из файла .env
load_dotenv()

# Получаем значения переменных
token = os.getenv('TOKEN')
sqlite = str(os.getenv('SQLITE'))
debug = os.getenv('DEBUG') == 'True'
rag = os.getenv('RAG') == 'True'
hf_token = str(os.getenv('HF_TOKEN'))

# Проверяем, установлен ли токен
if token is None:
    raise ValueError("Токен не установлен. Пожалуйста, проверьте файл .env.")

# Создаем объекты бота и диспетчера
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Создаем словарь для объектов чатов
chats : dict = {}
