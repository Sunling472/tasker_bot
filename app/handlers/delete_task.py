from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from ..base import del_task


class StateDel(StatesGroup):
    del_id = State()


async def get_task_id_del(message: types.Message):
    await message.answer('Введите id таска, который нужно удалить.')
    await StateDel.del_id.set()


async def delete_task(message: types.Message, state: FSMContext):

    await state.update_data(task_id=message.text)

    task_id_dict: dict = await state.get_data()
    try:
        task_id = int(task_id_dict['task_id'])
        del_task(task_id)
        await message.answer('Таск успешно удалён.')
        await state.finish()

    except ValueError:
        await message.answer('Ошибка, в task_id могут быть только цифры.')
        await state.finish()


def register_handler_delete_task(dp: Dispatcher):
    dp.register_message_handler(get_task_id_del, commands='del', state='*')
    dp.register_message_handler(delete_task, state=StateDel.del_id)
