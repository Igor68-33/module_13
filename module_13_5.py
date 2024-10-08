# Клавиатура кнопок
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

TOKEN = 'token_value'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_(message):
    await message.answer('Привет, я бот помогающий вашему здоровью. Выберите действие.',
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="Рассчитать"),
                                     KeyboardButton(text="Информация"),
                                 ]
                             ],
                             resize_keyboard=True, ),
                         )


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст (полных лет)',
                         reply_markup=ReplyKeyboardRemove(), )
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    # data = await state.get_data()
    # await message.answer(f'Возраст: {data["age"]}')
    await message.answer('Введите свой рост (см):',
                         reply_markup=ReplyKeyboardRemove(), )
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    # data = await state.get_data()
    # await message.answer(f'Рост: {data["growth"]}')
    await message.answer('Введите свой вес (кг):',
                         reply_markup=ReplyKeyboardRemove(), )
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    # await message.answer(f'Вес: {data["weight"]}')
    try:
        Calories_man = float(data["weight"]) * 10 + 6.25 * float(data["growth"]) - 5 * float(data["age"]) + 5
        Calories_wuman = float(data["weight"]) * 10 + 6.25 * float(data["growth"]) - 5 * float(data["age"]) - 161
        if Calories_wuman < 0:
            raise ValueError
        await message.answer(f'Норма калорий в сутки:',
                             reply_markup=ReplyKeyboardRemove(), )
        await message.answer(f'для мужчин: {Calories_man}')
        await message.answer(f'для женщин: {Calories_wuman}')
    except:
        await message.answer(f'Данные были введены неверно, повторите расчёт снова:',
                             reply_markup=ReplyKeyboardRemove(), )
    await state.finish()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
