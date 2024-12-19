from handlers import user_handlers
from config_data import dp, bot
from database.sqlite import sql_start
import asyncio
from aiogram.methods import DeleteWebhook


async def main():
    try:
        # Подключаемся к БД
        sql_start()

        # Регистриуем роутеры в диспетчере
        dp.include_router(user_handlers.router)

        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        print("Polling was cancelled.")
    except RuntimeError:


if __name__ == '__main__':
    asyncio.run(main())