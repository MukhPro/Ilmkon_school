import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)

CHANNEL = int(os.getenv("CHANNEL_ID"))

dp = Dispatcher()

async def menu_commands():
    command = [
        BotCommand(command='start', description='Botni ishga tushirish')
    ]
    await bot.set_my_commands(commands=command, scope=BotCommandScopeDefault())
