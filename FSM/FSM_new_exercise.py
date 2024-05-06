from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from database.core import gh
from FSM.FSM_Dataclasses import NewExerciseState
from keyboards.reply import ReplyKb, create_reply_kbs

FSM_add_new_exercise = Router()


# реакція на натискання кнопккі 'Додати нову вправу' ___________________________________________________________________
@FSM_add_new_exercise.message(StateFilter(None), F.text == 'Додати нову вправу')
async def func(message: Message, state: FSMContext):
    await state.set_state(NewExerciseState.muscle_group_name)
    await message.answer('Виберіть групу мʼязів для нової вправи ',
                         reply_markup=create_reply_kbs(gh.get_muscle_groups(), group=3, additional_btn=['🚫Відмінити']))


# вибір групи мʼязів ___________________________________________________________________________________________________
@FSM_add_new_exercise.message(NewExerciseState.muscle_group_name, F.text)
async def func(message: Message, state: FSMContext):
    if message.text in gh.get_muscle_groups():
        await state.update_data(muscle_group_name=message.text)
        await message.answer('Вкажіть назву вправи:', reply_markup=ReplyKb.cancel_btn)
        await state.set_state(NewExerciseState.exercise_name)
    else:
        await message.answer('Виберіть праильний варіант',
                             reply_markup=create_reply_kbs(gh.get_muscle_groups(), group=3,
                                                           additional_btn=['🚫Відмінити']))


# вибір назви вправи ___________________________________________________________________________________________________
@FSM_add_new_exercise.message(NewExerciseState.exercise_name, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(exercise_name=message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer(gh.add_user_exercise(user_id=message.chat.id, muscle_group_name=data['muscle_group_name'],
                                              exercise_name=data['exercise_name']), reply_markup=ReplyKb.main_menu)
