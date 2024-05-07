from aiogram.fsm.state import StatesGroup, State


class UserDetailsState(StatesGroup):
    weight = State()
    age = State()
    tall = State()
    gender = State()


class NewExerciseState(StatesGroup):
    muscle_group = State()
    exercise = State()


class DellExerciseState(StatesGroup):
    muscle_group = State()
    exercise = State()


class StartTrainingState(StatesGroup):
    muscle_group = State()
    exercise = State()
    repeats = State()
    weight = State()
