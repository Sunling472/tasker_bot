from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from Tasker_bot.app.base import edit_task


class StateEdit(StatesGroup):
    edit_id: str = ''
    edit_title = State()
    edit_body = State()


async def editing_title(message: types.Message):
    await message.answer('Введите новый заголовок:')
    await StateEdit.edit_title.set()


async def editing_body(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await StateEdit.next()
    await message.answer('Введите новый текст:')


async def editing_task(message: types.Message, state: FSMContext):
    await state.update_data(body=message.text)
    task_edit: dict = await state.get_data()
    try:
        edit_id: int = int(StateEdit.edit_id)
        title: str = task_edit['title']
        body: str = task_edit['body']
        edit_task(edit_id, title, body)
        await message.answer('Запись успешно отредактирована.')

    except ValueError:
        await message.answer('id может содержать только цифры.')

    finally:
        await state.finish()


def register_handler_edit_task(dp: Dispatcher):
    dp.register_message_handler(editing_title, state='*', commands='edit')
    dp.register_message_handler(editing_body, state=StateEdit.edit_title)
    dp.register_message_handler(editing_task, state=StateEdit.edit_body)
