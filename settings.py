import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_API')

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASS = os.getenv('DATABASE_PASS')
DATABASE_NAME = os.getenv('DATABASE_NAME')

muscle_group_list = ['шия',
                     'плечі',
                     'груди',
                     'руки',
                     'живіт',
                     'спина',
                     'сідниці',
                     'ноги',
                     ]
