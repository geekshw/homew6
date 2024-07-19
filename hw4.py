# import logging
# import asyncio
# from aiogram import Bot, Dispatcher, types
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.types import Message
# from aiogram.filters import Command
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from config import token
# from database import Database

# logging.basicConfig(level=logging.INFO)
# bot = Bot(token=token)
# storage = MemoryStorage()
# dp = Dispatcher(storage=storage)
# db = Database('sql.db')
# db.create_table()

# class Form(StatesGroup):
#     username = State()
#     age = State()

# @dp.message(Command('start'))
# async def start(message: Message, state: FSMContext):
#     await state.set_state(Form.username)
#     await message.reply("Привет! Как тебя зовут?")

# @dp.message(Form.username)
# async def process_username(message: Message, state: FSMContext):
#     username = message.text
#     await state.update_data(username=username)
#     await state.set_state(Form.age)
#     await message.reply("Сколько тебе лет?")

# @dp.message(Form.age)
# async def process_age(message: Message, state: FSMContext):
#     age = message.text
#     user_data = await state.get_data()
#     username = user_data['username']
#     db.add_user(message.from_user.id, username)
#     await state.clear()
#     await message.reply(f"Приятно познакомиться, {username}! Тебе {age} лет.")

# def get_back_button():
#     keyboard = InlineKeyboardMarkup()
#     back_button = InlineKeyboardButton("Назад", callback_data="back")
#     keyboard.add(back_button)
#     return keyboard

# @dp.message(Command('me'))
# async def me(message: Message):
#     user = db.get_user(message.from_user.id)
#     if user:
#         await message.reply(f"Ты зарегистрирован как {user[2]}", reply_markup=get_back_button())
#     else:
#         await message.reply("Ты еще не зарегистрирован.")

# @dp.callback_query_handler(lambda c: c.data == 'back')
# async def process_callback_back(callback_query: types.CallbackQuery, state: FSMContext):
#     await bot.answer_callback_query(callback_query.id)
#     await state.set_state(Form.username)
#     await bot.send_message(callback_query.from_user.id, "Привет! Как тебя зовут?")

# async def on_startup():
#     logging.info("Настройки базы")
#     db.create_table()
#     logging.info("База загружена")

# async def main():
#     dp.startup.register(on_startup)
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())