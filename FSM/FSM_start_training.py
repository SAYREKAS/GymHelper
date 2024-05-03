import pymysql
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from db import exercise, training
from FSM.FSM_Dataclasses import StartTraining
from keyboards.reply import ReplyKb, create_reply_kbs, repeat_step_1_30, weight_step_1_30

FSM_start_training = Router()


async def update_and_notify(message: Message, state: FSMContext, field: str, value: str, redact_message: int = None):
    await state.update_data({field: value})
    data = await state.get_data()
    if not redact_message:
        await message.answer(f"Група мʼязів - {data.get('muscle_group') if data.get('muscle_group') else '❔'}\n"
                             f"Вправа - {data.get('exercise_name') if data.get('exercise_name') else '❔'}\n"
                             f"Вага - {data.get('weight') if data.get('weight') else '❔'} кг\n"
                             f"Повтори - {data.get('repeats') if data.get('repeats') else '❔'} раз\n")


# Початок тренування____________________________________________________________________________________________________
@FSM_start_training.message(StateFilter(None), (F.text == 'Почати тренування') | (F.text == 'Додати ще один підхід'))
async def func(message: Message, state: FSMContext):
    ex = exercise.get_user_exercises(user_id=message.chat.id)
    if ex:
        await state.set_state(StartTraining.muscle_group)
        await message.answer('Що сьогодні тренуємо?', reply_markup=create_reply_kbs(ex))
    else:
        await message.answer('🔴Ви ще не додали жодної вправи', reply_markup=ReplyKb.main_menu)
        await state.clear()


@FSM_start_training.message(StartTraining.muscle_group, F.text)
async def func(message: Message, state: FSMContext):
    await update_and_notify(message, state, 'muscle_group', message.text)
    ex = exercise.get_user_exercises(user_id=message.chat.id)
    await message.answer('Виберіть вправу', reply_markup=create_reply_kbs(ex[message.text]))
    await state.set_state(StartTraining.exercise_name)


@FSM_start_training.message(StartTraining.exercise_name, F.text)
async def func(message: Message, state: FSMContext):
    await update_and_notify(message, state, 'exercise_name', message.text)
    await message.answer('Вкажіть вагу', reply_markup=create_reply_kbs(weight_step_1_30, 5))
    await state.set_state(StartTraining.weight)


@FSM_start_training.message(StartTraining.weight, F.text)
async def func(message: Message, state: FSMContext):
    await update_and_notify(message, state, 'weight', message.text)
    await message.answer('Кількість повторів', reply_markup=create_reply_kbs(repeat_step_1_30, 5))
    await state.set_state(StartTraining.repeats)


@FSM_start_training.message(StartTraining.repeats, F.text)
async def func(message: Message, state: FSMContext):
    await update_and_notify(message, state, 'repeats', message.text)
    data = await state.get_data()
    await state.clear()
    try:
        training.add_training_record(user_id=message.chat.id, exercise_name=data['exercise_name'],
                                     repeats=data['repeats'], weight=data['weight'])
    except pymysql.err.DataError:
        await message.answer('🔴введені дані не вірні\nвикористовуйте тільки цифри️️',
                             reply_markup=ReplyKb.another_training)
    else:
        await message.answer('🟢Підхід записано', reply_markup=ReplyKb.another_training)
