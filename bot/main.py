import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import BOT_TOKEN, DATABASE_PATH
from bot.database import Database

# Import handlers
from bot.handlers import registration, menu, friends, resources, lots, open_resources, admin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main function to start the bot"""
    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Initialize database
    db = Database(DATABASE_PATH)
    await db.init_db()
    logger.info("Database initialized")

    # Register middleware to pass database to handlers
    @dp.update.middleware()
    async def db_middleware(handler, event, data):
        data['db'] = db
        return await handler(event, data)

    # Include routers
    dp.include_router(registration.router)
    dp.include_router(menu.router)
    dp.include_router(friends.router)
    dp.include_router(resources.router)
    dp.include_router(lots.router)
    dp.include_router(open_resources.router)
    dp.include_router(admin.router)

    logger.info("Bot started")

    try:
        # Start polling
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
