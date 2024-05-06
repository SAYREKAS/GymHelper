from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from database.core import gh
from FSM.FSM_Dataclasses import DellExerciseState
from keyboards.reply import ReplyKb, create_reply_kbs

FSM_dell_exercise = Router()


@FSM_dell_exercise.message(StateFilter(None), F.text == '🗑Видалити вправу')
async def func(message: Message, state: FSMContext):
    await state.set_state(DellExerciseState.muscle_group_name)
    ex = gh.get_user_exercises(user_id=message.chat.id)
    if ex:
        await message.answer('Виберіть групу мʼязів для видалення вправи',
                             reply_markup=create_reply_kbs(ex, additional_btn=['🚫Відмінити']))
    else:
        await message.answer("Ще не додано жодної вправи", reply_markup=ReplyKb.main_menu)
        await state.clear()


@FSM_dell_exercise.message(DellExerciseState.muscle_group_name, F.text)
async def func(message: Message, state: FSMContext):
    if message.text not in gh.get_muscle_groups():
        await message.answer(f"Групи мʼязів  '{message.text}' не існує.", reply_markup=ReplyKb.main_menu)
        await state.clear()
    else:
        await state.update_data(muscle_group_name=message.text)
        ex = gh.get_user_exercises(user_id=message.chat.id)
        await message.answer('Виберіть назву вправи яку необхідно вдалити',
                             reply_markup=create_reply_kbs(ex[message.text], additional_btn=['🚫Відмінити']))
        await state.set_state(DellExerciseState.exercise_name)


@FSM_dell_exercise.message(DellExerciseState.exercise_name, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(exercise_name=message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer(gh.delete_user_exercise(user_id=message.chat.id, muscle_group_name=data['muscle_group_name'],
                                                 exercise_name=data['exercise_name']), reply_markup=ReplyKb.main_menu)
