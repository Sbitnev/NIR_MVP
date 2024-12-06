from handlers import *
from config_data import dp, bot
from database.sqlite import sql_start
import asyncio
from aiogram.methods import DeleteWebhook


async def main():
    try:
        sql_start()
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        print("Polling was cancelled.")

if __name__ == '__main__':
    asyncio.run(main())