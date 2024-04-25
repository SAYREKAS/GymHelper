from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup


def create_inline_kbs(args: list[str]):
    keyboards = []

    for item in args:
        keyboards.append([InlineKeyboardButton(text=item, callback_data=item)])

    result = InlineKeyboardMarkup(inline_keyboard=keyboards)

    return result


class InlineKb:
    settings_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='вказати параметри тіла', callback_data='config_user_menu')],
        [InlineKeyboardButton(text='редагувати список вправ', callback_data='config_user_menu')],
    ])


def main():
    test_btns_list = ['1', '2', '3', '4', ]

    create_reply_kbs(test_btns_list)


if __name__ == '__main__':
    main()
