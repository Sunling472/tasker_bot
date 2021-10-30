from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress

from ..base import get_list_tasks, del_task
from Tasker_bot.config.export_vars import dp
from .edit_tasks import StateEdit, editing_title, register_handler_edit_task


def get_keyboard(task_id: str):
    buttons: list = [
        types.InlineKeyboardButton(text='Редактировать', callback_data=f'edit|{task_id}'),
        types.InlineKeyboardButton(text='Удалить', callback_data=f'del|{task_id}')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


async def list_tasks(message: types.Message):
    user_id: int = message.from_user.id
    lt: list = get_list_tasks(user_id)
    if len(lt) == 0:
        await message.answer('Ни одного таска ещё не создано.')
    else:
        for task in lt:
            task_id: str = task[-1]
            await message.answer(f'{task[0]}\n\n{task[1]}', reply_markup=get_keyboard(task_id))


async def update_message(message: types.Message):
    with suppress(MessageNotModified):
        await message.edit_text('Задача удалена.')


@dp.callback_query_handler(Text(startswith='del'))
async def inline_del_handler(call: types.CallbackQuery):
    task_id: str = call.data.split('|')[1]
    del_task(int(task_id))
    await update_message(call.message)
    await call.answer()


@dp.callback_query_handler(Text(startswith='edit'))
async def inline_edit_handler(call: types.CallbackQuery):
    task_id: str = call.data.split('|')[1]

    StateEdit.edit_id = task_id
    await editing_title(call.message)
    await call.answer()


def register_handlers_list_task(dp: Dispatcher):
    dp.register_message_handler(list_tasks, commands=['list'])
    register_handler_edit_task(dp)



