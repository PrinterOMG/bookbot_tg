import asyncio

import aioschedule as aioschedule
from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data.config import PARSING_INTERVAL, SUB_PASSING_INTERVAL
from utils.updates_from_server import update
from utils.subscribe_update import sub_update


async def scheduler():
    aioschedule.every(PARSING_INTERVAL).seconds.do(update)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def sub_scheduler():
    aioschedule.every(SUB_PASSING_INTERVAL).hours.do(sub_update)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    asyncio.create_task(scheduler())
    asyncio.create_task(sub_scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
