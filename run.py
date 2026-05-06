import asyncio
import logging

from handlers import hand_router
from config import dp, bot, menu_commands
from middleware import SpamMiddleware


dp.include_router(hand_router)
dp.message.middleware(SpamMiddleware())

async def main():
    await menu_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())