import logging
import asyncio
from init_bot import bot


from aiogram import Dispatcher
from hendlers import router as hendlers_router


logging.basicConfig(level=logging.INFO)
    

async def main():
    dp = Dispatcher()
    dp.include_router(hendlers_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())    
