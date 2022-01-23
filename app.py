import asyncio

import aioschedule as aioschedule
from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data.config import PARSING_INTERVAL
from utils.updates_from_server import update
print("imports done")


async def scheduler():
    aioschedule.every(PARSING_INTERVAL).seconds.do(update)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    print("# Устанавливаем дефолтные команды")

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    print("# Уведомляет про запуск")

    asyncio.create_task(scheduler())
    print("scheduler")


if __name__ == '__main__':
    print("executor")
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)


