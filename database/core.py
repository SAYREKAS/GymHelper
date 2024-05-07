from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from database.models import Base, User, MuscleGroups, Exercise, Training
from database.servises import GymHelper
from config import DATABASE_USER, DATABASE_PASS, DATABASE_HOST, DATABASE_NAME

muscle_group_list = ['Шия', 'Плечі', 'Груди', 'Руки', 'Живіт', 'Спина', 'Сідниці', 'Ноги']

engine = create_engine(f'mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}/{DATABASE_NAME}')
Session = sessionmaker(engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as ex:
        print(f"session_scope ERROR - {ex}")
        session.rollback()
        raise
    finally:
        session.close()


def create_all_table() -> None:
    with session_scope():
        try:
            Base.metadata.create_all(engine)
            print('\nAll TABLE CREATED')
        except Exception as ex:
            print(f"\ncreate_all_table ERROR - {ex}\n")


def drop_all_table() -> None:
    with session_scope():
        try:
            Training.metadata.drop_all(engine)
            Exercise.metadata.drop_all(engine)
            MuscleGroups.metadata.drop_all(engine)
            User.metadata.drop_all(engine)
            print('\nAll TABLE DROP')
        except Exception as ex:
            print(f"\ndrop_all_table ERROR - {ex}\n")


gh = GymHelper(session_scope)

if __name__ == '__main__':
    drop_all_table()
    create_all_table()
    gh.add_muscle_groups(name_list=muscle_group_list)
    print(gh.get_muscle_groups())
    pass
