from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from db import db, exercise
from FSM.FSM_Dataclasses import NewExerciseState
from keyboards.reply import ReplyKb, create_reply_kbs

FSM_add_new_exercise = Router()


@FSM_add_new_exercise.message(StateFilter(None), F.text == 'Додати нову вправу')
async def func(message: Message, state: FSMContext):
    await state.set_state(NewExerciseState.muscle_group_name)
    await message.answer('Виберіть групу мʼязів для нової вправи ',
                         reply_markup=create_reply_kbs(db.get_muscle_groups(), group=3, additional_btn=['🚫Відмінити']))


@FSM_add_new_exercise.message(NewExerciseState.muscle_group_name, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(muscle_group_name=message.text)
    await message.answer('Вкажіть назву вправи:', reply_markup=ReplyKb.cancel_btn)
    await state.set_state(NewExerciseState.exercise_name)


@FSM_add_new_exercise.message(NewExerciseState.exercise_name, F.text)
async def func(message: Message, state: FSMContext):
    if not exercise.exercise_exists(exercise_name=message.text):
        await state.update_data(exercise_name=message.text)
        data = await state.get_data()
        await message.answer(f"Вправу {data['exercise_name']} успішно додано!", reply_markup=ReplyKb.main_menu)
        await state.clear()
        exercise.add_user_exercise(user_id=message.chat.id, muscle_group_name=data['muscle_group_name'],
                                   exercise_name=data['exercise_name'])

    else:
        await state.update_data(exercise_name=message.text)
        await message.answer('Така вправа вже існує!', reply_markup=ReplyKb.main_menu)
        await state.clear()
