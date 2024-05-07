from aiogram.fsm.context import FSMContext
from aiogram.types import Message


def is_number(stroke: str, lenght: int) -> bool:
    try:
        num = float(stroke.replace(',', '.'))
        if lenght >= num > 0:
            return True
    except ValueError:
        return False


async def update_and_notify(message: Message, state: FSMContext, field: str, value: str, redact_message: int = None):
    await state.update_data({field: value})
    data = await state.get_data()
    if not redact_message:
        await message.answer(f"Група мʼязів - {data.get('muscle_group') if data.get('muscle_group') else '❔'}\n"
                             f"Вправа - {data.get('exercise') if data.get('exercise') else '❔'}\n"
                             f"Вага - {data.get('weight') if data.get('weight') else '❔'} кг\n"
                             f"Повтори - {data.get('repeats') if data.get('repeats') else '❔'} раз\n")
