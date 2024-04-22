import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from db import Db
from settings import *

dp = Dispatcher()

db = Db(host=DATABASE_HOST,
        port=DATABASE_PORT,
        user=DATABASE_USER,
        password=DATABASE_PASS,
        database=DATABASE_NAME)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    db.add_user(user_id=message.chat.id,
                first_name=message.chat.first_name,
                last_name=message.chat.last_name,
                username=message.chat.username
                )
    await message.answer(f"Вітаємо в GymHelper")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
