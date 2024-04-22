import datetime
from pprint import pprint

import pymysql
from settings import *


class Db:
    def __init__(self, host: str, user: str, password: str, port: int, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = int(port)
        self.connection = self.__connect()

    def __connect(self):
        """Підключаємося до бази даних"""
        try:
            conection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Exception as ex:
            print(ex)
        else:
            print(f"\nПідключення до БД успішне")
            return conection

    def configure_table(self):
        """Створюємо всі необхідні таблиці для роботи програми:

        USERS;

        MUSCLE_GROUP;

        USER_EXERCISE;

        TRAINING;
        """
        self.__create_user_table()
        self.__muscle_groups_table()
        self.__user_exercise_table()
        self.__training_table()

    def __create_user_table(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY AUTO_INCREMENT, 
            user_id INT UNIQUE, 
            first_name VARCHAR(255), 
            last_name VARCHAR(255), 
            username VARCHAR(255),
            weight INT,
            age INT,
            tall INT,
            gender VARCHAR(255)
            )""")
        self.connection.commit()

    def __muscle_groups_table(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS muscle_groups (
            id INT PRIMARY KEY AUTO_INCREMENT,
            groups_name VARCHAR(255))""")
        self.connection.commit()

    def __user_exercise_table(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_exercise (
            id INT PRIMARY KEY AUTO_INCREMENT,
            id_muscle_group INT,
            user_id INT,
            exercise_name VARCHAR(255) UNIQUE,
            FOREIGN KEY (id_muscle_group) REFERENCES muscle_groups(id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
            )""")
        self.connection.commit()

    def __training_table(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS training (
            id INT PRIMARY KEY AUTO_INCREMENT,
            id_user_exercise INT,
            user_id INT,
            date DATE,
            time TIME,
            weight INT,
            repeats INT,
            FOREIGN KEY (id_user_exercise) REFERENCES training(id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
            )""")
        self.connection.commit()

    def add_user(self, user_id: int, first_name: str, last_name: str, username: str) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            existing_group = cursor.fetchone()
            if existing_group:
                print(f"\nКористувач '{user_id}' вже існує.")
            else:
                cursor.execute("INSERT INTO users (user_id, first_name, last_name, username) VALUES (%s, %s, %s, %s)",
                               (user_id, first_name, last_name, username,))
                print(f"\nКористувача '{user_id}' успішно додано.")
        self.connection.commit()

    def add_muscle_groups(self, arg: str) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM muscle_groups WHERE groups_name = %s", (arg,))
            existing_group = cursor.fetchone()
            if existing_group:
                print(f"\nГрупа м'язів '{arg}' вже існує.")
            else:
                cursor.execute("INSERT INTO muscle_groups (groups_name) VALUES (%s)", (arg,))
                print(f"\nГрупу м'язів '{arg}' успішно додано.")
        self.connection.commit()

    def add_user_exercise(self, id_muscle_group: int, user_id: int, exercise_name: str) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM user_exercise WHERE id_muscle_group = %s AND user_id = %s AND exercise_name = %s",
                (id_muscle_group, user_id, exercise_name))
            existing_exercise = cursor.fetchone()
            if existing_exercise:
                print(f"\nВправа '{exercise_name}' "
                      f"для користувача з id {user_id} "
                      f"та групи м'язів з id {id_muscle_group} вже існує.")
            else:
                cursor.execute(
                    "INSERT INTO user_exercise (id_muscle_group, user_id, exercise_name) VALUES (%s, %s, %s)",
                    (id_muscle_group, user_id, exercise_name,))
                print(f"\nЗапис '{exercise_name}' для користувача з id {user_id} "
                      f"та групи м'язів з id {id_muscle_group} успішно додано.")
        self.connection.commit()

    def get_user_exercises(self, user_id: int) -> dict:
        """
            Отримує всі вправи для заданого користувача.

            Args:
                user_id (int): ID користувача.

            Returns:
                dict: Словник, де ключі - це ID вправ, а значення - це словники, що містять 'muscle_group_id'
                      та 'exercise_name'.
            """
        exercises = {}
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT id, id_muscle_group, exercise_name FROM user_exercise WHERE user_id = %s",
                           (user_id,))
            result = cursor.fetchall()
            for row in result:
                exercises[row[0]] = {'muscle_group_id': row[1], 'exercise_name': row[2]}
        return exercises

    def add_training_record(self, id_user_exercise: int, user_id: int, repeats: int, weight: int = 0) -> None:
        date = datetime.date.today().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")

        with self.connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO training 
                (id_user_exercise, user_id, date, time, weight, repeats) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (id_user_exercise, user_id, date, time, weight, repeats,))
            print(f"\nТренувальний запис для користувача з id {user_id}, "
                  f"з id_user_exercise {id_user_exercise}, "
                  f"датою {date}, "
                  f"часом {time}, "
                  f"вагою {weight} "
                  f"та повторами {repeats} "
                  f"успішно додано.")
        self.connection.commit()


if __name__ == '__main__':
    db = Db(host=DATABASE_HOST,
            port=DATABASE_PORT,
            user=DATABASE_USER,
            password=DATABASE_PASS,
            database=DATABASE_NAME)

    for f in db.get_user_exercises(user_id=11111).values():
        pprint(f)
