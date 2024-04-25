from aiogram.fsm.state import StatesGroup, State


class UserDetailsState(StatesGroup):
    weight = State()
    age = State()
    tall = State()
    gender = State()


class NewExerciseState(StatesGroup):
    muscle_group_name = State()
    exercise_name = State()


class StartTraining(StatesGroup):
    id_user_exercise = State()
    user_id = State()
    repeats = State()
    weight = State()
