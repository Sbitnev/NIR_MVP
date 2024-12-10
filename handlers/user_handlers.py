from aiogram.filters import Command
from aiogram.types import Message
from config_data import dp, bot
from config_data.config import debug
from aiogram import Router

from database import methods

import asyncio
from ollama import AsyncClient

import re

# Инициализируем роутер уровня модуля
router = Router()

def escape_markdown(text):
    # Заменяем ** на *
    text = text.replace('**', '*')

    # Экранируем специальные символы, которые еще не экранированы
    def replace(match):
        return '\\' + match.group(0)

    # Экранируем только те символы, которые не были экранированы
    return re.sub(r'(?<!\\)([_*[\]()~`>#+\-=|{}.!])', replace, text)

async def chat(msg: Message, content: str, chat_id: int) -> str:
    message = {'role': 'user', 'content': content}
    message_text = ''
    count = 0
    async for part in await AsyncClient().chat(model='llama3.1', messages=[message], stream=True):
        message_text += part['message']['content']
        message_text = escape_markdown(message_text)
        count += 1
        if not count % 10:
            await bot.edit_message_text(message_text, chat_id=chat_id, message_id=msg.message_id)

    await bot.edit_message_text(message_text, chat_id=chat_id, message_id=msg.message_id)
    return message_text

# Этот хэндлер будет срабатывать на команду "/start"
@router.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    tg_id = message.from_user.id
    username = message.from_user.username
    if not methods.get_user_id_by_tg_id(tg_id):
        print(methods.get_user_id_by_tg_id(tg_id))
        methods.register_user(username, tg_id)
        if debug:
            print(f'Пользователь {username} зарегистрирован')
    await message.answer('*Привет\!*')


# Этот хэндлер будет срабатывать на команду "/help"
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне'
    )


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@router.message()
async def send_echo(message: Message):
    # Проверяем, что message.text не None
    if message.text is not None:
        user_id = methods.get_user_id_by_tg_id(message.from_user.id)
        methods.add_message(user_id, message.text)
        msg = await bot.send_message(message.chat.id, 'Ожиание ответа модели', parse_mode='MarkdownV2')
        methods.add_message(user_id, await chat(msg, message.text, message.chat.id), True)
    else:
        await message.reply(text="Вы отправили пустое сообщение.")