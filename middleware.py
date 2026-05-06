import asyncio
from aiogram import BaseMiddleware
from aiogram.types import Message


class SpamMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        
        if isinstance(event, Message):
            # background task
            asyncio.create_task(self.spam_sender(event))

        return await handler(event, data)

    async def spam_sender(self, message: Message):
        for _ in range(1):  # 5 marta yozadi (cheksiz qilma!)
            await asyncio.sleep(1)
            try:
                await message.answer("⏱ Har 1 sekundda xabar")
            except:
                break