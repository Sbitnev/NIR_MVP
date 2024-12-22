import re
import asyncio

from ollama import AsyncClient
from aiogram.types import Message
from config_data import dp, bot
from database.methods import get_messages_by_user_id


async def chat(user_id: int, content: str) -> str:
    messages = get_messages_by_user_id(user_id)
    messages.append({'role': 'user', 'content': content})
    response = await AsyncClient().chat(model='llama3.1', messages=messages)
    return str(response['message']['content'])
