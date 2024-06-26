import sys
import asyncio
import logging

from aiogram import types, F
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties

from FSM.FSM_common import FSM_common
from FSM.FSM_dell_exercise import FSM_dell_exercise
from FSM.FSM_new_exercise import FSM_add_new_exercise
from FSM.FSM_start_training import FSM_start_training
from FSM.FSM_user_details import FSM_user_details

from database.core import gh
from config import TOKEN
from keyboards.reply import ReplyKb

BOT_COMMAND = [
    BotCommand(command='start', description='перезапустити бота'),
]

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
dp.include_router(FSM_common)
FSM_common.include_router(FSM_user_details)
FSM_common.include_router(FSM_add_new_exercise)
FSM_common.include_router(FSM_dell_exercise)
FSM_common.include_router(FSM_start_training)


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()

    if not gh.user_exist(user_id=message.chat.id):
        gh.add_new_user(user_id=message.chat.id, first_name=message.chat.first_name,
                        last_name=message.chat.last_name, username=message.chat.username)
        await message.answer(f"Вітаємо в GymHelper", reply_markup=ReplyKb.start_menu)
    else:
        await message.answer(f"Бота перезапущено", reply_markup=ReplyKb.main_menu)


@dp.message(F.text == 'Налаштування')
async def func(message: Message):
    await message.answer('Налаштування', reply_markup=ReplyKb.settings_menu)


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(BOT_COMMAND)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    print('\nBOT STOPED')
