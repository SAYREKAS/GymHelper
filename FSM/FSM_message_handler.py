from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from settings import user, exercise, training, db
from keyboards.reply import ReplyKb, create_reply_kbs
from FSM.FSM_Dataclasses import UserDetailsState, NewExerciseState, StartTraining

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
    await message.answer('Виберіть вашу стать:', reply_markup=ReplyKb.gender_btn)
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
@fsm_router.message(StateFilter(None), F.text == 'Почати тренування')
async def func(message: Message, state: FSMContext):
    ex = exercise.get_user_exercises(user_id=message.chat.id)
    if ex:
        await state.set_state(StartTraining.muscle_group)
        await message.answer('Що сьогодні тренуємо?', reply_markup=create_reply_kbs(ex))
    else:
        await message.answer('Ви ще не додали жодної вправи', reply_markup=ReplyKb.main_menu)
        await state.clear()


@fsm_router.message(StartTraining.muscle_group, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(muscle_group=message.text)
    ex = exercise.get_user_exercises(user_id=message.chat.id)
    await message.answer('Виберіть вправу', reply_markup=create_reply_kbs(ex[message.text]))
    await state.set_state(StartTraining.exercise_name)


@fsm_router.message(StartTraining.exercise_name, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(exercise_name=message.text)
    await message.answer('Вкажіть вагу', reply_markup=ReplyKeyboardRemove())
    await state.set_state(StartTraining.weight)


@fsm_router.message(StartTraining.weight, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer('Кількість повторів', reply_markup=ReplyKeyboardRemove())
    await state.set_state(StartTraining.repeats)


@fsm_router.message(StartTraining.repeats, F.text)
async def func(message: Message, state: FSMContext):
    await state.update_data(repeats=message.text)
    await message.answer('Підхід записано', reply_markup=ReplyKb.main_menu)
    data = await state.get_data()
    print(data)
    await state.clear()
    training.add_training_record(user_id=message.chat.id, exercise_name=data['exercise_name'], repeats=data['repeats'],
                                 weight=data['weight'])


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
