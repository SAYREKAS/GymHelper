from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from database.core import gh
from keyboards.reply import ReplyKb, create_reply_kbs

from FSM.FSM_Dataclasses import DellExerciseState

FSM_dell_exercise = Router()


# реакція на натискання кнопкі '🗑Видалити вправу'______________________________________________________________________
@FSM_dell_exercise.message(StateFilter(None), F.text == '🗑Видалити вправу')
async def func(message: Message, state: FSMContext):
    ex = gh.get_user_exercises(user_id=message.from_user.id)
    if ex:
        await state.set_state(DellExerciseState.muscle_group)
        await message.answer('Виберіть групу мʼязів для видалення вправи',
                             reply_markup=create_reply_kbs(ex, additional_btn=['🚫Відмінити']))
    else:
        await message.answer("Ще не додано жодної вправи", reply_markup=ReplyKb.main_menu)


# вибір групи мʼязів____________________________________________________________________________________________________
@FSM_dell_exercise.message(DellExerciseState.muscle_group, F.text)
async def func(message: Message, state: FSMContext):
    ex = gh.get_user_exercises(user_id=message.from_user.id)

    if message.text in ex:
        await state.update_data(muscle_group=message.text)
        await state.set_state(DellExerciseState.exercise)
        await message.answer('Виберіть назву вправи яку необхідно вдалити',
                             reply_markup=create_reply_kbs(ex[message.text], additional_btn=['🚫Відмінити']))
    else:
        await message.answer(f"Групи мʼязів  '{message.text}' не існує.",
                             reply_markup=create_reply_kbs(ex, additional_btn=['🚫Відмінити']))


# # вибір назви вправи__________________________________________________________________________________________________
@FSM_dell_exercise.message(DellExerciseState.exercise, F.text)
async def func(message: Message, state: FSMContext):
    ex = gh.get_user_exercises(user_id=message.from_user.id)
    data = await state.get_data()

    if message.text in ex[data['muscle_group']]:
        await state.update_data(exercise=message.text)
        data = await state.get_data()
        await state.clear()
        await message.answer(gh.delete_user_exercise(user_id=message.from_user.id,
                                                     muscle_group=data['muscle_group'],
                                                     exercise=data['exercise']),
                             reply_markup=ReplyKb.main_menu)
    else:
        await message.answer('помилка', reply_markup=create_reply_kbs(ex[data['muscle_group']],
                                                                      additional_btn=['🚫Відмінити']))
