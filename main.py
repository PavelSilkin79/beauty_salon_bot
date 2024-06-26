import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers import other_handlers, user_handlers
from keyboards.main_menu import set_main_menu
from aiogram.fsm.storage.memory import MemoryStorage
#from aiogram.utils import executor



    # Конфигурируем логирование
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s')
    
    # Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def start_bot():
    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Проверяем токен
    if not config.tg_bot.token:
        raise ValueError("Bot token is not defined in the config file!")

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

   
    # Настраиваем главное меню бота
    await set_main_menu(bot)

    # Регистрируем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass


 