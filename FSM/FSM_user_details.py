import pymysql

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from db import user
from keyboards.reply import ReplyKb
from FSM.FSM_Dataclasses import UserDetailsState

FSM_user_details = Router()


@FSM_user_details.message(StateFilter(None), F.text == 'Вказати параметри тіла')
async def func(message: Message, state: FSMContext):
    await state.set_state(UserDetailsState.weight)
    await message.answer('Введіть вашу вагу кг:', reply_markup=ReplyKeyboardRemove())


@FSM_user_details.message(UserDetailsState.weight, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer('Введіть ваш вік')
    await state.set_state(UserDetailsState.age)


@FSM_user_details.message(UserDetailsState.age, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введіть ваш ріст в см.')
    await state.set_state(UserDetailsState.tall)


@FSM_user_details.message(UserDetailsState.tall, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(tall=message.text)
    await message.answer('Виберіть вашу стать', reply_markup=ReplyKb.gender_btn)
    await state.set_state(UserDetailsState.gender)


@FSM_user_details.message(UserDetailsState.gender, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    data = await state.get_data()
    await state.clear()
    try:
        user.add_user_details(user_id=message.chat.id, weight=data['weight'], age=data['age'], tall=data['tall'],
                              gender=data['gender'])
    except pymysql.err.DataError:
        await message.answer('🔴Введено не коректні дані.', reply_markup=ReplyKb.main_menu)
    else:
        await message.answer('🟢Все готово!', reply_markup=ReplyKb.main_menu)
