from aiogram.types import ReplyKeyboardRemove
from settings import muscle_group_list, db, user, con
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardBuilder


def create_reply_kbs(button_name_list: list[str], ):
    keyboards = []

    for item in button_name_list:
        keyboards.append([KeyboardButton(text=item, callback_data=item, )])

    result = ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True, )

    return result


class ReplyKb:
    start_menu = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Вказати параметри тіла', )],
    ], resize_keyboard=True,
    )

    main_menu = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Почати тренування', )],
        [KeyboardButton(text='Додати нову вправу')],
        [KeyboardButton(text='Налаштування')],
    ], resize_keyboard=True,
    )
    gender_btn = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='👨‍💼Чоловік', )],
        [KeyboardButton(text='👩‍💼Жінка')],
    ], resize_keyboard=True,
    )
