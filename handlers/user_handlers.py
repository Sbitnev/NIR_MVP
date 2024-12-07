from aiogram.filters import Command
from aiogram.types import Message
from config_data import dp, bot

import asyncio
from ollama import AsyncClient

async def chat(msg: Message, content: str, chat_id: int) -> None:
    message = {'role': 'user', 'content': content}
    message_text = ''
    count = 0
    async for part in await AsyncClient().chat(model='llama3.1', messages=[message], stream=True):
        message_text += part['message']['content']
        # count += 1
        # if not count % 10:
        #     await bot.edit_message_text(message_text, chat_id=chat_id, message_id=msg.message_id)

    await bot.edit_message_text(message_text, chat_id=chat_id, message_id=msg.message_id)

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    # Проверяем, что message.text не None
    if message.text is not None:
        msg = await bot.send_message(message.chat.id, 'Ожиание ответа модели')
        await chat(msg, message.text, message.chat.id)
    else:
        await message.reply(text="Вы отправили пустое сообщение.")