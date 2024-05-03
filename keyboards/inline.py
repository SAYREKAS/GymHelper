from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup


def create_reply_kbs(button_name_list: list[str], group: int = None):
    keyboards = []

    if group:
        sep_keyboards = [button_name_list[i:i + group] for i in range(0, len(button_name_list), group)]
        for item in sep_keyboards:
            keyboards.append([InlineKeyboardButton(text=str(f), callback_data=str(f)) for f in item])
    else:
        for item in button_name_list:
            keyboards.append([InlineKeyboardButton(text=str(item), callback_data=str(item))])

    result = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return result


class InlineKb:
    settings_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='вказати параметри тіла', callback_data='вказати параметри тіла')],
        [InlineKeyboardButton(text='редагувати список вправ', callback_data='редагувати список вправ')],
    ])
