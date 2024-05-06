from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from database.core import gh
from FSM.FSM_Dataclasses import StartTrainingState
from keyboards.reply import ReplyKb, create_reply_kbs

FSM_start_training = Router()


async def update_and_notify(message: Message, state: FSMContext, field: str, value: str, redact_message: int = None):
    await state.update_data({field: value})
    data = await state.get_data()
    if not redact_message:
        await message.answer(f"Група мʼязів - {data.get('muscle_group') if data.get('muscle_group') else '❔'}\n"
                             f"Вправа - {data.get('exercise_name') if data.get('exercise_name') else '❔'}\n"
                             f"Вага - {data.get('weight') if data.get('weight') else '❔'} кг\n"
                             f"Повтори - {data.get('repeats') if data.get('repeats') else '❔'} раз\n")


def is_number(stroke: str) -> bool:
    try:
        float(stroke.replace(',', '.'))
        return True
    except ValueError:
        return False


# Реакція на натискання кнопкі ʼПочати тренуванняʼ______________________________________________________________________
@FSM_start_training.message(StateFilter(None), (F.text == 'Почати тренування') | (F.text == 'Додати ще один підхід'))
async def func(message: Message, state: FSMContext):
    ex = gh.get_user_exercises(user_id=message.chat.id)

    if ex:
        await state.set_state(StartTrainingState.muscle_group)
        await message.answer('Що сьогодні тренуємо?', reply_markup=create_reply_kbs(ex, additional_btn=['🚫Відмінити']))
    else:
        await message.answer('🔴Ви ще не додали жодної вправи', reply_markup=ReplyKb.main_menu)
        await state.clear()


# меню вибору групи мʼязів______________________________________________________________________________________________
@FSM_start_training.message(StartTrainingState.muscle_group, F.text)
async def func(message: Message, state: FSMContext):
    ex = gh.get_user_exercises(user_id=message.chat.id)

    if message.text in ex:
        await update_and_notify(message, state, 'muscle_group', message.text)
        await message.answer('Виберіть вправу',
                             reply_markup=create_reply_kbs(ex[message.text], additional_btn=['🚫Відмінити']))
        await state.set_state(StartTrainingState.exercise_name)
    else:
        await message.answer('неправильно вибрана вправа',
                             reply_markup=create_reply_kbs(ex, additional_btn=['🚫Відмінити']))


# меню вибору вправи з конкретної групи мʼязів__________________________________________________________________________
@FSM_start_training.message(StartTrainingState.exercise_name, F.text)
async def func(message: Message, state: FSMContext):
    ex = gh.get_user_exercises(user_id=message.chat.id)
    data = await state.get_data()

    if message.text in ex[data['muscle_group']]:
        await update_and_notify(message, state, 'exercise_name', message.text)
        await message.answer('Вкажіть вагу', reply_markup=ReplyKb.cancel_btn)
        await state.set_state(StartTrainingState.weight)
    else:
        await message.answer('неправильно вибрана вправа',
                             reply_markup=create_reply_kbs(ex[data['muscle_group']], additional_btn=['🚫Відмінити']))


# меню вибору ваги з якою працювали_____________________________________________________________________________________
@FSM_start_training.message(StartTrainingState.weight, F.text)
async def func(message: Message, state: FSMContext):
    if is_number(message.text):
        await update_and_notify(message, state, 'weight', message.text.replace(',', '.'))
        await message.answer('Кількість повторів', reply_markup=ReplyKb.cancel_btn)
        await state.set_state(StartTrainingState.repeats)
    else:
        await message.answer('Тільки цілі або дробові числа', reply_markup=ReplyKb.cancel_btn)


# запис інформації в базу данних________________________________________________________________________________________
@FSM_start_training.message(StartTrainingState.repeats, F.text)
async def func(message: Message, state: FSMContext):
    if is_number(message.text):
        await update_and_notify(message, state, 'repeats', message.text.replace(',', '.'))
        data = await state.get_data()
        await state.clear()
        await message.answer(gh.add_training_record(user_id=message.chat.id, exercise_name=data['exercise_name'],
                                                    repeats=data['repeats'], weight=data['weight']),
                             reply_markup=ReplyKb.main_menu)
    else:
        await message.answer('Тільки цілі або дробові числа', reply_markup=ReplyKb.cancel_btn)
