from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

repeat_step_1_30 = range(1, 51)

weight_step_1_30 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30,
                    35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]


def create_reply_kbs(button_name_list: list[str], group: int = None):
    keyboards = []

    if group:
        sep_keyboards = [button_name_list[i:i + group] for i in range(0, len(button_name_list), group)]
        for item in sep_keyboards:
            keyboards.append([KeyboardButton(text=str(f)) for f in item])
    else:
        for item in button_name_list:
            keyboards.append([KeyboardButton(text=str(item))])

    result = ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True)
    return result


class ReplyKb:
    start_menu = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Вказати параметри тіла', )],
    ], resize_keyboard=True)

    main_menu = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Почати тренування', )],
        [KeyboardButton(text='Додати нову вправу')],
        [KeyboardButton(text='Налаштування')],
    ], resize_keyboard=True)

    settings_menu = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Вказати параметри тіла', )],
        [KeyboardButton(text='Видалити вправу')],
        [KeyboardButton(text='Головне меню')],
    ], resize_keyboard=True)

    gender_btn = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='👨‍💼Чоловік', )],
        [KeyboardButton(text='👩‍💼Жінка')],
    ], resize_keyboard=True)

    another_training = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Додати ще один підхід', )],
        [KeyboardButton(text='Головне меню', )],
    ], resize_keyboard=True)
