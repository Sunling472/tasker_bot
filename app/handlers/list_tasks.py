from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup

from ..base import get_list_tasks, del_task


def get_keyboard():
    buttons: list = [
        types.InlineKeyboardButton(text='Редактировать', callback_data='edit'),
        types.InlineKeyboardButton(text='Удалить', callback_data='del')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


async def list_tasks(message: types.Message):
    keyboard = get_keyboard()
    user_id: int = message.from_user.id
    lt: list = get_list_tasks(user_id)
    if len(lt) == 0:
        await message.answer('Ни одного таска ещё не создано.')
    else:
        for task in lt:
            await message.answer(f'{task[0]}\n\n{task[1]}\n\nid: {task[-1]}', reply_markup=keyboard)


async def inline_del_handler(call: types.CallbackQuery, message: types.Message):
    pass


def register_handlers_list_task(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(list_tasks, commands=['list'])
