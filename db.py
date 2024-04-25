import pymysql
import datetime
from datetime import datetime, timedelta
from pymysql.connections import Connection as PyMySQLConnection
from settings import *


class Connection:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        self.__host = str(host)
        self.__port = int(port)
        self.__user = str(user)
        self.__password = str(password)
        self.__database = str(database)
        self.session = self.__start()

    def __start(self) -> PyMySQLConnection:
        try:
            con = pymysql.connect(host=self.__host,
                                  port=self.__port,
                                  user=self.__user,
                                  password=self.__password,
                                  database=self.__database
                                  )
        except Exception as ex:
            print(ex)
        else:
            print(f"\nПідключення до БД успішне")
            return con


class GymDb:
    def __init__(self, conection: Connection):
        self.__connection = conection.session

    def __user_table(self) -> None:
        with self.__connection.cursor() as cursor:
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
        self.__connection.commit()

    def __muscle_groups_table(self) -> None:

        with self.__connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS muscle_groups (
            group_name VARCHAR(255) PRIMARY KEY)""")
        self.__connection.commit()

    def __user_exercise_table(self) -> None:
        with self.__connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_exercise (
            id INT PRIMARY KEY AUTO_INCREMENT,
            muscle_group_name VARCHAR(255),
            user_id INT,
            exercise_name VARCHAR(255),
            FOREIGN KEY (muscle_group_name) REFERENCES muscle_groups(group_name),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
            )""")
        self.__connection.commit()

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
        with self.__connection.cursor() as cursor:
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
        self.__connection.commit()

    def configure_table(self) -> None:
        """Створює всі потрібні таблиці"""
        try:
            self.__user_table()
            print('\n__user_table OK')
            self.__muscle_groups_table()
            print('__muscle_groups_table OK')
            self.__user_exercise_table()
            print('__user_exercise_table OK')
            self.__training_table()
            print('__training_table OK')

        except Exception as ex:
            print(ex)
        else:
            print('\nТаблиці успішно сконфігуровані')

    def add_muscle_groups(self, muscle_groups_list: list[str]) -> None:
        """
            Додає нову групу м'язів до таблиці груп м'язів (muscle_groups).

            Параметри:
            - arg: str - назва нової групи м'язів

            Якщо група м'язів з вказаною назвою вже існує в базі даних, виводиться повідомлення про це.
            Інакше, група м'язів додається до бази даних, і виводиться повідомлення про успішне додавання.
            """
        with self.__connection.cursor() as cursor:
            for muscle_group in muscle_groups_list:
                cursor.execute("SELECT * FROM muscle_groups WHERE group_name = %s", (muscle_group,))
                existing_group = cursor.fetchone()
                if existing_group:
                    print(f"Група м'язів '{muscle_group}' вже існує.")
                else:
                    cursor.execute("INSERT INTO muscle_groups (group_name) VALUES (%s)", (muscle_group,))
                    print(f"Групу м'язів '{muscle_group}' успішно додано.")
        self.__connection.commit()

    def get_muscle_groups(self) -> list[str]:
        """
        Повертає список доступних груп м'язів.

        Returns:
        list[str]: Список назв груп м'язів.
        """
        with self.__connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT group_name FROM muscle_groups")
            result = cursor.fetchall()
            muscle_groups = [row[0] for row in result]
        return muscle_groups

    def drop_tables(self) -> None:
        """
        Видаляє усі створені таблиці з бази даних.
        """
        with self.__connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS training")
            cursor.execute("DROP TABLE IF EXISTS user_exercise")
            cursor.execute("DROP TABLE IF EXISTS muscle_groups")
            cursor.execute("DROP TABLE IF EXISTS users")
        self.__connection.commit()


class GymUser:
    def __init__(self, conection: Connection):
        self.connection = conection.session

    def add_user(self, user_id: int, first_name: str, last_name: str, username: str) -> None:
        """
            Додає нового користувача до таблиці користувачів (users).

            Параметри:
            - user_id: int - унікальний ідентифікатор користувача
            - first_name: str - ім'я користувача
            - last_name: str - прізвище користувача
            - username: str - ім'я користувача у системі

            """
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (user_id, first_name, last_name, username) VALUES (%s, %s, %s, %s)",
                           (user_id, first_name, last_name, username,))
            print(f"\nКористувача '{user_id}' успішно додано.")
        self.connection.commit()

    def user_exist(self, user_id: int) -> bool:
        """
        перевіряємо чи існує користувач з такимм user_id в БД

        :param:
            user_id: int

        :return:
            True - якщо снує,
            False - якщо не існує.
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            existing_group = cursor.fetchone()
            if existing_group:
                return True
        return False

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

    def add_user_exercise(self, user_id: int, muscle_group_name: str, exercise_name: str) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM user_exercise WHERE exercise_name = %s AND user_id = %s",
                (exercise_name, user_id,))
            existing_exercise = cursor.fetchone()
            if existing_exercise:
                print(f"\nВправа '{exercise_name}' "
                      f"для користувача з id {user_id} "
                      f"та групи м'язів з імʼям {muscle_group_name} вже існує.")
            else:
                cursor.execute(
                    "INSERT INTO user_exercise (muscle_group_name, user_id, exercise_name) VALUES (%s, %s, %s)",
                    (muscle_group_name, user_id, exercise_name,))
                print(f"\nЗапис '{exercise_name}' для користувача з id {user_id} "
                      f"та групи м'язів з імʼям {muscle_group_name} успішно додано.")
        self.connection.commit()

    def get_user_exercises(self, user_id: int, muscle_group_name: str = None) -> list[str]:
        exercises = []
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT exercise_name, muscle_group_name  FROM user_exercise WHERE user_id = %s",
                           (user_id,))
            result = cursor.fetchall()
            for row in result:
                if muscle_group_name:
                    if row[1] == muscle_group_name:
                        exercises.append(row[0])
                else:
                    exercises.append(row[0])

        return exercises

    def add_training_record(self, id_user_exercise: int, user_id: int, repeats: int, weight: int = 0) -> None:
        """
        Додає запис про тренування для користувача.

        :param id_user_exercise: Ідентифікатор вправи для користувача.
        :param user_id: Ідентифікатор користувача.
        :param repeats: Кількість повторів у вправі.
        :param weight: Вага, яку використовував користувач (за замовчуванням 0).
        """
        date = datetime.now().date()
        time = datetime.now().time()

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

    def get_training_records(self, user_id: int, days: int) -> list[dict]:
        """
        Отримує тренувальні записи для користувача за останній кількість днів.

        :param user_id: int - ідентифікатор користувача
        :param days: int - кількість днів назад
        :return: list - список тренувальних записів
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM training
                WHERE user_id = %s AND date BETWEEN %s AND %s
            """, (user_id, start_date, end_date))
            result = cursor.fetchall()
            training_records = []
            for row in result:
                training_records.append({
                    'id': row[0],
                    'id_user_exercise': row[1],
                    'user_id': row[2],
                    # 'date': row[3],
                    # 'time': row[4],
                    'weight': row[5],
                    'repeats': row[6]
                })
        return training_records


def main():
    db.drop_tables()
    db.configure_table()
    db.add_muscle_groups(muscle_group_list)


if __name__ == '__main__':
    main()
