import os
from aiogram.types import BotCommand
from dotenv import load_dotenv

from db import Connection, GymDb, GymUser

load_dotenv()

TOKEN = os.getenv('BOT_API')

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASS = os.getenv('DATABASE_PASS')
DATABASE_NAME = os.getenv('DATABASE_NAME')

BOT_COMMAND = [
    BotCommand(command='start', description='перезапустити бота'),
]

muscle_group_list = ['Шия', 'Плечі', 'Груди', 'Руки', 'Живіт', 'Спина', 'Сідниці', 'Ноги']

con = Connection(host=DATABASE_HOST, user=DATABASE_USER, password=DATABASE_PASS, database=DATABASE_NAME)
db = GymDb(con)
user = GymUser(con)
