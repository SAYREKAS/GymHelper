import datetime
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
        """Створює всі потрібні таблиці"""
        self.__create_user_table()
        self.__muscle_groups_table()
        self.__user_exercise_table()
        self.__training_table()

    def __create_user_table(self) -> None:
        """
            Створює таблицю користувачів (users), яка зберігає дані про користувачів.

            Структура таблиці:
            - id: INT - унікальний ідентифікатор користувача
            - user_id: INT - унікальний ідентифікатор користувача (може бути використаний для зовнішніх систем)
            - first_name: VARCHAR(255) - ім'я користувача
            - last_name: VARCHAR(255) - прізвище користувача
            - username: VARCHAR(255) - ім'я користувача у системі
            - weight: INT - вага користувача
            - age: INT - вік користувача
            - tall: INT - зріст користувача
            - gender: VARCHAR(255) - стать користувача
            """
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
        """
            Створює таблицю груп м'язів (muscle_groups), яка зберігає назви груп м'язів.

            Структура таблиці:
            - id: INT - унікальний ідентифікатор групи м'язів
            - groups_name: VARCHAR(255) - назва групи м'язів
            """
        with self.connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS muscle_groups (
            id INT PRIMARY KEY AUTO_INCREMENT,
            groups_name VARCHAR(255))""")
        self.connection.commit()

    def __user_exercise_table(self) -> None:
        """
            Створює таблицю записів вправ користувачів (user_exercise), яка зберігає інформацію про вправи, які виконує користувач.

            Структура таблиці:
            - id: INT - унікальний ідентифікатор запису
            - id_muscle_group: INT - ідентифікатор групи м'язів, до якої відноситься вправа
            - user_id: INT - ідентифікатор користувача, який додав вправу
            - exercise_name: VARCHAR(255) - назва вправи
            """
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
        """
            Створює таблицю тренувальних записів (training), яка зберігає інформацію про тренування користувачів.

            Структура таблиці:
            - id: INT - унікальний ідентифікатор запису
            - id_user_exercise: INT - ідентифікатор запису вправи користувача
            - user_id: INT - ідентифікатор користувача, який проводить тренування
            - date: DATE - дата тренування
            - time: TIME - час тренування
            - weight: INT - вага, з якою була виконана вправа
            - repeats: INT - кількість повторень
            """
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
        """
            Додає нового користувача до таблиці користувачів (users).

            Параметри:
            - user_id: int - унікальний ідентифікатор користувача
            - first_name: str - ім'я користувача
            - last_name: str - прізвище користувача
            - username: str - ім'я користувача у системі

            Якщо користувач з вказаним user_id вже існує в базі даних, виводиться повідомлення про це.
            Інакше, користувача додається до бази даних, і виводиться повідомлення про успішне додавання.
            """
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

    def add_user_details(self, user_id: int, weight: int, age: int, tall: int, gender: str) -> None:
        """
        Додає дані про вагу, вік, зріст та стать користувача до таблиці користувачів (users).

        :param user_id: int - унікальний ідентифікатор користувача
        :param weight: int - вага користувача
        :param age: int - вік користувача
        :param tall: int - зріст користувача
        :param gender: str - стать користувача
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET weight = %s, age = %s, tall = %s, gender = %s WHERE user_id = %s",
                (weight, age, tall, gender, user_id,))
            self.connection.commit()
            print(f"\nДані користувача з id {user_id} успішно оновлено.")

    def add_muscle_groups(self, arg: str) -> None:
        """
            Додає нову групу м'язів до таблиці груп м'язів (muscle_groups).

            Параметри:
            - arg: str - назва нової групи м'язів

            Якщо група м'язів з вказаною назвою вже існує в базі даних, виводиться повідомлення про це.
            Інакше, група м'язів додається до бази даних, і виводиться повідомлення про успішне додавання.
            """
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
        """
        Додає новий запис про вправу користувача до таблиці вправ користувача (user_exercise).

        Параметри:
        - id_muscle_group: int - ідентифікатор групи м'язів
        - user_id: int - ідентифікатор користувача
        - exercise_name: str - назва вправи

        Якщо вправа для вказаного користувача та групи м'язів вже існує в базі даних, виводиться повідомлення про це.
        Інакше, новий запис додається до бази даних, і виводиться повідомлення про успішне додавання.
        """
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
        """
        Додає запис про тренування для користувача.

        :param id_user_exercise: Ідентифікатор вправи для користувача.
        :param user_id: Ідентифікатор користувача.
        :param repeats: Кількість повторів у вправі.
        :param weight: Вага, яку використовував користувач (за замовчуванням 0).
        """
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
    db = Db(host=DATABASE_HOST, port=DATABASE_PORT, user=DATABASE_USER, password=DATABASE_PASS, database=DATABASE_NAME)

    db.add_user_details(user_id=11111, weight=106, age=27, tall=190, gender='чоловік')
