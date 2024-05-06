from sqlalchemy import ForeignKey, Index, Date, Time
from sqlalchemy import String, BigInteger
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(50))
    weight: Mapped[int] = mapped_column(nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
    tall: Mapped[int] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(String(50), nullable=True)


class MuscleGroups(Base):
    __tablename__ = 'muscle_groups'

    group_name: Mapped[str] = mapped_column(String(255), primary_key=True)


class Exercise(Base):
    __tablename__ = "exercise"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    muscle_group_name: Mapped[str] = mapped_column(String(50), ForeignKey('muscle_groups.group_name'))
    exercise_name: Mapped[str] = mapped_column(String(255))


class Training(Base):
    __tablename__ = "training"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user_exercise_name: Mapped[int] = mapped_column(ForeignKey('exercise.exercise_name'))
    weight: Mapped[int] = mapped_column()
    repeats: Mapped[int] = mapped_column()
    date: Mapped[Date] = mapped_column(Date)
    time: Mapped[Time] = mapped_column(Time)


Index('exercise_name_index', Exercise.exercise_name)
