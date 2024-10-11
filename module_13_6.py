# Клавиатура кнопок
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import filters
from aiogram.dispatcher import FSMContext
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

in_kb = types.InlineKeyboardMarkup()
in_button1 = types.InlineKeyboardButton(text='Button1', callback_data='in_button1')
in_kb.add(in_button1)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['help'])
async def start_(message):
    await message.answer(text='/help is pressed', reply_markup=in_kb)


@dp.callback_query_handler(text='in_button1')
@dp.callback_query_handler(filters.Text(contains='in_button1'))
async def some_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Pressed in_button1')


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
