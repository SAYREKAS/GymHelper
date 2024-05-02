import pymysql
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from settings import user, exercise, training, db
from keyboards.reply import ReplyKb, create_reply_kbs, repeat_step_1_30, weight_step_1_30
from FSM.FSM_Dataclasses import UserDetailsState, NewExerciseState, StartTraining

fsm_router = Router()


async def update_and_notify(message: Message, state: FSMContext, field: str, value: str, redact_message: int = None):
    await state.update_data({field: value})
    data = await state.get_data()
    if not redact_message:
        await message.answer(f"Група мʼязів - {data.get('muscle_group') if data.get('muscle_group') else '❔'}\n"
                             f"Вправа - {data.get('exercise_name') if data.get('exercise_name') else '❔'}\n"
                             f"Вага - {data.get('weight') if data.get('weight') else '❔'} кг\n"
                             f"Повтори - {data.get('repeats') if data.get('repeats') else '❔'} раз\n")


# Уточнення деталей користувача_________________________________________________________________________________________
@fsm_router.message(StateFilter(None), F.text == 'Вказати параметри тіла')
async def func(message: Message, state: FSMContext):
    await state.set_state(UserDetailsState.weight)
    await message.answer('Введіть вашу вагу кг:', reply_markup=ReplyKeyboardRemove())


@fsm_router.message(UserDetailsState.weight, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer('Введіть ваш вік')
    await state.set_state(UserDetailsState.age)


@fsm_router.message(UserDetailsState.age, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введіть ваш ріст в см.')
    await state.set_state(UserDetailsState.tall)


@fsm_router.message(UserDetailsState.tall, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(tall=message.text)
    await message.answer('Виберіть вашу стать', reply_markup=ReplyKb.gender_btn)
    await state.set_state(UserDetailsState.gender)


@fsm_router.message(UserDetailsState.gender, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    data = await state.get_data()
    await state.clear()
    try:
        user.add_user_details(user_id=message.chat.id,
                              weight=data['weight'],
                              age=data['age'],
                              tall=data['tall'],
                              gender=data['gender'])
    except pymysql.err.DataError:
        await message.answer('🔴Введено не коректні дані.', reply_markup=ReplyKb.main_menu)
    else:
        await message.answer('🟢Все готово!', reply_markup=ReplyKb.main_menu)


# стать вік ріст вага

# Початок тренування____________________________________________________________________________________________________
@fsm_router.message(StateFilter(None), (F.text == 'Почати тренування') | (F.text == 'Додати ще один підхід'))
async def func(message: Message, state: FSMContext):
    ex = exercise.get_user_exercises(user_id=message.chat.id)
    if ex:
        await state.set_state(StartTraining.muscle_group)
        await message.answer('Що сьогодні тренуємо?', reply_markup=create_reply_kbs(ex))
    else:
        await message.answer('🔴Ви ще не додали жодної вправи', reply_markup=ReplyKb.main_menu)
        await state.clear()


@fsm_router.message(StartTraining.muscle_group, F.text)
async def func(message: Message, state: FSMContext):
    await update_and_notify(message, state, 'muscle_group', message.text)
    ex = exercise.get_user_exercises(user_id=message.chat.id)
    await message.answer('Виберіть вправу', reply_markup=create_reply_kbs(ex[message.text]))
    await state.set_state(StartTraining.exercise_name)


@fsm_router.message(StartTraining.exercise_name, F.text)
async def func(message: Message, state: FSMContext):
    await update_and_notify(message, state, 'exercise_name', message.text)
    await message.answer('Вкажіть вагу', reply_markup=create_reply_kbs(weight_step_1_30, 5))
    await state.set_state(StartTraining.weight)


@fsm_router.message(StartTraining.weight, F.text)
async def func(message: Message, state: FSMContext):
    await update_and_notify(message, state, 'weight', message.text)
    await message.answer('Кількість повторів', reply_markup=create_reply_kbs(repeat_step_1_30, 5))
    await state.set_state(StartTraining.repeats)


@fsm_router.message(StartTraining.repeats, F.text)
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


# Додавання тренування__________________________________________________________________________________________________
@fsm_router.message(StateFilter(None), F.text == 'Додати нову вправу')
async def func(message: Message, state: FSMContext):
    await state.set_state(NewExerciseState.muscle_group_name)
    await message.answer('Виберіть групу мʼязів для нової вправи ',
                         reply_markup=create_reply_kbs(db.get_muscle_groups()))


@fsm_router.message(NewExerciseState.muscle_group_name, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(muscle_group_name=message.text)
    await message.answer('Вкажіть назву вправи:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(NewExerciseState.exercise_name)


@fsm_router.message(NewExerciseState.exercise_name, F.text)
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


# Налаштування__________________________________________________________________________________________________________
@fsm_router.message(F.text == 'Налаштування')
async def func(message: Message):
    await message.answer('Налаштування', reply_markup=ReplyKb.settings_menu)


@fsm_router.message(F.text == 'Головне меню')
async def func(message: Message):
    await message.answer('Головна', reply_markup=ReplyKb.main_menu)
