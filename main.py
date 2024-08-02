import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.handlers import router as user_router
from app.database import models


async def main():
    load_dotenv()

    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_router(user_router)

    await models.db_connection()

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
