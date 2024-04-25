import sys
import asyncio
import logging

from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties

from settings import *
from keyboards.reply import ReplyKb
from FSM.FSM_message_handler import fsm_router

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
dp.include_router(fsm_router)


@dp.message(CommandStart())
async def start(message: Message) -> None:
    if not user.user_exist(user_id=message.chat.id):
        user.add_user(user_id=message.chat.id, first_name=message.chat.first_name, last_name=message.chat.last_name,
                      username=message.chat.username)
        await message.answer(f"Вітаємо в GymHelper", reply_markup=ReplyKb.start_menu)
    else:
        await message.answer(f"Бота перезапущено", reply_markup=ReplyKb.main_menu)


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(BOT_COMMAND)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    print('\nBOT STOPED')
