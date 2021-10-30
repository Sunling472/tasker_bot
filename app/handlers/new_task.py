from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Tasker_bot.app.base import new_task, get_last_task_id


class TaskState(StatesGroup):
    title = State()
    body = State()


async def start_new_task(message: types.Message):
    await message.answer('Введите заголовок:')
    await TaskState.title.set()


async def get_title_body(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await TaskState.next()
    await message.answer('Введите текст задачи:')


async def add_task(message: types.Message, state: FSMContext):
    await state.update_data(body=message.text)

    task_dict: dict = await state.get_data()
    user_id: int = message.from_user.id
    title: str = task_dict['title']
    body: str = task_dict['body']
    task_id: int or None = get_last_task_id()
    if task_id is None:
        new_task(user_id, title, body)
        await message.answer('Таск успешно создан!')
    else:
        task_id = task_id + 1
        new_task(user_id, title, body, task_id)
        await message.answer('Таск успешно создан!')

    await state.finish()


def register_handlers_new_task(dp: Dispatcher):
    dp.register_message_handler(start_new_task, commands=['new'], state='*')
    dp.register_message_handler(get_title_body, state=TaskState.title)
    dp.register_message_handler(add_task, state=TaskState.body)
    # dp.register_message_handler(add_task)
