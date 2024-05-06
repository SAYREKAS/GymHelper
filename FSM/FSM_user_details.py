from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from database.core import gh
from keyboards.reply import ReplyKb
from FSM.common_functions import is_number

from FSM.FSM_Dataclasses import UserDetailsState

FSM_user_details = Router()


# Реакція на натискання клавіші 'Вказати параметри тіла'________________________________________________________________
@FSM_user_details.message(StateFilter(None), F.text == 'Вказати параметри тіла')
async def func(message: Message, state: FSMContext):
    await state.set_state(UserDetailsState.weight)
    await message.answer('Введіть вашу вагу кг:', reply_markup=ReplyKeyboardRemove())


# меню введення ваги користувача________________________________________________________________________________________
@FSM_user_details.message(UserDetailsState.weight, F.text)
async def func(message: Message, state: FSMContext):
    if is_number(message.text):
        await state.update_data(weight=message.text)
        await state.set_state(UserDetailsState.age)
        await message.answer('Введіть ваш вік')
    else:
        await message.answer('Використовуйте тільки цифри')


# меню введення віку користувача________________________________________________________________________________________
@FSM_user_details.message(UserDetailsState.age, F.text)
async def func(message: Message, state: FSMContext):
    if is_number(message.text):
        await state.update_data(age=message.text)
        await state.set_state(UserDetailsState.tall)
        await message.answer('Введіть ваш ріст в см.')
    else:
        await message.answer('Використовуйте тільки цифри')


# меню введення росту користувача_______________________________________________________________________________________
@FSM_user_details.message(UserDetailsState.tall, F.text)
async def func(message: Message, state: FSMContext):
    if is_number(message.text):
        await state.update_data(tall=message.text)
        await state.set_state(UserDetailsState.gender)
        await message.answer('Виберіть вашу стать', reply_markup=ReplyKb.gender_btn)
    else:
        await message.answer('Використовуйте тільки цифри')


# меню введення статі користувача_______________________________________________________________________________________
@FSM_user_details.message(UserDetailsState.gender, F.text)
async def func(message: Message, state: FSMContext):
    if message.text in ['👨‍💼Чоловік', '👩‍💼Жінка']:
        await state.update_data(gender=message.text)
        data = await state.get_data()
        await state.clear()
        await message.answer(gh.add_user_details(user_id=message.chat.id, weight=data['weight'], age=data['age'],
                                                 tall=data['tall'], gender=data['gender']),
                             reply_markup=ReplyKb.main_menu)
