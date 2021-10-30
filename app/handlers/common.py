from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


from ..base import user_reg, is_reg


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer(
        'Выберете действие:',

    )


async def reg(message: types.Message, state: FSMContext):
    await state.finish()

    user_id: int = message.from_user.id
    if is_reg(user_id):
        await message.answer('Вы уже зарегистрированы.')
    else:
        user_reg(user_id)
        await message.answer('Вы успешно зарегистрированы!')


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Действие отменено')


# Функция регистрации хэндлеров
def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start', state='*')
    dp.register_message_handler(reg, commands=['reg'], state='*')
    dp.register_message_handler(cancel, commands=['cancel'], state='*')


