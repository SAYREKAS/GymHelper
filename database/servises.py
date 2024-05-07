from datetime import datetime
from database.models import User, MuscleGroups, Exercise, Training


class GymHelper:
    def __init__(self, session_scope):
        self.session_scope = session_scope

    def add_new_user(self, user_id: int, first_name: str = None, last_name: str = None, username: str = None) -> None:
        with self.session_scope() as session:
            try:
                new_user = User(user_id=user_id, first_name=first_name, last_name=last_name, username=username)
                session.add(new_user)
                session.commit()
            except Exception as ex:
                print(f"add_new_user ERROR - {ex}")

    def add_user_details(self, user_id: int, weight: int, age: int, tall: int, gender: str) -> str:
        with self.session_scope() as session:
            try:
                user = session.query(User).filter_by(user_id=user_id).first()
                if user is not None:
                    user.weight = weight
                    user.age = age
                    user.tall = tall
                    user.gender = gender
                    session.commit()
                    return "Дані успішно оновлено"
                return "Сталася помилка"
            except Exception as ex:
                print(f"add_user_details ERROR - {ex}")

    def user_exist(self, user_id: int = None) -> bool:
        with self.session_scope() as session:
            try:
                return True if user_id in [info.user_id for info in session.query(User).all()] else False
            except Exception as ex:
                print(f"user_exist ERROR - {ex}")

    def add_muscle_groups(self, name_list: list[str]) -> None:
        with self.session_scope() as session:
            try:
                for name in name_list:
                    session.add(MuscleGroups(group_name=name))
                session.commit()
            except Exception as ex:
                print(f"add_muscle_groups ERROR - {ex}")

    def get_muscle_groups(self) -> list[str]:
        with self.session_scope() as session:
            try:
                return [name.group_name for name in session.query(MuscleGroups).all()]
            except Exception as ex:
                print(f"get_muscle_groups ERROR - {ex}")
                return []

    def add_user_exercise(self, user_id: int, muscle_group: str, exercise: str) -> str:
        with self.session_scope() as session:
            try:
                ex_exist = session.query(Exercise).filter_by(user_id=user_id, muscle_group_name=muscle_group,
                                                             exercise_name=exercise).first()
                if ex_exist is None:
                    new_exercise = Exercise(user_id=user_id, muscle_group_name=muscle_group, exercise_name=exercise)
                    session.add(new_exercise)
                    session.commit()
                    return f"Вправу '{exercise}' успішно додано."
                else:
                    return f"Вправа '{exercise}' вже існує."
            except Exception as ex:
                print(f"add_user_exercise ERROR - {ex}")
                return 'Виникла помилка'

    def get_user_exercises(self, user_id: int, muscle_group: str = None) -> dict[str, list[str]]:
        with self.session_scope() as session:
            try:
                query = session.query(Exercise).filter(Exercise.user_id == user_id)
                if muscle_group is not None:
                    query = query.filter(Exercise.muscle_group_name == muscle_group)
                exercises = query.all()
                return {exercise.muscle_group_name: [ex.exercise_name for ex in exercises
                                                     if ex.muscle_group_name == exercise.muscle_group_name]
                        for exercise in exercises}
            except Exception as ex:
                print(f"get_user_exercises ERROR - {ex}")
                return {}

    def delete_user_exercise(self, user_id: int, muscle_group: str, exercise: str) -> str:
        with self.session_scope() as session:
            try:
                ex = session.query(Exercise).filter(Exercise.user_id == user_id,
                                                    Exercise.muscle_group_name == muscle_group,
                                                    Exercise.exercise_name == exercise).first()
                if ex is not None:
                    session.delete(ex)
                    session.commit()
                    return f"Вправу - {exercise} успішно видалено"
                return f"Вправи - {exercise} не існує"

            except Exception as ex:
                print(f"delete_user_exercise ERROR - {ex}")
                return 'Виникла помилка'

    def add_training_record(self, user_id: int, exercise: str, repeats: int, weight: int = 0) -> str:
        with self.session_scope() as session:
            try:
                date = datetime.now().date()
                time = datetime.now().time()
                ex = session.query(Exercise).filter(Exercise.user_id == user_id,
                                                    Exercise.exercise_name == exercise).first()
                if ex is not None:
                    training = Training(user_id=user_id, user_exercise_name=exercise, weight=weight, repeats=repeats,
                                        date=date, time=time)
                    session.add(training)
                    session.commit()
                    return "Успішно записано"

            except Exception as ex:
                print(f"add_training_record ERROR - {ex}")
                return 'Виникла помилка'

    def get_training_records(self, user_id: int, days: int) -> list[dict]:
        pass
