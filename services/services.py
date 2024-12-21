import re
import asyncio

from ollama import AsyncClient
from aiogram.types import Message
from config_data import dp, bot
from database.methods import get_messages_by_user_id

def escape_markdown(text):
    # Заменяем ** на *
    text = text.replace('**', '*')

    # Экранируем специальные символы, которые еще не экранированы
    def replace(match):
        return '\\' + match.group(0)

    # Экранируем только те символы, которые не были экранированы
    return re.sub(r'(?<!\\)([_*[\]()~`>#+\-=|{}.!])', replace, text)

async def chat(user_id: int, content: str) -> str:
    messages = get_messages_by_user_id(user_id)
    messages.append({'role': 'user', 'content': content})
    response = await AsyncClient().chat(model='llama3.1', messages=messages)
    return str(response['message']['content'])

# class Chat:
#     chats : dict = {}

#     def __new__(cls, user_id : int, *args, **kwargs):
#         if user_id in cls.chats:
#             return cls.chats[user_id]
#         else:
#             return super().__new__(cls)

#     def __init__(self, user_id : int):
#         self.user_is = user_id
#         self.messages : list = []
#         Chat.chats[user_id] = self

#     async def chat(self, user_id: int, content: str) -> str:
#         message = {'role': 'user', 'content': content}
#         self.messages.append(message)
#         response = await AsyncClient().chat(model='llama3.1', messages=self.messages)
#         self.messages.append({'role': 'assistant', 'content': str(response['message']['content'])})
#         return str(response['message']['content'])
