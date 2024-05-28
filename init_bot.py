from config import settings
from aiogram import Bot

bot = Bot(token=settings.TG_TOKEN.get_secret_value())