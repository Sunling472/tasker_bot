import asyncio
import sys
import logging

from aiogram import types
from aiogram.types import BotCommand


from Tasker_bot.app.config_reader import load_config
from Tasker_bot.app.handlers.common import register_handlers_common
# from app.handlers.common import common_handlers
from Tasker_bot.config.export_vars import dp, bot
from Tasker_bot.app.handlers.new_task import register_handlers_new_task
from Tasker_bot.app.handlers.list_tasks import register_handlers_list_task
from Tasker_bot.app.handlers.delete_task import register_handler_delete_task
# from Tasker_bot.app.handlers.edit_tasks import register_handler_edit_task



logger = logging.getLogger(__name__)


# Регистрация команд
async def set_commands(bot):

    commands: list[BotCommand] = [
        BotCommand(command='new', description='New Task'),
        BotCommand(command='list', description='List Tasks'),
        BotCommand(command='edit', description='Edit Task'),
        BotCommand(command='del', description='Delete Task'),
        BotCommand(command='reg', description='Registration'),
        BotCommand(command='cancel', description='Cancel')
    ]
    await bot.set_my_commands(commands)


async def main(dp, bot):
    # Настройка логгирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )
    logger.info('Starting bot')

    # Настройка файла конфигурации


    # Инициализация объекта бота и диспетчера


    # Регистрация хендлеров...
    register_handlers_common(dp)
    register_handlers_new_task(dp)
    register_handlers_list_task(dp)
    # register_handler_delete_task(dp)
    # register_handler_edit_task(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()

if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == '__main__':
    asyncio.run(main(dp, bot))
