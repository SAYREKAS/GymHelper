from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.inline import InlineKb
from keyboards.reply import ReplyKb
from FSM.FSM_Dataclasses import UserDetailsState, NewExerciseState, StartTraining
from settings import user, db

fsm_router = Router()


# Уточнення деталей користувача_________________________________________________________________________________________
@fsm_router.message(StateFilter(None), F.text == 'Вказати параметри тіла')
async def func(message: Message, state: FSMContext):
    await state.set_state(UserDetailsState.weight)
    await message.answer('Введіть вашу вагу кг:', reply_markup=ReplyKeyboardRemove())


@fsm_router.message(UserDetailsState.weight, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer('Введіть ваш вік:')
    await state.set_state(UserDetailsState.age)


@fsm_router.message(UserDetailsState.age, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введіть ваш ріст см:')
    await state.set_state(UserDetailsState.tall)


@fsm_router.message(UserDetailsState.tall, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(tall=message.text)
    await message.answer('Виберіть вашу стать:')
    await state.set_state(UserDetailsState.gender)


@fsm_router.message(UserDetailsState.gender, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer('Все готово!', reply_markup=ReplyKb.main_menu)
    data = await state.get_data()
    await state.clear()
    user.add_user_details(user_id=message.chat.id,
                          weight=data['weight'],
                          age=data['age'],
                          tall=data['tall'],
                          gender=data['gender'])


# стать вік ріст вага

# Початок тренування____________________________________________________________________________________________________
# @fsm_router.message(StateFilter(None), F.text == 'Почати тренування')
# async def func(message: Message, state: FSMContext):
#     # await state.set_state(StartTraining.)
#     await message.answer('Що сьогодні тренуємо?', reply_markup=ReplyKb.muscle_group)


# Додавання тренування__________________________________________________________________________________________________
@fsm_router.message(StateFilter(None), F.text == 'Додати нове тренування')
async def func(message: Message, state: FSMContext):
    await state.set_state(NewExerciseState.muscle_group_name)
    await message.answer('Виберіть групу мʼязів для нової вправи ', reply_markup=ReplyKb.muscle_group)


@fsm_router.message(NewExerciseState.muscle_group_name, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(muscle_group_name=message.text)
    await message.answer('Вкажіть назву вправи:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(NewExerciseState.exercise_name)


@fsm_router.message(NewExerciseState.exercise_name, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(exercise_name=message.text)
    await message.answer('Готово!:', reply_markup=ReplyKb.main_menu)
    data = await state.get_data()
    await state.clear()
    user.add_user_exercise(user_id=message.chat.id,
                           muscle_group_name=data['muscle_group_name'],
                           exercise_name=data['exercise_name'])
