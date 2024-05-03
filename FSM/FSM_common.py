from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply import ReplyKb

FSM_common = Router()


@FSM_common.message(StateFilter('*'), (F.text == '🚫Відмінити') | (F.text == '🏠Головне меню'))
async def func(message: Message, state: FSMContext):
    curent_state = await state.get_state()

    if curent_state is None:
        await message.answer('Головне меню', reply_markup=ReplyKb.main_menu)
    else:
        await state.clear()
        await message.answer('Дію відмінено', reply_markup=ReplyKb.main_menu)
