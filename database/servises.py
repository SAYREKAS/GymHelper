from datetime import datetime

from sqlalchemy.orm import Session

from database.models import User, MuscleGroups, Exercise, Training


class GymHelper:
    def __init__(self, session: Session):
        self.session = session

    def add_new_user(self, user_id: int, first_name: str = None, last_name: str = None, username: str = None) -> None:
        new_user = User(user_id=user_id, first_name=first_name, last_name=last_name, username=username)
        self.session.add(new_user)
        self.session.commit()

    def add_user_details(self, user_id: int, weight: int, age: int, tall: int, gender: str) -> str:
        user = self.session.query(User).filter_by(user_id=user_id).first()

        if user is not None:
            user.weight = weight
            user.age = age
            user.tall = tall
            user.gender = gender
            self.session.commit()
            return "Дані успішно оновлено"
        else:
            return "Сталася помилка"

    def user_exist(self, user_id: int = None) -> bool:
        return True if user_id in [info.user_id for info in self.session.query(User).all()] else False

    def add_muscle_groups(self, name_list: list[str]) -> None:
        try:
            for name in name_list:
                self.session.add(MuscleGroups(group_name=name))
            self.session.commit()
            print(f"{name_list} added to muscle_groups")
        except Exception as ex:
            print(f"\nadd_muscle_groups ERROR - {ex}\n")

    def get_muscle_groups(self) -> list[str]:
        return [name.group_name for name in self.session.query(MuscleGroups).all()]

    def add_user_exercise(self, user_id: int, muscle_group_name: str, exercise_name: str) -> str:
        ex_exist = self.session.query(Exercise).filter_by(user_id=user_id, muscle_group_name=muscle_group_name,
                                                          exercise_name=exercise_name).first()
        if ex_exist is None:
            new_exercise = Exercise(user_id=user_id, muscle_group_name=muscle_group_name, exercise_name=exercise_name)
            self.session.add(new_exercise)
            self.session.commit()
            return f"Вправу '{exercise_name}' успішно додано."
        else:
            return f"Вправа '{exercise_name}' вже існує."

    def get_user_exercises(self, user_id: int, muscle_group_name: str = None) -> dict[str, list[str]]:
        query = self.session.query(Exercise).filter(Exercise.user_id == user_id)

        if muscle_group_name is not None:
            query = query.filter(Exercise.muscle_group_name == muscle_group_name)

        exercises = query.all()

        return {
            exercise.muscle_group_name: [ex.exercise_name for ex in exercises if
                                         ex.muscle_group_name == exercise.muscle_group_name] for exercise in exercises
        }

    def delete_user_exercise(self, user_id: int, muscle_group_name: str, exercise_name: str) -> str:
        exercise = self.session.query(Exercise).filter(Exercise.user_id == user_id,
                                                       Exercise.muscle_group_name == muscle_group_name,
                                                       Exercise.exercise_name == exercise_name).first()
        if exercise is not None:
            self.session.delete(exercise)
            self.session.commit()
            return f"Вправу - {exercise_name} успішно видалено"
        return f"Вправи - {exercise_name} не існує"

    def add_training_record(self, user_id: int, exercise_name: str, repeats: int, weight: int = 0) -> str:
        date = datetime.now().date()
        time = datetime.now().time()
        exercise = self.session.query(Exercise).filter(Exercise.user_id == user_id,
                                                       Exercise.exercise_name == exercise_name).first()
        if exercise is not None:
            training = Training(user_id=user_id, user_exercise_name=exercise_name, weight=weight, repeats=repeats,
                                date=date, time=time)
            self.session.add(training)
            self.session.commit()
            return "Успішно записано"

        return 'Сталася помилка під час збереження інформації'

    def get_training_records(self, user_id: int, days: int) -> list[dict]:
        pass
