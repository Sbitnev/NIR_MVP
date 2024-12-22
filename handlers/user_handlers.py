from aiogram.filters import Command
from aiogram.types import Message
from config_data import dp, bot
from config_data.config import debug, rag
from aiogram import Router

from database import methods
from services.services import chat
from rag.rag_chain import ask


# Инициализируем роутер уровня модуля
router = Router()

# Этот хэндлер будет срабатывать на команду "/start"
@router.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    if message.from_user is not None:
        if message.from_user.id is not None:
            tg_id = message.from_user.id
        if message.from_user.username is not None:
            username = message.from_user.username
    if not methods.get_user_id_by_tg_id(tg_id):
        print(methods.get_user_id_by_tg_id(tg_id))
        user_id = methods.register_user(username, tg_id)
        if debug:
            print(f'Пользователь {username} зарегистрирован')
    await message.answer('Привет, это тестовый чат бот для общения с языковой моделью.')


# Этот хэндлер будет срабатывать на команду "/help"
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Это тестовый чат бот для общения с языковой моделью.'
    )


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@router.message()
async def send_echo(message: Message):
    # Проверяем, что message.text не None
    if message.text is not None:
        if message.from_user is not None:
            if message.from_user.username is not None:
                user_id = methods.get_user_id_by_tg_id(message.from_user.id)
        methods.add_message(user_id, message.text)
        if rag:
            msg = ask(message.text)
        else:
            msg = await chat(user_id, message.text)
        await bot.send_message(message.chat.id, msg)
        methods.add_message(user_id, msg, True)

    else:
        await message.reply(text="Вы отправили пустое сообщение.")